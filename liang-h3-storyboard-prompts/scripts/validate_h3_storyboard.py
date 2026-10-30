#!/usr/bin/env python3
"""Structure-check a H3 参考生分镜 markdown file.

Copied from short-drama-h3-storyboard and extended for the bilingual delivery
rule of liang-h3-storyboard-prompts: after the English H3 prompt code block,
a segment-by-segment 中文对照 section is mandatory.
"""
from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

UNIT_RE = re.compile(r"^##\s+(H3-UNIT-[A-Za-z0-9_-]+)\b.*$", re.MULTILINE)
REQUIRED_FIELDS = (
    "时长",
    "模式",
    "来源",
    "参考图",
    "主体映射",
    "声线映射",
    "空间锁",
    "口型纪律",
    "状态链",
    "声音",
)
REFERENCE_SECTIONS = (
    "subject_definitions",
    "summary",
    "retention_analysis",
    "detailed_description",
    "overall_soundscape",
    "non_diegetic_music",
)
BASE_SECTIONS = (
    "integrated_multimodal_description",
    "overall_soundscape",
    "non_diegetic_music",
)
MODES = {"reference", "first_frame", "first_last_frame", "base"}
RETENTION_TERMS = (
    "fully_preserved",
    "partially_preserved",
    "attribute_transfer",
    "weak_reference",
)


@dataclass(frozen=True)
class Issue:
    unit: str
    message: str


def field_value(block: str, label: str) -> str | None:
    pattern = re.compile(
        rf"^-\s*{re.escape(label)}\s*[：:]\s*(.*?)\s*$",
        re.MULTILINE,
    )
    match = pattern.search(block)
    return match.group(1).strip() if match else None


def fenced_prompt(block: str) -> str | None:
    heading = re.search(r"^###\s+H3 提示词.*$", block, re.MULTILINE)
    if heading is None:
        return None
    match = re.search(
        r"```(?:text|markdown)?\s*\n(.*?)\n```",
        block[heading.end() :],
        re.DOTALL,
    )
    return match.group(1).strip() if match else None


def parse_units(text: str) -> list[tuple[str, str]]:
    matches = list(UNIT_RE.finditer(text))
    units: list[tuple[str, str]] = []
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        units.append((match.group(1), text[start:end]))
    return units


def parse_duration(value: str | None) -> float | None:
    if value is None:
        return None
    match = re.search(r"(\d+(?:\.\d+)?)", value)
    return float(match.group(1)) if match else None


def has_section(prompt: str, section: str) -> bool:
    return re.search(rf"^{re.escape(section)}\s*:", prompt, re.MULTILINE) is not None


def validate_subject_picture_labels(prompt: str, unit: str) -> list[Issue]:
    issues: list[Issue] = []
    definitions_match = re.search(
        r"^subject_definitions[ \t]*:[ \t]*(.*)$",
        prompt,
        re.MULTILINE,
    )
    if definitions_match is None:
        return issues
    start = definitions_match.end()
    next_section = re.search(r"^(?:summary|retention_analysis)\s*:", prompt[start:], re.MULTILINE)
    definitions = (
        prompt[start:start + next_section.start()] if next_section else prompt[start:]
    )

    subject_tags = {f"<Subject {value}>" for value in re.findall(r"<Subject\s+(\d+)>", prompt)}
    missing_subjects = sorted(tag for tag in subject_tags if tag not in definitions)
    if missing_subjects:
        issues.append(
            Issue(
                unit,
                "subject_definitions 缺少主体定义：" + "、".join(missing_subjects),
            )
        )

    picture_tags = {f"<Picture {value}>" for value in re.findall(r"<Picture\s+(\d+)>", prompt)}
    missing_pictures = sorted(tag for tag in picture_tags if tag not in definitions)
    if missing_pictures:
        issues.append(
            Issue(
                unit,
                "subject_definitions 缺少图片角色定义：" + "、".join(missing_pictures),
            )
        )
    return issues


def validate_speaker_mapping(prompt: str, voice_mapping: str | None, unit: str) -> list[Issue]:
    if not voice_mapping:
        return []
    issues: list[Issue] = []
    speaker_ids = sorted(set(re.findall(r"\(S(\d+)\)", prompt)), key=int)
    for speaker_id in speaker_ids:
        if f"S{speaker_id}" not in voice_mapping:
            issues.append(
                Issue(unit, f"正文使用 S{speaker_id}，但声线映射未登记")
            )
    return issues


def validate_dialogue_tags(prompt: str, unit: str) -> list[Issue]:
    issues: list[Issue] = []
    opening_count = prompt.count("<d>")
    closing_count = prompt.count("</d>")
    if opening_count != closing_count:
        issues.append(Issue(unit, "<d> 与 </d> 数量不一致"))

    matches = re.findall(r"<d>\[Chinese\](.*?)</d>", prompt, re.DOTALL)
    if len(matches) != closing_count:
        issues.append(Issue(unit, "台词必须使用 <d>[Chinese]逐字台词</d>"))
    for dialogue in matches:
        if not dialogue.strip():
            issues.append(Issue(unit, "存在空的中文对白标签"))
    return issues


