#!/usr/bin/env python3
"""机械校验《视觉设定.md》与《资产生图提示词.md》的结构一致性。

只核对能被字符串证明的东西：ID 结构、锁语法、锁面是否逐字出现在被点名的
提示词正文里、参考槽位语法与用途词表、文字政策两层的显式冲突、占位符与
引擎专用语法残留。判断该不该上这把锁、锚点写得准不准、资产拆得对不对，
仍属于创作者与审查的工作；本脚本通过不等于资产正确。
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import NamedTuple

MINIMUM_PYTHON = (3, 9)
if sys.version_info < MINIMUM_PYTHON:
    raise SystemExit("check_assets.py requires Python 3.9 or newer")

VISUAL_DOC = "视觉设定.md"
PROMPT_DOC = "资产生图提示词.md"
LEGACY_PROMPT_DOC = "图片提示词.md"

ASSET_PREFIXES = ("CHAR", "LOOK", "LOC", "VIEW", "PROP", "PSTATE", "CREA")
REQUIRED_FIELDS = ("资产", "用途", "视图", "文字政策", "参考")

SOURCE_POLICIES = ("exact_readable", "graphic_only", "no_readable_text", "pending_creator_text")
PRESENT_METHODS = ("readable", "symbolic", "blank", "postproduction")

#: 资产来源政策 -> 允许的呈现方法（见 references/prompt-recipe.md 的映射表）
POLICY_MATRIX = {
    "exact_readable": ("readable", "postproduction"),
    "graphic_only": ("symbolic",),
    "no_readable_text": ("blank", "symbolic"),  # symbolic 须在正文显式写"不可读"
    "pending_creator_text": ("postproduction",),  # readable 被阻断，须先回资产侧补文字
}

REF_USES = ("身份", "造型状态", "地理", "构图", "尺度", "效果", "起始帧", "结束帧", "风格")
ASSET_BOARD_FORBIDDEN_USES = ("起始帧", "结束帧")

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*\S)\s*$")
#: 单字母 ID（`CHAR-A`、`LOC-B`）合法，所以后缀下限是 1 个字符，但不能以 `-`/`_` 收尾。
ID_RE = re.compile(
    r"(?<![A-Za-z0-9_-])"
    r"(CHAR|LOOK|LOC|VIEW|PROP|PSTATE|CREA|LOCK|IMG|REF|SHOT|MOTION)"
    r"-[A-Za-z0-9](?:[A-Za-z0-9_-]*[A-Za-z0-9])?"
)

LOCK_LINE_RE = re.compile(r"^\s*[-*+]\s*连续性锁\s*[：:]\s*(.+?)\s*$")
LOCK_FULL_RE = re.compile(
    r"^(?P<lock>LOCK-[A-Za-z0-9][A-Za-z0-9_-]*)\s*"
    r"《(?P<name>[^》]*)》\s*"
    r"[（(](?P<scope>[^（）()]*)[）)]\s*"
    r"(?:[·・]\s*锁面\s*[：:]\s*(?P<surface>.+?))?\s*$"
)
CAMERA_WORDS = ("入画", "全集")
SHOT_TOKEN_RE = re.compile(r"SHOT-[A-Za-z0-9][A-Za-z0-9_-]*")

REF_FULL_RE = re.compile(
    r"REF-(?P<slot>[A-Za-z0-9][A-Za-z0-9_-]*)\s*"
    r"[（(]\s*顺序\s*[：:]\s*(?P<order>\d+)\s*[）)]\s*"
    r"[·・]\s*(?P<path>[^《\n]+?)\s*"
    r"《(?P<name>[^》]*)》\s*"
    r"[（(]\s*用途\s*[：:]\s*(?P<use>[^；;）)]*)"
    r"(?:[；;]\s*控制\s*[：:]\s*(?P<control>[^；;）)]*))?"
    r"(?:[；;]\s*不得控制\s*[：:]\s*(?P<deny>[^；;）)]*))?\s*[）)]"
)
REF_TOKEN_RE = re.compile(r"(?<![A-Za-z0-9_-])REF-")

POLICY_VALUE_RE = re.compile(
    r"`?([a-z][a-z0-9_]*[a-z])`?\s*(?:→|->|⇒|=>)\s*`?([a-z][a-z0-9_]*[a-z])`?"
)
ILLEGIBLE_RE = re.compile(r"不可读|无法辨读|不要求可辨字义|illegible", re.IGNORECASE)
TEXT_BAN_RE = re.compile(
    r"(?:不要|不能出现|不出现|避免)(?:出现)?(?:任何)?(?:可读)?文字"
    r"|no\s+(?:readable\s+)?text|without\s+(?:any\s+)?text",
    re.IGNORECASE,
)

ENGINE_SYNTAX_RES = (
    # 参数常紧跟中文标点，不一定要有空格
    (re.compile(r"(?:^|[\s。，、；：！？,;:])--[a-zA-Z]{1,12}\b"), "--ar 一类参数"),
    (re.compile(r"\(\s*[^()\n]{1,60}:\s*\d+(?:\.\d+)?\s*\)"), "(x:1.2) 一类权重"),
    (re.compile(r"::\s*\d+"), "cat::2 一类权重"),
)
PLACEHOLDER_RE = re.compile(
    r"TODO|FIXME|TBD|xxx+|XXX+|待填|待补|待定文案|\{\{|\}\}|<待[^>]*>|【待[^】]*】"
)
INTERNAL_LEAK_RE = re.compile(
    r"(?<![A-Za-z0-9_-])(?:IMG|LOCK|SHOT|MOTION)-[A-Za-z0-9]"
    r"|\.md\b|\.jsonl?\b|\.png\b|\.jpe?g\b"
    r"|请模型务必|根据上图保持一致|参考上文"
)
UNRESOLVED_RE = re.compile(r"未决|unresolved|待创作者决定")
UNRESOLVED_NONE_RE = re.compile(r"未决\s*[：:]\s*(?:无|none)|无未决")

NEG_ZH = ("不要", "不能", "没有", "避免", "不出现", "禁止", "禁用", "排除", "去掉", "删除")
NEG_EN = re.compile(r"(?:^|[^a-z])(?:no|not|without|avoid|never|none|exclude|remove)(?![a-z])")


class Finding(NamedTuple):
    code: str
    location: str
    detail: str
    severity: str = "error"


class Block(NamedTuple):
    level: int
    title: str
    line: int
    body: list  # list[tuple[int, str]]

    @property
    def text(self) -> str:
        return "\n".join(text for _, text in self.body)

    @property
    def first_id(self) -> str:
        found = [match.group(0) for match in ID_RE.finditer(self.title)]
        return found[0] if found else ""


# ---------------------------------------------------------------------------
# 基础工具
# ---------------------------------------------------------------------------


def split_blocks(text: str) -> list:
    blocks = []
    current = None
    for index, raw in enumerate(text.splitlines(), start=1):
        match = HEADING_RE.match(raw)
        if match:
            if current is not None:
                blocks.append(current)
            current = Block(len(match.group(1)), match.group(2), index, [])
        elif current is not None:
            current.body.append((index, raw))
    if current is not None:
        blocks.append(current)
    return blocks


def field_value(block: Block, name: str):
    """返回块内 ``- 名称：值`` 的值与行号；找不到返回 ``(None, None)``。"""
    pattern = re.compile(r"^\s*[-*+]\s*(?:\*\*)?%s(?:\*\*)?\s*[：:]\s*(.*)$" % re.escape(name))
    for line_no, text in block.body:
        match = pattern.match(text)
        if match:
            return match.group(1).strip(), line_no
    return None, None


def _bounded(hay: str, pos: int, needle: str) -> bool:
    """锁面首尾是字母数字时，粘在别的词上不算命中。"""
    if needle and needle[0].isascii() and needle[0].isalnum():
        if pos > 0 and (hay[pos - 1].isalnum() or hay[pos - 1] in "-_"):
            return False
    if needle and needle[-1].isascii() and needle[-1].isalnum():
        end = pos + len(needle)
        if end < len(hay) and (hay[end].isalnum() or hay[end] in "-_"):
            return False
    return True


def _negated(hay: str, pos: int) -> bool:
    boundary = -1
    for marker in ("。", "；", ";", ".", "\n", "|"):
        boundary = max(boundary, hay.rfind(marker, 0, pos))
    segment = hay[boundary + 1 : pos][-60:]
    if any(word in segment for word in NEG_ZH):
        return True
    return bool(NEG_EN.search(segment))


def surface_state(text: str, surface: str) -> str:
    """锁面在正文里的状态：``present`` / ``negated`` / ``absent``。"""
    hay = " ".join(text.split()).lower()
    needle = " ".join(surface.split()).lower()
    if not needle:
        return "absent"
    negated_only = False
    start = 0
    while True:
        pos = hay.find(needle, start)
        if pos < 0:
            break
        if _bounded(hay, pos, needle):
            if _negated(hay, pos):
                negated_only = True
            else:
                return "present"
        start = pos + 1
    return "negated" if negated_only else "absent"


def copyable_text(blocks: list, index: int) -> tuple:
    """取某条目下的 ``可复制提示词`` 段落正文，返回 (正文, 段落标题行)。"""
    level = blocks[index].level
    for block in blocks[index + 1 :]:
        if block.level <= level:
            return "", None
        if "可复制" in block.title:
            quoted = [
                text.strip()
                for _, text in block.body
                if text.strip().startswith(">")
            ]
            return "\n".join(quoted), block.line
    return "", None


# ---------------------------------------------------------------------------
# 视觉设定
# ---------------------------------------------------------------------------


def collect_entries(visual_blocks: list) -> tuple:
    entries = {}
    by_name = {}
    findings = []
    for block in visual_blocks:
        if block.level < 3:
            continue
        entry_id = block.first_id
        if entry_id:
            if entry_id in entries:
                findings.append(
                    Finding("ID-02", f"{VISUAL_DOC}:{block.line}", f"重复条目 ID {entry_id}")
                )
                continue
            entries[entry_id] = block
        if "·" in block.title:
            name = block.title.split("·", 1)[1].strip()
            if name:
                by_name.setdefault(name, set()).add(entry_id or f"<无 ID>@{block.line}")
    for name, owners in by_name.items():
        if len(owners) > 1:
            findings.append(
                Finding(
                    "ID-03",
                    VISUAL_DOC,
                    f"专名《{name}》对应多个 ID：{'、'.join(sorted(owners))}",
                )
            )
    return entries, findings


def is_unresolved(block: Block) -> bool:
    if UNRESOLVED_NONE_RE.search(block.text):
        return False
    return bool(UNRESOLVED_RE.search(block.text))


def parse_scope(scope: str) -> tuple:
    """拆 `镜头：…；生图提示词项：…`，返回 (镜头列表, 提示词项列表, 错误说明)。"""
    shots = []
    prompts = []
    error = ""
    for part in re.split(r"[；;]", scope):
        part = part.strip()
        if not part:
            continue
        key, sep, value = part.partition("：")
        if not sep:
            key, sep, value = part.partition(":")
        key, value = key.strip(), value.strip()
        if key == "镜头":
            if value in CAMERA_WORDS:
                shots.append(value)
                continue
            items = [token.strip() for token in re.split(r"[、,]", value) if token.strip()]
            # 混写（`SHOT-001、入画`）留给下面统一报错，这里只挑真正认不出的词。
            bad = [
                token
                for token in items
                if token not in CAMERA_WORDS and not SHOT_TOKEN_RE.fullmatch(token)
            ]
            if bad:
                error = f"镜头范围含无法识别的值：{'、'.join(bad)}"
            else:
                shots.extend(items)
        elif key == "生图提示词项":
            for token in re.split(r"[、,]", value):
                token = token.strip()
                if not token:
                    continue
                if not re.fullmatch(r"IMG-[A-Za-z0-9][A-Za-z0-9_-]*", token):
                    error = f"生图提示词项含非 IMG- 值：{token}"
                else:
                    prompts.append(token)
        else:
            error = f"括号内出现未知键 `{key}`"

    camera_like = [item for item in shots if item in CAMERA_WORDS]
    shot_like = [item for item in shots if item not in CAMERA_WORDS]
    if not error:
        if not shots:
            error = "括号内缺 `镜头：`"
        elif len(camera_like) > 1:
            error = "`入画` 与 `全集` 不能同时出现"
        elif camera_like and shot_like:
            error = "`入画`/`全集` 不能与 `SHOT-...` 列表混写"
    return shots, prompts, error


def inherited_source(visual_blocks: list, index: int) -> str:
    """本条目没有 `来源：` 时，向上找最近一层带来源的资产条目。"""
    own = field_value(visual_blocks[index], "来源")[0]
    if own:
        return own
    level = visual_blocks[index].level
    for block in reversed(visual_blocks[:index]):
        if block.level < level:
            if block.first_id:
                return field_value(block, "来源")[0] or ""
            level = block.level
    return ""


def check_locks(visual_blocks, entries, prompts, findings, skip_prompt_checks):
    """``skip_prompt_checks`` 为真时（partial，或提示词文件尚未产出）不核对 IMG- 一侧。"""
    seen = {}
    for index, block in enumerate(visual_blocks):
        for line_no, text in block.body:
            match = LOCK_LINE_RE.match(text)
            if not match:
                continue
            location = f"{VISUAL_DOC}:{line_no}"
            parsed = LOCK_FULL_RE.match(match.group(1))
            if not parsed:
                findings.append(
                    Finding(
                        "LK-01",
                        location,
                        "锁语法不完整：需 `LOCK-ID《中文名》（镜头：…；生图提示词项：…）· 锁面：…`",
                    )
                )
                continue
            lock_id = parsed.group("lock")
            name = parsed.group("name").strip()
            surface = (parsed.group("surface") or "").strip()

            if lock_id in seen:
                findings.append(
                    Finding("LK-02", location, f"锁 ID {lock_id} 已在第 {seen[lock_id]} 行声明")
                )
            else:
                seen[lock_id] = line_no
            if not re.search(r"[一-鿿]", name):
                findings.append(Finding("LK-01", location, "锁的《中文名》必须含中文"))
            if not surface:
                findings.append(Finding("LK-01", location, f"{lock_id} 缺少 `锁面：`"))

            shots, prompt_ids, error = parse_scope(parsed.group("scope"))
            if error:
                findings.append(Finding("LK-06", location, f"{lock_id} {error}"))
            if shots == ["入画"] and not inherited_source(visual_blocks, index):
                findings.append(
                    Finding(
                        "LK-06",
                        location,
                        f"{lock_id} 写 `镜头：入画`，但所属资产条目及其上层都没有 `来源：` 可展开",
                        "note",
                    )
                )

            for prompt_id in prompt_ids:
                if skip_prompt_checks:
                    continue
                if prompt_id not in prompts:
                    findings.append(
                        Finding("LK-05", location, f"{lock_id} 点名的 {prompt_id} 不在提示词文件里")
                    )
                    continue
                body = prompts[prompt_id]["copyable"]
                if not body:
                    findings.append(
                        Finding("LK-03", location, f"{lock_id} 点名的 {prompt_id} 没有可复制正文")
                    )
                    continue
                state = surface_state(body, surface)
                if state == "absent":
                    findings.append(
                        Finding(
                            "LK-03",
                            location,
                            f"锁面 `{surface}` 未逐字出现在 {prompt_id} 的可复制正文里",
                        )
                    )
                elif state == "negated":
                    findings.append(
                        Finding(
                            "LK-04",
                            location,
                            f"锁面 `{surface}` 在 {prompt_id} 只出现在负面提示词里，不构成在场证据",
                        )
                    )


# ---------------------------------------------------------------------------
# 资产生图提示词
# ---------------------------------------------------------------------------


def collect_prompts(prompt_blocks: list, findings: list) -> dict:
    prompts = {}
    for index, block in enumerate(prompt_blocks):
        if block.level < 2 or "IMG-" not in block.title:
            continue
        prompt_id = block.first_id
        if not prompt_id:
            continue
        if prompt_id in prompts:
            findings.append(
                Finding("ID-02", f"{PROMPT_DOC}:{block.line}", f"重复提示词 ID {prompt_id}")
            )
            continue
        body, body_line = copyable_text(prompt_blocks, index)
        prompts[prompt_id] = {"block": block, "copyable": body, "copyable_line": body_line}
    return prompts


def check_prompt_entry(prompt_id, record, entries, findings):
    block = record["block"]
    location = f"{PROMPT_DOC}:{block.line}"

    values = {name: field_value(block, name) for name in REQUIRED_FIELDS}
    missing = [name for name, (value, _) in values.items() if value is None]
    if missing:
        findings.append(Finding("IM-01", location, f"{prompt_id} 缺字段：{'、'.join(missing)}"))

    asset_value, asset_line = values["资产"]
    if asset_value:
        found = [m.group(0) for m in ID_RE.finditer(asset_value)]
        targets = [item for item in found if item.startswith(tuple(p + "-" for p in ASSET_PREFIXES))]
        if not targets:
            findings.append(
                Finding(
                    "IM-02",
                    f"{PROMPT_DOC}:{asset_line}",
                    f"{prompt_id} 的 `资产：` 没写出视觉设定里的条目 ID",
                )
            )
        for target in targets:
            if target not in entries:
                findings.append(
                    Finding(
                        "IM-02",
                        f"{PROMPT_DOC}:{asset_line}",
                        f"{prompt_id} 的 `资产：` 指向 {target}，视觉设定里没有这个条目",
                    )
                )
            elif is_unresolved(entries[target]):
                findings.append(
                    Finding(
                        "IM-03",
                        f"{PROMPT_DOC}:{asset_line}",
                        f"{prompt_id} 的 `资产：` 指向未决条目 {target}",
                    )
                )

    ref_value, ref_line = values["参考"]
    if ref_value is not None:
        check_refs(prompt_id, ref_value, ref_line, findings)

    policy_value, policy_line = values["文字政策"]
    method = None
    if policy_value is not None:
        method = check_policy(prompt_id, policy_value, policy_line, record, findings)

    body = record["copyable"]
    if not body:
        findings.append(Finding("IM-04", location, f"{prompt_id} 没有以 `>` 开头的可复制正文"))
        return
    for pattern, label in ENGINE_SYNTAX_RES:
        hit = pattern.search(body)
        if hit:
            # 正则为了锁定前边界会连前面的标点一起吃掉，报错时只留语法本身。
            snippet = hit.group(0).strip(" \t。，、；：！？,;:")
            findings.append(
                Finding(
                    "IM-05",
                    location,
                    f"{prompt_id} 正文含引擎专用语法（{label}）：{snippet}",
                )
            )
    placeholder = PLACEHOLDER_RE.search(body)
    if placeholder:
        findings.append(
            Finding("IM-06", location, f"{prompt_id} 正文含占位符：{placeholder.group(0)}")
        )
    leak = INTERNAL_LEAK_RE.search(body)
    if leak:
        findings.append(
            Finding("IM-07", location, f"{prompt_id} 正文混入内部字段或路径：{leak.group(0)}")
        )
    if method == "readable" and TEXT_BAN_RE.search(body):
        findings.append(
            Finding("TXT-03", location, f"{prompt_id} 要求 readable，正文却全局禁字")
        )


def check_refs(prompt_id, ref_value, ref_line, findings):
    location = f"{PROMPT_DOC}:{ref_line}"
    if ref_value.strip() in ("无外部参考", "无", "无参考"):
        return
    declared = len(REF_TOKEN_RE.findall(ref_value))
    matches = list(REF_FULL_RE.finditer(ref_value))
    if declared != len(matches):
        findings.append(
            Finding(
                "REF-01",
                location,
                f"{prompt_id} 有 {declared} 个 `REF-`，只有 {len(matches)} 个符合"
                " `REF-<槽位>（顺序：<n>）· <路径>《<名>》（用途：…；控制：…；不得控制：…）`",
            )
        )
    slots = set()
    orders = set()
    for match in matches:
        slot = match.group("slot")
        use = match.group("use").strip()
        if slot in slots:
            findings.append(Finding("REF-04", location, f"槽位 REF-{slot} 重复"))
        slots.add(slot)
        order = match.group("order")
        if order in orders:
            findings.append(Finding("REF-04", location, f"参考顺序号 {order} 重复"))
        orders.add(order)
        if use not in REF_USES:
            findings.append(
                Finding(
                    "REF-02",
                    location,
                    f"REF-{slot} 用途 `{use}` 不在封闭词表：{'/'.join(REF_USES)}",
                )
            )
        elif use in ASSET_BOARD_FORBIDDEN_USES:
            findings.append(
                Finding("REF-03", location, f"REF-{slot} 用 `{use}`：资产板不用起始帧/结束帧")
            )


def check_policy(prompt_id, value, line_no, record, findings):
    """核对两层文字政策，返回呈现方法（解析失败返回 ``None``）。"""
    location = f"{PROMPT_DOC}:{line_no}"
    parsed = POLICY_VALUE_RE.search(value)
    if not parsed:
        findings.append(
            Finding("TXT-01", location, f"{prompt_id} 的文字政策须写成 `来源政策` → `呈现方法`")
        )
        return None
    source, method = parsed.group(1), parsed.group(2)
    if source not in SOURCE_POLICIES:
        findings.append(Finding("TXT-01", location, f"{prompt_id} 来源政策 `{source}` 不在词表内"))
        return None
    if method not in PRESENT_METHODS:
        findings.append(Finding("TXT-01", location, f"{prompt_id} 呈现方法 `{method}` 不在词表内"))
        return None
    allowed = POLICY_MATRIX[source]
    if method not in allowed:
        findings.append(
            Finding(
                "TXT-02",
                location,
                f"{prompt_id} 的映射 `{source}` → `{method}` 不被允许（可选：{'/'.join(allowed)}）",
            )
        )
        return method
    if source == "no_readable_text" and method == "symbolic":
        if not ILLEGIBLE_RE.search(record["copyable"] or ""):
            findings.append(
                Finding(
                    "TXT-02",
                    location,
                    f"{prompt_id} 用 symbolic 承担 no_readable_text，正文须显式写明不可读",
                )
            )
    return method


# ---------------------------------------------------------------------------
# 入口
# ---------------------------------------------------------------------------


def validate_documents(visual_text, prompt_text, partial: bool = False) -> list:
    findings = []
    if visual_text is None and prompt_text is None:
        return [Finding("DOC-01", "-", "既没有《视觉设定.md》也没有提示词文件")]

    visual_blocks = split_blocks(visual_text) if visual_text else []
    prompt_blocks = split_blocks(prompt_text) if prompt_text else []

    entries = {}
    if visual_text:
        entries, entry_findings = collect_entries(visual_blocks)
        findings.extend(entry_findings)

    prompts = {}
    if prompt_text:
        prompts = collect_prompts(prompt_blocks, findings)
        for prompt_id, record in prompts.items():
            check_prompt_entry(prompt_id, record, entries, findings)

    if prompt_text is None:
        findings.append(
            Finding(
                "DOC-01",
                "-",
                f"没有 {PROMPT_DOC}（或并入的 {LEGACY_PROMPT_DOC}）",
                "note" if partial else "error",
            )
        )

    if visual_text:
        # 提示词文件整份缺失时，缺文件本身已由 DOC-01 报过，不再让每把锁连带报 LK-05。
        check_locks(visual_blocks, entries, prompts, findings, partial or prompt_text is None)

    return findings


def resolve_inputs(target: Path) -> tuple:
    if target.is_dir():
        visual = target / VISUAL_DOC
        prompt = target / PROMPT_DOC
        if not prompt.exists():
            prompt = target / LEGACY_PROMPT_DOC
        return (
            visual if visual.exists() else None,
            prompt if prompt.exists() else None,
        )
    if target.name == VISUAL_DOC:
        sibling = target.parent / PROMPT_DOC
        if not sibling.exists():
            sibling = target.parent / LEGACY_PROMPT_DOC
        return target, sibling if sibling.exists() else None
    visual = target.parent / VISUAL_DOC
    return (visual if visual.exists() else None), target


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="机械校验视觉设定与资产生图提示词的结构一致性"
    )
    parser.add_argument("target", help="剧集目录，或其中任一份文件")
    parser.add_argument(
        "--partial",
        action="store_true",
        help="只完成视觉设定、提示词文件尚未产出时使用",
    )
    parser.add_argument("--json", action="store_true", help="以 JSON 输出")
    args = parser.parse_args(argv)

    target = Path(args.target)
    if not target.exists():
        print(f"找不到 {target}", file=sys.stderr)
        return 2
    visual_path, prompt_path = resolve_inputs(target)
    visual_text = visual_path.read_text(encoding="utf-8") if visual_path else None
    prompt_text = prompt_path.read_text(encoding="utf-8") if prompt_path else None

    findings = validate_documents(visual_text, prompt_text, args.partial)
    errors = [item for item in findings if item.severity == "error"]

    if args.json:
        print(
            json.dumps(
                {
                    "visual": str(visual_path) if visual_path else None,
                    "prompts": str(prompt_path) if prompt_path else None,
                    "findings": [item._asdict() for item in findings],
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        for item in findings:
            print(f"{item.location}\t{item.code}\t{item.detail}")
        if not findings:
            print("没有发现结构问题。检查器通过不等于资产正确，仍需人工判断。")
        else:
            notes = len(findings) - len(errors)
            print(f"\n共 {len(findings)} 项（错误 {len(errors)}，提示 {notes}）。")

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
