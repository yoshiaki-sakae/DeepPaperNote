"""日本語（ja）出力プロファイルの契約・lint・図表配置を検証する。"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest
from build_synthesis_bundle import compact_writing_contract
from contracts import paper_type_contracts
from lint_grounding import validate_note_plan
from localization import (
    normalize_output_language,
    require_artifact_output_language,
    required_sections,
)
from plan_figures import build_figure_items
from user_configuration import inspect_configuration

LINT_SCRIPT = Path(__file__).resolve().parents[1] / "skills/deeppapernote/scripts/lint_note.py"

JAPANESE_SECTIONS = (
    "基本情報",
    "要旨の翻訳",
    "新規性",
    "一言まとめ",
    "研究課題",
    "データとタスク定義",
    "手法の骨子",
    "主要な結果",
    "深掘り分析",
    "限界",
    "私のメモ",
    "参考文献",
)


def japanese_note() -> str:
    return """---
tags:
  - papers/methods
aliases:
  - "Auditable Tool Use"
date: 2024
doi: 10.1234/example
---

# Auditable Tool Use

## 基本情報

- タイトル: Auditable Tool Use
- タイトル訳: 監査可能なツール利用
- 著者: Smith et al.
- 発表時期: 2024
- 発表媒体: Example Journal
- DOI: 10.1234/example
- 論文タイプ: AI_method

## 要旨の翻訳

本論文は多段階の質問応答のために監査可能な状態機械を構築し、明示的な失敗記録が回答の信頼性を改善するかを評価する。

## 新規性

- 証拠選択とツール状態の追跡を一つの実行記録に統合し、失敗した証拠が黙って信頼できる入力に変わることを防ぐ。
- 証拠の欠落と推論の誤りを区別する明示的なロールバック状態を追加し、最終回答の追跡を可能にする。

## 一言まとめ

明示的なツール状態の記録は、多段階質問応答における誤りの伝播を減らす。

## 研究課題

検索が不完全で、外部ツールが失敗し、中間結果が誤用されるとき、多段階質問応答システムはどのように追跡可能性を保てるか。

## データとタスク定義

入力は質問、候補証拠、利用可能なツールであり、出力は回答、状態トレース、そして完了が支持されない場合の失敗ラベルである。

## 手法の骨子

### 機構フロー

1. **入力:** 質問と候補証拠。**操作:** 関連する証拠を抽出する。**出力:** 根拠づけられた初期状態。
2. **入力:** 現在の状態とツール登録簿。**操作:** 要求を利用可能なツールに整列させる。**出力:** 計画された呼び出し。
3. **入力:** ツール出力と確信度。**操作:** 状態を更新するかロールバックする。**出力:** 監査可能な実行記録。
4. **入力:** 最終状態。**操作:** 回答または拒否を復号する。**出力:** 出所を伴う応答。

> [!figure] Figure 1 システム概要
> 推奨位置：手法の骨子
> 配置理由：この図は証拠とツール状態が実行チェーンをどう流れるかを示す。
> 現在の状態：プレースホルダを保持。抽出した切り出しは不完全で、単独では解釈できない。

## 主要な結果

三つのデータセットにわたり、回答精度は 71.2% から 78.5% に向上し、追跡不能な誤りは 18% から 9% に減少した。

## 深掘り分析

重要な貢献はスコアの向上だけではない。失敗した呼び出しは隠れた中間状態ではなく検査可能な証拠となり、監査と的を絞った復旧を支える。

## 限界

評価は英語の質問応答データと狭いツール集合に限られており、マルチモーダルなツールや高遅延サービスに対する頑健性は確立していない。

## 私のメモ

状態記録の設計は、ソース資料の欠落とモデルの解釈失敗を分離するため、証拠優先の論文ワークフローでも再利用できる。

## 参考文献