def validate_shot_timestamps(prompt: str, unit: str) -> list[Issue]:
    """At MM:SS.mmm 是可选写法：写就要严格递增，不写不算错。"""
    issues: list[Issue] = []
    shot_matches = list(re.finditer(r"\[Shot\s+(\d+)\]", prompt))
    timestamps: list[float] = []
    for index, match in enumerate(shot_matches):
        shot_number = int(match.group(1))
        start = match.end()
        end = shot_matches[index + 1].start() if index + 1 < len(shot_matches) else len(prompt)
        segment = prompt[start:end]
        timestamp = re.search(r"\bAt\s+(\d{2}):(\d{2})(?:\.(\d{1,3}))?", segment)
        if timestamp is not None:
            minutes = int(timestamp.group(1))
            seconds = int(timestamp.group(2))
            fraction = timestamp.group(3) or "0"
            fraction_value = float(f"0.{fraction}")
            timestamps.append(minutes * 60 + seconds + fraction_value)
    if timestamps and timestamps != sorted(timestamps):
        issues.append(Issue(unit, "切镜时间戳没有严格递增（写了 At 就必须严格递增；也可全不写）"))
    return issues


def has_chinese_contrast(block: str) -> bool:
    """Bilingual delivery rule: a 中文对照 section must live AFTER the prompt."""
    contrast = re.search(r"^###+\s*中文对照", block, re.MULTILINE)
    if contrast is None:
        return False
    prompt_heading = re.search(r"^###\s+H3 提示词", block, re.MULTILINE)
    if prompt_heading is None:
        return True
    return contrast.start() > prompt_heading.start()


def validate_unit(unit: str, block: str) -> list[Issue]:
    issues: list[Issue] = []
    values = {label: field_value(block, label) for label in REQUIRED_FIELDS}
    for label, value in values.items():
        if not value:
            issues.append(Issue(unit, f"缺少字段：{label}"))

    duration = parse_duration(values["时长"])
    if duration is None:
        issues.append(Issue(unit, "无法解析时长"))
    elif duration < 4 or duration > 15:
        issues.append(Issue(unit, f"时长 {duration:g} 秒不在 H3 的 4–15 秒范围"))

    mode = (values["模式"] or "").strip().lower()
    if mode not in MODES:
        issues.append(Issue(unit, f"非法模式：{mode or '空'}"))
    if mode == "reference" and values["参考图"] in {None, "", "无"}:
        issues.append(Issue(unit, "reference 模式必须登记参考图"))

    prompt = fenced_prompt(block)
    if prompt is None:
        issues.append(Issue(unit, "缺少 ### H3 提示词 代码块"))
        return issues

    required_sections = REFERENCE_SECTIONS if mode == "reference" else BASE_SECTIONS
    for section in required_sections:
        if not has_section(prompt, section):
            issues.append(Issue(unit, f"H3 正文缺少字段：{section}"))

    description_key = (
        "detailed_description" if mode == "reference" else "integrated_multimodal_description"
    )
    if not re.search(r"\[Shot\s+1\]", prompt):
        issues.append(Issue(unit, "H3 正文缺少 [Shot 1]"))

    if mode == "reference":
        retention_match = re.search(
            r"^retention_analysis\s*:\s*(.*)$",
            prompt,
            re.MULTILINE,
        )
        retention_text = retention_match.group(1) if retention_match else ""
        if retention_text and not any(term in retention_text for term in RETENTION_TERMS):
            issues.append(Issue(unit, "retention_analysis 未写保留强度"))

    issues.extend(validate_subject_picture_labels(prompt, unit))
    issues.extend(validate_speaker_mapping(prompt, values["声线映射"], unit))
    issues.extend(validate_dialogue_tags(prompt, unit))
    issues.extend(validate_shot_timestamps(prompt, unit))

    if description_key not in prompt:
        issues.append(Issue(unit, f"H3 正文缺少字段：{description_key}"))

    if not has_chinese_contrast(block):
        issues.append(Issue(unit, "缺少逐段中文对照：### 中文对照 必须紧跟 H3 提示词代码块之后"))
    return issues


def validate_file(path: Path) -> list[Issue]:
    text = path.read_text(encoding="utf-8-sig")
    units = parse_units(text)
    if not units:
        return [Issue("FILE", "没有找到 H3-UNIT-* 二级标题")]

    issues: list[Issue] = []
    for unit, block in units:
        issues.extend(validate_unit(unit, block))
    return issues


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate a short-drama H3 storyboard markdown file.")
    parser.add_argument("path", type=Path, help="Path to H3分镜.md")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if not args.path.is_file():
        print(f"FILE: 文件不存在：{args.path}")
        return 1

    issues = validate_file(args.path)
    if not issues:
        print(f"OK: {args.path}")
        return 0

    for issue in issues:
        print(f"{issue.unit}: {issue.message}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())