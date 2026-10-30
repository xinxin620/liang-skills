#!/usr/bin/env python3
"""check_assets.py 的回归自测：用内存里的样例文档断言该报的码报了、不该报的不报。

只测检查器自己的判定，不测资产拆得对不对。新增错误码时在这里补一条用例。
运行：``python scripts/selftest.py``（Windows 用 `python`）
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import check_assets as ca

GOOD_VISUAL = """\
# EP001 视觉设定

## 人物与造型

### CHAR-JIANGCHEN · 江晨
- 识别锚点：方下颌，左眉骨一道两厘米浅疤。
- 来源：S001

#### LOOK-JIANGCHEN-DRESS · 江晨常服
- 识别锚点：松枝绿翻领制服，铜扣五粒。
- 连续性锁：LOCK-JIANGCHEN-DRESS《江晨松枝绿常服》（镜头：入画；生图提示词项：IMG-LOOK-JIANGCHEN-DRESS）· 锁面：pine-green lapel service jacket
"""

GOOD_PROMPT = """\
# EP001 资产生图提示词

## IMG-LOOK-JIANGCHEN-DRESS · 江晨常服三视图
- 资产：LOOK-JIANGCHEN-DRESS
- 用途：造型参考板
- 视图：16:9 三视图
- 文字政策：`no_readable_text` → `blank`
- 参考：无外部参考

### 可复制提示词

