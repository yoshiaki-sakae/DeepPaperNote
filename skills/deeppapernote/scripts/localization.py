#!/usr/bin/env python3
"""Language schemas shared by DeepPaperNote contracts and validators."""

from __future__ import annotations

import os
from copy import deepcopy
from typing import Any

DEFAULT_OUTPUT_LANGUAGE = "zh-CN"
SUPPORTED_OUTPUT_LANGUAGES = ("zh-CN", "en", "ja")
_ALIASES = {
    "zh": "zh-CN", "zh-cn": "zh-CN", "zh_cn": "zh-CN", "chinese": "zh-CN",
    "en": "en", "en-us": "en", "en_us": "en", "english": "en",
    "ja": "ja", "ja-jp": "ja", "ja_jp": "ja", "japanese": "ja", "日本語": "ja",
}
_SCHEMAS: dict[str, dict[str, Any]] = {
    "zh-CN": {
        "sections": {"core_information": "核心信息", "abstract": "原文摘要翻译", "contributions": "创新点", "one_sentence_summary": "一句话总结", "research_questions": "研究问题", "data_and_task": "数据与任务定义", "method": "方法主线", "key_results": "关键结果", "deep_analysis": "深度分析", "limitations": "局限", "my_notes": "我的笔记", "references": "引用"},
        "core_info_fields": ("标题", "标题翻译", "作者", "机构", "发表时间", "发表渠道", "DOI", "arXiv", "论文链接", "代码 / 项目", "数据 / 资源", "论文类型"),
        "core_info_aliases": {},
        "figure_labels": {"location": "建议位置：", "reason": "放置原因：", "status": "当前状态：", "original_caption": "论文原图编号："},
        "mechanism_flow": "机制流程",
    },
    "en": {
        "sections": {"core_information": "Core Information", "abstract": "Abstract", "contributions": "Contributions", "one_sentence_summary": "One-Sentence Summary", "research_questions": "Research Question", "data_and_task": "Data and Task Definition", "method": "Method", "key_results": "Key Results", "deep_analysis": "Deep Analysis", "limitations": "Limitations", "my_notes": "Research Notes", "references": "References"},
        "core_info_fields": ("Title", "Translated title", "Authors", "Institutions", "Publication date", "Venue", "DOI", "arXiv", "Paper link", "Code / Project", "Data / Resources", "Paper type"),
        "core_info_aliases": {},
        "figure_labels": {"location": "Suggested location:", "reason": "Why it matters:", "status": "Current status:", "original_caption": "Original paper item:"},
        "mechanism_flow": "Mechanism Flow",
        "abstract_contract": {
            "source": "source_abstract",
            "requirement": "faithful_rendering_in_output_language",
            "forbidden_additions": [
                "later_contribution_claims",
                "later_result_interpretation",
                "hindsight_judgment",
            ],
        },
    },
    "ja": {
        "sections": {"core_information": "基本情報", "abstract": "要旨の翻訳", "contributions": "新規性", "one_sentence_summary": "一言まとめ", "research_questions": "研究課題", "data_and_task": "データとタスク定義", "method": "手法の骨子", "key_results": "主要な結果", "deep_analysis": "深掘り分析", "limitations": "限界", "my_notes": "私のメモ", "references": "参考文献"},
        "core_info_fields": ("タイトル", "タイトル訳", "著者", "所属", "発表時期", "発表媒体", "DOI", "arXiv", "論文リンク", "コード / プロジェクト", "データ / リソース", "論文タイプ"),
        "core_info_aliases": {},
        "figure_labels": {"location": "推奨位置：", "reason": "配置理由：", "status": "現在の状態：", "original_caption": "論文原図番号："},
        "mechanism_flow": "機構フロー",
        "abstract_contract": {
            "source": "source_abstract",
            "requirement": "faithful_rendering_in_output_language",
            "forbidden_additions": [
                "later_contribution_claims",
                "later_result_interpretation",
                "hindsight_judgment",
            ],
        },
    },
}

def normalize_output_language(value: str | None = None) -> str:
    raw = (value if value is not None else os.environ.get("DEEPPAPERNOTE_OUTPUT_LANGUAGE", "")).strip()
    if not raw:
        return DEFAULT_OUTPUT_LANGUAGE
    normalized = _ALIASES.get(raw.lower(), raw)
    if normalized not in SUPPORTED_OUTPUT_LANGUAGES:
        raise ValueError(f"Unsupported DeepPaperNote output language: {raw}. Choose one of: {', '.join(SUPPORTED_OUTPUT_LANGUAGES)}.")
    return normalized


def require_artifact_output_language(
    artifact: dict[str, Any],
    artifact_name: str,
    expected: str,
) -> str:
    language = artifact.get("output_language")
    if language not in SUPPORTED_OUTPUT_LANGUAGES:
        raise ValueError(
            f"{artifact_name} requires output_language with one of: "
            f"{', '.join(SUPPORTED_OUTPUT_LANGUAGES)}."
        )
    resolved = normalize_output_language(expected)
    if language != resolved:
        raise ValueError(
            f"{artifact_name} output_language {language} does not match "
            f"resolved output_language {resolved}."
        )
    return str(language)

def note_schema(language: str | None = None) -> dict[str, Any]:
    return deepcopy(_SCHEMAS[normalize_output_language(language)])

def required_sections(language: str | None = None) -> tuple[str, ...]:
    return tuple(note_schema(language)["sections"].values())