- Smith et al. (2024). Auditable Tool Use for Multi-hop Question Answering. DOI: 10.1234/example
"""


def plan_payload() -> dict:
    return {
        "output_language": "ja",
        "paper_type": "AI_method",
        "paper_type_rationale": "モデルの機構を提案し評価する論文である。",
        "dominant_domain": "reasoning",
        "must_cover": ["手法の骨子"],
        "key_numbers": ["78.5%"],
        "real_comparisons": ["71.2% 対 78.5%"],
        "central_claims": [{
            "claim": "手法は追跡可能性を改善する。",
            "supporting_evidence": [{"section_id": "sec:results"}],
            "what_it_actually_proves": "報告されたプロトコルはツール状態を記録する。",
            "what_it_does_not_prove": "本番環境での頑健性は証明していない。",
        }],
        "claim_boundaries": ["証拠は報告されたワークフローに限られる。"],
        "negative_or_limiting_results": ["マルチモーダルなツールは試験されていない。"],
        "mechanism_result_map": ["ロールバック状態が追跡不能な誤りの減少を説明する。"],
        "comparative_positioning": ["回答のみのベースラインと比較。"],
        "reuse_takeaways": ["失敗状態を明示的に追跡する。"],
        "followup_questions": ["欠落・遅延したツール出力を試験する。"],
        "section_plan": [{"section": "手法の骨子", "evidence_sources": [{"section_id": "sec:method"}]}],
    }


def run_lint(tmp_path: Path, note: str, *extra_args: str) -> dict:
    note_path = tmp_path / "paper.md"
    plan_path = tmp_path / "paper.plan.json"
    output_path = tmp_path / "lint.json"
    note_path.write_text(note, encoding="utf-8")
    plan_path.write_text(json.dumps(plan_payload(), ensure_ascii=False), encoding="utf-8")
    subprocess.run(
        [
            sys.executable,
            str(LINT_SCRIPT),
            *extra_args,
            "--input",
            str(note_path),
            "--plan-file",
            str(plan_path),
            "--output",
            str(output_path),
        ],
        check=True,
    )
    return json.loads(output_path.read_text(encoding="utf-8"))


def test_japanese_language_aliases() -> None:
    assert normalize_output_language("ja") == "ja"
    assert normalize_output_language("Japanese") == "ja"
    assert normalize_output_language("ja-JP") == "ja"
    assert normalize_output_language("日本語") == "ja"
    assert require_artifact_output_language({"output_language": "ja"}, "Note Plan", "ja") == "ja"
    with pytest.raises(ValueError):
        require_artifact_output_language({"output_language": "ja"}, "Note Plan", "en")


def test_japanese_user_configuration_accepts_ja(tmp_path: Path) -> None:
    path = tmp_path / "config.json"
    path.write_text(
        json.dumps({"output_language": "ja", "save_mode": "workspace"}),
        encoding="utf-8",
    )
    result = inspect_configuration(config_path=path, environ={})
    assert result["state"] == "ready"
    assert result["affected_fields"] == []
    assert result["configuration"]["output_language"] == "ja"


def test_japanese_user_configuration_reports_invalid_enum_with_ja_choice(tmp_path: Path) -> None:
    path = tmp_path / "config.json"
    path.write_text(
        json.dumps({"output_language": "fr", "save_mode": "workspace"}),
        encoding="utf-8",
    )
    result = inspect_configuration(config_path=path, environ={})
    assert result["state"] != "ready"
    messages = [issue["message"] for issue in result["issues"]]
    assert any("ja" in message for message in messages)


def test_japanese_contract_exposes_localized_schema() -> None:
    contract = compact_writing_contract("ja")
    assert contract["language"] == "ja"
    assert tuple(contract["must_include_sections"]) == JAPANESE_SECTIONS
    assert tuple(required_sections("ja")) == JAPANESE_SECTIONS
    assert contract["mechanism_flow_heading"] == "機構フロー"
    assert contract["core_info_fields"] == [
        "タイトル",
        "タイトル訳",
        "著者",
        "所属",
        "発表時期",
        "発表媒体",
        "DOI",
        "arXiv",
        "論文リンク",
        "コード / プロジェクト",
        "データ / リソース",
        "論文タイプ",
    ]
    assert contract["figure_labels"] == {
        "location": "推奨位置：",
        "reason": "配置理由：",
        "status": "現在の状態：",
        "original_caption": "論文原図番号：",
    }
    assert contract["abstract_contract"]["requirement"] == "faithful_rendering_in_output_language"
    # 日本語プロファイルの契約本文に簡体字中国語のセクション名が残っていないこと
    dumped = json.dumps(contract, ensure_ascii=False)
    for leftover in ("核心信息", "方法主线", "关键结果", "深度分析", "我的笔记"):
        assert leftover not in dumped


def test_japanese_paper_type_contracts_use_japanese_section_names() -> None:
    contracts = paper_type_contracts("ja")
    assert set(contracts) == {
        "AI_method",
        "benchmark_or_dataset",
        "clinical_or_psychology_empirical",
        "humanities_or_social_science",
        "survey_or_review",
    }
    ai_method = contracts["AI_method"]
    assert "手法の骨子" in ai_method["section_semantics"]
    assert "機構フロー" in ai_method["recommended_subsections"]["手法の骨子"]
    assert ai_method["mechanism_flow_contract"]["required_step_count"] == "3_to_4"
    for contract in contracts.values():
        assert set(contract["section_semantics"]) <= set(JAPANESE_SECTIONS)
        assert set(contract["recommended_subsections"]) <= set(JAPANESE_SECTIONS)


def test_japanese_grounding_accepts_japanese_section_plan() -> None:
    plan = plan_payload()
    plan["central_claims"][0]["supporting_evidence"] = [{"section_id": "sec:method"}]
    plan["section_plan"] = [
        {
            "section": section,
            "focus": f"{section} に固有の証拠と分析上の役割を説明する。",
            "evidence_sources": [{"section_id": "sec:method"}],
        }
        for section in ("研究課題", "データとタスク定義", "手法の骨子", "主要な結果", "深掘り分析", "限界")
    ]
    manifest = {
        "coverage": {"total_pages": 10, "text_truncated": False},
        "sections": [{"section_id": "sec:method", "title": "Method", "page_start": 1, "page_end": 10}],
        "pages": [],
    }
    assert validate_note_plan(plan, manifest, "ja") == []


def test_japanese_figure_plan_uses_japanese_targets_and_reasons() -> None:
    items = build_figure_items(
        {
            "figure_captions": [{"id": "Figure 1", "caption": "Overview of the system architecture."}],
            "table_captions": [{"id": "Table 1", "caption": "Main results on three benchmarks."}],
        },
        language="ja",
    )
    by_id = {item["id"]: item for item in items}
    assert by_id["Figure 1"]["section"] == "機構フロー"
    assert by_id["Table 1"]["section"] == "主要な結果"
    dumped = json.dumps(items, ensure_ascii=False)
    assert "この" in dumped
    for leftover in ("方法主线", "关键结果", "深度分析", "机制流程"):
        assert leftover not in dumped


def test_japanese_note_passes_every_lint_gate_from_user_configuration(
    tmp_path: Path, configured_user_home: Path
) -> None:
    configured_user_home.write_text(
        json.dumps({"output_language": "ja", "save_mode": "workspace"}),
        encoding="utf-8",
    )
    payload = run_lint(tmp_path, japanese_note())
    assert payload["output_language"] == "ja"
    assert payload["warnings"] == []
    assert all(value is True for key, value in payload.items() if key.startswith("passes_"))


@pytest.mark.parametrize(
    ("original", "invalid"),
    [
        ("> 推奨位置：", "> 建议位置："),
        ("> 現在の状態：", "> Current status:"),
        ("### 機構フロー", "### 机制流程"),
        ("- タイトル:", "- 标题:"),
    ],
)
def test_japanese_lint_requires_exact_labels_and_mechanism_heading(
    tmp_path: Path, original: str, invalid: str
) -> None:
    payload = run_lint(tmp_path, japanese_note().replace(original, invalid), "--language", "ja")
    all_gates_pass = all(value is True for key, value in payload.items() if key.startswith("passes_"))
    assert payload["warnings"] or not all_gates_pass


@pytest.mark.parametrize(
    "leftover_line",
    [
        "### 机制流程",
        "> 建议位置：手法の骨子",
        "这张图解释方法内部机制。",
    ],
)
def test_japanese_lint_rejects_simplified_chinese_leftovers(tmp_path: Path, leftover_line: str) -> None:
    note = japanese_note().replace(
        "重要な貢献はスコアの向上だけではない。",
        f"重要な貢献はスコアの向上だけではない。\n\n{leftover_line}",
    )
    payload = run_lint(tmp_path, note, "--language", "ja")
    assert payload["passes_style_gate"] is False
    assert "mixed_language_lines_present" in payload["warnings"]
    assert any(
        issue["reason"] == "simplified_chinese_text_present" for issue in payload["mixed_language_issues"]
    )


def test_japanese_lint_keeps_shared_kanji_and_source_metadata(tmp_path: Path) -> None:
    # 日中で共有される漢字（数・与・会・後 など）と、参考文献の原語メタデータは許容する
    note = japanese_note().replace(
        "- Smith et al. (2024). Auditable Tool Use for Multi-hop Question Answering. DOI: 10.1234/example",
        "- Smith et al. (2024). Auditable Tool Use for Multi-hop Question Answering. DOI: 10.1234/example\n"
        "- 张伟 (2023). `可审计的工具使用`. DOI: 10.1234/example2",
    ).replace(
        "状態記録の設計は、",
        "数値と証拠を与える設計は会議後にも再利用でき、状態記録の設計は、",
    )
    payload = run_lint(tmp_path, note, "--language", "ja")
    assert payload["passes_style_gate"] is True


def test_japanese_lint_requires_complete_top_level_heading_order(tmp_path: Path) -> None:
    note = (
        japanese_note()
        .replace("## 手法の骨子", "## TEMP")
        .replace("## 主要な結果", "## 手法の骨子")
        .replace("## TEMP", "## 主要な結果")
    )
    payload = run_lint(tmp_path, note, "--language", "ja")
    assert payload["passes_basic_structure"] is False
    assert "top_level_section_profile_invalid" in payload["warnings"]


def test_japanese_lint_flags_english_prose_mixed_into_japanese(tmp_path: Path) -> None:
    note = japanese_note().replace(
        "重要な貢献はスコアの向上だけではない。",
        "重要な貢献は the improvement of the score だけではない and it is also about the auditability。",
    )
    payload = run_lint(tmp_path, note, "--language", "ja")
    assert payload["passes_style_gate"] is False
    assert "mixed_language_lines_present" in payload["warnings"]


def test_japanese_lint_rejects_generic_japanese_filler(tmp_path: Path) -> None:
    note = japanese_note().replace(
        "- 証拠選択とツール状態の追跡を一つの実行記録に統合し、失敗した証拠が黙って信頼できる入力に変わることを防ぐ。",
        "- 本論文は新しい手法を提案する。",
    ).replace(
        "- 証拠の欠落と推論の誤りを区別する明示的なロールバック状態を追加し、最終回答の追跡を可能にする。",
        "- 新規性が高い。",
    )
    payload = run_lint(tmp_path, note, "--language", "ja")
    assert not all(value is True for key, value in payload.items() if key.startswith("passes_"))


def test_run_pipeline_accepts_ja_language_override() -> None:
    script = Path(__file__).resolve().parents[1] / "skills/deeppapernote/scripts/run_pipeline.py"
    result = subprocess.run(
        [sys.executable, str(script), "--help"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True,
    )
    assert "ja" in result.stdout


JAPANESE_DOMAIN_RULES = """
domains:
  - label: 医療・健康
    aliases:
      - healthcare
      - medical
    specialized_folders:
      - メンタルヘルス
    keywords:
      - clinical
      - patient
    methods: []
  - label: メンタルヘルス
    route_to: 医療・健康
    aliases:
      - mental health
    keywords:
      - depression
    methods: []