> 人物设定三视图，左半幅半身特写，右侧正面全身与背面全身同一人物。
> 身穿 pine-green lapel service jacket，松枝绿翻领，铜扣五粒，配色与形制完全统一。
> 纯净中灰背景，棚拍柔光。
"""


def codes(visual, prompt, partial=False):
    findings = ca.validate_documents(visual, prompt, partial)
    return [item.code for item in findings if item.severity == "error"]


def notes(visual, prompt, partial=False):
    findings = ca.validate_documents(visual, prompt, partial)
    return [item.code for item in findings if item.severity == "note"]


CASES = []


def case(name, expected_errors, expected_notes=(), partial=False):
    def wrap(fn):
        CASES.append((name, fn, set(expected_errors), set(expected_notes), partial))
        return fn

    return wrap


@case("完整且正确的一集，零错误", [])
def _good():
    return GOOD_VISUAL, GOOD_PROMPT


@case("锁面被改写，LK-03", ["LK-03"])
def _surface_rewritten():
    prompt = GOOD_PROMPT.replace("pine-green lapel service jacket", "松枝绿翻领制服")
    return GOOD_VISUAL, prompt


@case("锁面只出现在否定句里，LK-04", ["LK-04"])
def _surface_negated():
    prompt = GOOD_PROMPT.replace(
        "身穿 pine-green lapel service jacket", "不要 pine-green lapel service jacket"
    )
    return GOOD_VISUAL, prompt


@case("锁名缺中文与缺锁面，两条 LK-01", ["LK-01", "LK-01"])
def _bad_lock_syntax():
    visual = GOOD_VISUAL.replace(
        "LOCK-JIANGCHEN-DRESS《江晨松枝绿常服》（镜头：入画；生图提示词项：IMG-LOOK-JIANGCHEN-DRESS）· 锁面：pine-green lapel service jacket",
        "LOCK-JIANGCHEN-DRESS《Dress》（镜头：入画）",
    )
    return visual, GOOD_PROMPT


@case("锁面消失、锁面被改写", ["LK-03"])
def _missing_surface():
    prompt = GOOD_PROMPT.replace("pine-green lapel service jacket，松枝绿翻领，", "")
    return GOOD_VISUAL, prompt


@case("锁 ID 重复，LK-02", ["LK-02"])
def _duplicate_lock():
    visual = GOOD_VISUAL
    line = [
        text
        for text in visual.splitlines()
        if text.strip().startswith("- 连续性锁")
    ][0]
    return visual + line + "\n", GOOD_PROMPT


@case("镜头写全集又混 SHOT-，LK-06", ["LK-06"])
def _mixed_scope():
    visual = GOOD_VISUAL.replace("镜头：入画", "镜头：全集、SHOT-001")
    return visual, GOOD_PROMPT


@case("入画但无来源可展开，LK-06（提示级）", [], ["LK-06"])
def _no_source():
    visual = GOOD_VISUAL.replace("- 来源：S001\n", "")
    return visual, GOOD_PROMPT


@case("点名的 IMG- 不存在，LK-05", ["LK-05"])
def _lock_points_missing():
    visual = GOOD_VISUAL.replace("IMG-LOOK-JIANGCHEN-DRESS）", "IMG-NOPE）")
    return visual, GOOD_PROMPT


@case("条目 ID 重复，ID-02", ["ID-02"])
def _duplicate_entry():
    visual = GOOD_VISUAL + "\n### CHAR-JIANGCHEN · 江晨\n- 识别锚点：重复。\n"
    return visual, GOOD_PROMPT


@case("同一专名两个 ID，ID-03", ["ID-03"])
def _duplicate_name():
    visual = GOOD_VISUAL + "\n### CHAR-JIANGCHEN-OLD · 江晨\n- 识别锚点：旧条目。\n"
    return visual, GOOD_PROMPT


@case("单字母 ID 合法，不误报 ID-03", [])
def _short_id():
    visual = GOOD_VISUAL.replace("CHAR-JIANGCHEN", "CHAR-A").replace(
        "LOOK-JIANGCHEN-DRESS", "LOOK-A"
    )
    prompt = GOOD_PROMPT.replace("LOOK-JIANGCHEN-DRESS", "LOOK-A").replace(
        "IMG-LOOK-JIANGCHEN-DRESS", "IMG-LOOK-A"
    )
    return visual, prompt


@case("提示词缺字段，IM-01", ["IM-01"])
def _missing_field():
    prompt = GOOD_PROMPT.replace("- 视图：16:9 三视图\n", "")
    return GOOD_VISUAL, prompt


@case("资产指向不存在的条目，IM-02", ["IM-02"])
def _dangling_asset():
    # 只改 `资产：` 那一行；若做全局替换会连锁里的 `生图提示词项：IMG-…` 一起改掉，
    # 那就变成用例自己造出来的 LK-05，测不到 IM-02。
    prompt = GOOD_PROMPT.replace("- 资产：LOOK-JIANGCHEN-DRESS", "- 资产：LOOK-MISSING")
    return GOOD_VISUAL, prompt


@case("资产指向未决条目，IM-03", ["IM-03"])
def _unresolved_asset():
    visual = GOOD_VISUAL.replace(
        "- 识别锚点：松枝绿翻领制服，铜扣五粒。",
        "- 识别锚点：尚未定。\n- 未决：等创作者确认。",
    )
    return visual, GOOD_PROMPT


@case("没有可复制正文，IM-04（连带 LK-03：锁面无处在场）", ["IM-04", "LK-03"])
def _no_body():
    prompt = GOOD_PROMPT.replace("### 可复制提示词", "### 说明")
    return GOOD_VISUAL, prompt


@case("正文残留引擎语法，IM-05", ["IM-05"])
def _engine_syntax():
    prompt = GOOD_PROMPT.replace("棚拍柔光。", "棚拍柔光。--ar 16:9")
    return GOOD_VISUAL, prompt


@case("正文残留占位符，IM-06", ["IM-06"])
def _placeholder():
    prompt = GOOD_PROMPT.replace("棚拍柔光。", "棚拍柔光，待补背景色。")
    return GOOD_VISUAL, prompt


@case("正文混入路径，IM-07", ["IM-07"])
def _leak():
    prompt = GOOD_PROMPT.replace("棚拍柔光。", "棚拍柔光，见 视觉设定.md。")
    return GOOD_VISUAL, prompt


@case("REF 语法残缺，REF-01", ["REF-01"])
def _ref_syntax():
    prompt = GOOD_PROMPT.replace(
        "- 参考：无外部参考",
        "- 参考：REF-A（顺序：1）· assets/a.png《甲图》（用途：身份）、REF-B 随便写",
    )
    return GOOD_VISUAL, prompt


@case("REF 用途不在词表，REF-02", ["REF-02"])
def _ref_use():
    prompt = GOOD_PROMPT.replace(
        "- 参考：无外部参考",
        "- 参考：REF-A（顺序：1）· assets/a.png《甲图》（用途：脸；控制：五官；不得控制：服装）",
    )
    return GOOD_VISUAL, prompt


@case("资产板用起始帧，REF-03", ["REF-03"])
def _ref_forbidden():
    prompt = GOOD_PROMPT.replace(
        "- 参考：无外部参考",
        "- 参考：REF-A（顺序：1）· assets/a.png《甲图》（用途：起始帧；控制：构图；不得控制：服装）",
    )
    return GOOD_VISUAL, prompt


@case("槽位重复，REF-04", ["REF-04"])
def _ref_dup():
    prompt = GOOD_PROMPT.replace(
        "- 参考：无外部参考",
        "- 参考：REF-A（顺序：1）· assets/a.png《甲图》（用途：身份；控制：脸；不得控制：服装）、"
        "REF-A（顺序：2）· assets/b.png《乙图》（用途：风格；控制：色彩；不得控制：身份）",
    )
    return GOOD_VISUAL, prompt


@case("文字政策没写成两层，TXT-01", ["TXT-01"])
def _policy_shape():
    prompt = GOOD_PROMPT.replace("`no_readable_text` → `blank`", "不出现文字")
    return GOOD_VISUAL, prompt


@case("映射不被允许，TXT-02", ["TXT-02"])
def _policy_mismatch():
    prompt = GOOD_PROMPT.replace("`no_readable_text` → `blank`", "`graphic_only` → `readable`")
    return GOOD_VISUAL, prompt


@case("symbolic 承担禁字但没写不可读，TXT-02", ["TXT-02"])
def _policy_symbolic():
    prompt = GOOD_PROMPT.replace(
        "`no_readable_text` → `blank`", "`no_readable_text` → `symbolic`"
    ).replace("纯净中灰背景", "招牌为抽象图形，纯净中灰背景")
    return GOOD_VISUAL, prompt


@case("要求 readable 却全局禁字，TXT-03", ["TXT-03"])
def _policy_conflict():
    prompt = GOOD_PROMPT.replace(
        "`no_readable_text` → `blank`", "`exact_readable` → `readable`"
    ).replace("纯净中灰背景，棚拍柔光。", "纯净中灰背景，棚拍柔光，不要出现任何文字。")
    return GOOD_VISUAL, prompt


@case("两份文件都没有，DOC-01", ["DOC-01"])
def _no_docs():
    return None, None


@case("只有视觉设定且声明 partial，DOC-01 降为提示", [], ["DOC-01"], partial=True)
def _partial_ok():
    return GOOD_VISUAL, None


@case("只有视觉设定却没声明 partial，DOC-01", ["DOC-01"])
def _partial_missing():
    return GOOD_VISUAL, None


def main() -> int:
    failed = 0
    for name, fn, want_errors, want_notes, partial in CASES:
        visual, prompt = fn()
        got_errors = codes(visual, prompt, partial)
        got_notes = notes(visual, prompt, partial)
        ok = set(got_errors) == want_errors and set(got_notes) == want_notes
        if not ok:
            failed += 1
            print(f"FAIL  {name}")
            print(f"      期望错误 {sorted(want_errors) or '无'}，实得 {sorted(set(got_errors)) or '无'}")
            print(f"      期望提示 {sorted(want_notes) or '无'}，实得 {sorted(set(got_notes)) or '无'}")
        else:
            print(f"ok    {name}")
    print(f"\n{len(CASES) - failed}/{len(CASES)} 通过")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