fallback_domains:
  - label: 機械学習
    aliases:
      - machine learning
    keywords:
      - deep learning
      - neural network
    methods: []
  - label: 未分類
    aliases:
      - unclassified
    keywords: []
    methods: []
""".strip() + "\n"


def test_domain_rules_can_be_overridden_by_environment_path(tmp_path: Path, monkeypatch) -> None:
    import common

    rules_path = tmp_path / "ja_domain_rules.yaml"
    rules_path.write_text(JAPANESE_DOMAIN_RULES, encoding="utf-8")
    monkeypatch.setenv("DEEPPAPERNOTE_DOMAIN_RULES", str(rules_path))

    assert common.infer_domain_label("Deep learning for depression screening", "patient cohort") == "医療・健康"
    assert common.infer_domain_label("A neural network for image denoising") == "機械学習"


def test_domain_rules_next_to_user_configuration_are_preferred_over_skill_default(
    tmp_path: Path, monkeypatch, configured_user_home: Path
) -> None:
    import common

    monkeypatch.delenv("DEEPPAPERNOTE_DOMAIN_RULES", raising=False)
    (configured_user_home.parent / "domain_rules.yaml").write_text(JAPANESE_DOMAIN_RULES, encoding="utf-8")

    assert common.infer_domain_label("A neural network for image denoising") == "機械学習"


def test_domain_fallback_labels_follow_loaded_rules(tmp_path: Path, monkeypatch) -> None:
    """ルールにヒットしない場合の既定ラベルも、読み込んだ規則の alias から解決する。"""
    import common

    rules_path = tmp_path / "ja_domain_rules.yaml"
    rules_path.write_text(JAPANESE_DOMAIN_RULES, encoding="utf-8")
    monkeypatch.setenv("DEEPPAPERNOTE_DOMAIN_RULES", str(rules_path))

    # ルールのキーワードには一切ヒットしないが論文タイプが AI_method と推定されるタイトル
    assert common.infer_domain_label(
        "A new encoder-decoder model with attention for translation",
        "We propose a model architecture and train it end to end; ablations show gains.",
    ) == "機械学習"
    assert common.infer_domain_label(
        "Randomized controlled trial of cognitive therapy",
        "We enrolled participants with anxiety and measured symptom scores at follow-up.",
    ) == "医療・健康"
    # 何にも該当しない場合（人文系の論文タイプ）
    assert common.infer_domain_label(
        "An ethnographic study of eighteenth-century poetry circles",
        "An interpretive account of literary sociability.",
    ) == "未分類"
