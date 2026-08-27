#!/usr/bin/env python3
"""Scaffolded JSON contracts for the paper-deep-notes core workflow."""

from __future__ import annotations

from typing import Any, TypedDict

NOTE_REQUIRED_SECTIONS: tuple[str, ...] = (
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

PAPER_TYPE_VALUES: tuple[str, ...] = (
    "AI_method",
    "benchmark_or_dataset",
    "clinical_or_psychology_empirical",
    "humanities_or_social_science",
    "survey_or_review",
)

NOTE_PLAN_STRING_FIELDS: tuple[str, ...] = (
    "paper_type",
    "paper_type_rationale",
    "dominant_domain",
)

NOTE_PLAN_LIST_FIELDS: tuple[str, ...] = (
    "must_cover",
    "key_numbers",
    "real_comparisons",
    "central_claims",
    "claim_boundaries",
    "negative_or_limiting_results",
    "mechanism_result_map",
    "comparative_positioning",
    "reuse_takeaways",
    "followup_questions",
    "section_plan",
)

NOTE_PLAN_REQUIRED_FIELDS: tuple[str, ...] = NOTE_PLAN_STRING_FIELDS + NOTE_PLAN_LIST_FIELDS
NOTE_PLAN_FIELD_TYPES: dict[str, str] = {
    **dict.fromkeys(NOTE_PLAN_STRING_FIELDS, "string"),
    **dict.fromkeys(NOTE_PLAN_LIST_FIELDS, "array"),
}
REQUIRED_FIELD_CHECKS: dict[str, dict[str, bool]] = {
    "string": {"non_empty": True},
    "array": {"non_empty": True},
}
CENTRAL_CLAIM_FIELD_TYPES: dict[str, str] = {
    "claim": "string",
    "supporting_evidence": "array",
    "what_it_actually_proves": "string",
    "what_it_does_not_prove": "string",
}


def required_field_value_error(
    value: Any,
    field_type: str,
    checks: dict[str, dict[str, bool]],
) -> str:
    if field_type == "string":
        if not isinstance(value, str):
            return "invalid"
        return "empty" if checks["string"]["non_empty"] and not value.strip() else ""
    if field_type == "array":
        if not isinstance(value, list):
            return "invalid"
        return "empty" if checks["array"]["non_empty"] and not value else ""
    return "invalid"

PAPER_TYPE_SECTION_PROFILES: dict[str, dict[str, dict[str, Any]]] = {
    "AI_method": {
        "section_semantics": {
            "研究課題": "手法が解決しようとする具体的な技術課題と、既存手法の弱点。",
            "データとタスク定義": "データセット、入出力、評価タスク、実験設定。",
            "手法の骨子": "モデル・アルゴリズム・学習または推論の機構。",
            "主要な結果": "主結果、強力なベースライン、アブレーション、重要な数値。",
            "深掘り分析": "手法がなぜ有効か、どこが脆いか、再現・拡張のコスト。",
        },
        "recommended_subsections": {
            "手法の骨子": ["機構フロー", "モデル構造", "学習目標", "推論・サンプリング経路", "主要な実装詳細"],
            "主要な結果": ["主要結果と強力なベースライン", "アブレーションが示すもの", "失敗・不安定な設定"],
            "深掘り分析": ["なぜ有効か", "計算量とスケーラビリティ", "再現時の注意点"],
        },
    },
    "benchmark_or_dataset": {
        "section_semantics": {
            "研究課題": "この benchmark/dataset が埋めようとする評価またはデータのギャップ。",
            "データとタスク定義": "データ出所、タスク分割、ラベル/課題の定義、サンプル範囲。",
            "手法の骨子": "データ構築・選別・アノテーション・評価プロトコル。モデルの pipeline としては書かない。",
            "主要な結果": "ベースライン性能、難易度分布、カバレッジ範囲、バイアス。",
            "深掘り分析": "実際に何を測れているか、そして何を代表できないか。",
        },
        "recommended_subsections": {
            "データとタスク定義": ["データ出所", "タスク分割", "アノテーション/選別プロトコル"],
            "手法の骨子": ["構築フロー", "評価プロトコル", "ベースライン設定"],
            "主要な結果": ["ベースライン性能", "難易度分布", "カバレッジとバイアス"],
            "深掘り分析": ["ベンチマークが実際に測るもの", "適用範囲の境界"],
        },
    },
    "clinical_or_psychology_empirical": {
        "section_semantics": {
            "研究課題": "臨床・心理学・行動科学における研究課題、仮説、変数間の関係。",
            "データとタスク定義": "サンプル出所、選択・除外基準、変数/尺度、測定方法。",
            "手法の骨子": "研究デザイン、群分け、測定手順、統計解析の道筋。",
            "主要な結果": "主効果、相関、群間差、不確実性や有意性。",
            "深掘り分析": "結果の解釈、因果の境界、臨床/心理学的意義、外挿の限界。",
        },
        "recommended_subsections": {
            "データとタスク定義": ["サンプルと選択・除外基準", "変数と尺度", "測定手順"],
            "手法の骨子": ["研究デザイン", "分析モデル", "主要な比較"],
            "主要な結果": ["主要な効果", "不確実性と有意性", "臨床・心理学的解釈"],
            "深掘り分析": ["因果解釈の境界", "外挿の限界"],
        },
    },
    "humanities_or_social_science": {
        "section_semantics": {
            "研究課題": "著者が説明しようとする社会・文化・歴史・制度・理論上の問い。",
            "データとタスク定義": "資料、事例、テキスト、インタビュー、アーカイブ、コーパスの範囲。ML task としては書かない。",
            "手法の骨子": "理論的枠組み、概念の区別、論証の道筋。",
            "主要な結果": "中心的な解釈的発見、概念的貢献、既存の見解への修正。",
            "深掘り分析": "論証の強さ、資料の境界、解釈の代替可能性、転用可能性。",
        },
        "recommended_subsections": {
            "データとタスク定義": ["資料の範囲", "選択基準", "事例・コーパスの境界"],
            "手法の骨子": ["理論的枠組み", "概念の区別", "論証の道筋"],
            "主要な結果": ["中心的な解釈的発見", "概念的貢献"],
            "深掘り分析": ["論証の強さ", "代替的解釈", "資料の境界"],
        },
    },
    "survey_or_review": {
        "section_semantics": {
            "研究課題": "サーベイが整理しようとする分野の問い、論争、知識のギャップ。",
            "データとタスク定義": "対象とする文献範囲、検索/選別基準、レビュー対象。",
            "手法の骨子": "分類体系、レビューの構成方法、証拠統合のロジック。単一論文の手法構成としては書かない。",
            "主要な結果": "分野の合意、対立、トレンド、代表的な方向性、未解決問題。",
            "深掘り分析": "サーベイがカバーしていない盲点、分類体系の説明力、今後の研究機会。",
        },
        "recommended_subsections": {
            "データとタスク定義": ["サーベイの範囲", "選定・除外基準", "文献カバレッジ"],
            "手法の骨子": ["分類体系", "手法の系譜", "証拠の整理方法"],
            "主要な結果": ["代表的な方向性", "合意と対立", "未解決問題"],
            "深掘り分析": ["分類体系の限界", "未カバー領域", "今後の研究機会"],
        },
    },
}

PAPER_TYPE_CONTRACTS: dict[str, dict[str, Any]] = {
    "AI_method": {
        "paper_type": "AI_method",
        "reader_lens": "手法の機構を再現できる技術読者向け",
        "section_focus": [
            "問題設定",
            "手法の機構",
            "学習/推論フロー",
            "主要な数式",
            "比較ベースライン",
            "アブレーションと失敗の境界",
        ],
        "required_checks": ["機構フロー、主要な数式、実験デザイン、アブレーションの含意、失敗の境界を説明する必要がある。"],
        "formula_rules": ["手法の理解に必須の 1〜3 個の主要な数式のみを残し、その工学的含意を説明する。"],
        "avoid_rules": ["AI_method でない論文を無理にモデルアーキテクチャとして書き換えない。"],
        "boundary_questions": [
            "中心的な機構の利得は、主結果が示唆するだけでなく、どの実験やアブレーションで裏付けられているか？",
            "どの比較が現在のデータ・ベースライン・計算資源・プロトコルの下でのみ有効で、汎用的な状況へ外挿できないか？",
            "論文は失敗・劣化・不安定・コスト増の証拠を示しているか。示していない場合、結論の境界は何か？",
        ],
        **PAPER_TYPE_SECTION_PROFILES["AI_method"],
        "mechanism_flow_contract": {
            "apply_when_paper_type_in": ["AI_method"],
            "required_step_count": "3_to_4",
            "required_step_fields": ["input", "operation", "output_destination"],
        },
    },
    "benchmark_or_dataset": {
        "paper_type": "benchmark_or_dataset",
        "reader_lens": "benchmark/dataset の有用性とバイアスの境界を判断したい研究者向け",
        "section_focus": [
            "タスク分割",
            "データ出所と構築フロー",
            "アノテーションプロトコル",
            "評価指標",
            "カバレッジ範囲とバイアス",
            "サンプル統計とデータ公開制限",
        ],
        "required_checks": [
            "データ出所、構築/アノテーションのフロー、評価指標、ベースライン性能、サンプル統計、データ公開やプライバシー制限、適用範囲の境界を説明する必要がある。"
        ],
        "formula_rules": ["中心的な評価指標、サンプリング規則、分割定義のみを残す。"],
        "avoid_rules": ["データ構築フローをモデルの pipeline として書かない。"],
        "boundary_questions": [
            "この benchmark/dataset が実際に測定している構成概念は何で、どの能力は間接的な近似に過ぎないか？",
            "タスク・ラベル・サンプリング・フィルタ・評価プロトコルは、どのようなカバレッジの欠落やバイアスを持ち込むか？",
            "ベースライン結果は評価セットに識別力があることを示すのか、それとも特定タイプのモデルがこのプロトコルに適応しただけか？",
            "サンプルの長さ、コーパス長、人口統計、クラス分布、データのアクセス可能性やプライバシー制限は、再現と外挿にどう影響するか？",
        ],
        **PAPER_TYPE_SECTION_PROFILES["benchmark_or_dataset"],
    },
    "clinical_or_psychology_empirical": {
        "paper_type": "clinical_or_psychology_empirical",
        "reader_lens": "臨床/心理学のサンプル、変数関係、外挿の境界に注目する研究読者向け",
        "section_focus": [
            "サンプル出所",
            "選択・除外基準",
            "変数または尺度",
            "分析パイプライン",
            "効果量と不確実性",
            "サンプル統計・倫理・データのアクセス可能性",
        ],
        "required_checks": [
            "相関・予測・群間差・因果的解釈を区別し、サンプル統計、倫理/プライバシー上の制約、外挿の境界を説明する必要がある。"
        ],
        "formula_rules": ["中心的な統計モデル、効果量、信頼区間、尺度の定義のみを残す。"],
        "avoid_rules": ["相関、予測性能、群間差を、証明されていない因果結論として書かない。"],
        "boundary_questions": [
            "サンプル出所、選択・除外基準、測定ツール、アノテーション手順は、外挿をどのように制限するか？",
            "結果は相関・予測・群間差・因果的解釈のどれを支持するか。論文のデザインが証明できる範囲を越えないこと。",
            "臨床または心理学的意義は、未観測の交絡、尺度の閾値、テキスト/音声の欠落、場面の制約に依存していないか？",
            "サンプル構成、データ欠損、プライバシー制限、資料の非公開は、再現と再分析をどのように制限するか？",
        ],
        **PAPER_TYPE_SECTION_PROFILES["clinical_or_psychology_empirical"],
    },
    "humanities_or_social_science": {
        "paper_type": "humanities_or_social_science",
        "reader_lens": "理論的枠組み、資料の解釈、論証の構造に注目する研究読者向け",
        "section_focus": ["研究対象", "資料の出所", "理論的枠組み", "論証の道筋", "概念的貢献", "解釈の境界"],
        "required_checks": ["著者の論証、資料的証拠、規範的判断、実験的事実を区別する必要がある。"],
        "formula_rules": ["通常は数式を無理に残さない。中心的な形式的定義やコーディング規則のみを残す。"],
        "avoid_rules": ["規範的判断、テキスト解釈、事例分析を実験的事実として書かない。"],
        "boundary_questions": [
            "著者の解釈は、どの資料・事例・理論的前提に依存しているか？",
            "同じく資料を説明できる代替的解釈は存在するか。論文はそれをどのように排除したか、あるいは排除していないか？",
            "どの結論が概念的貢献や規範的判断であり、経験的事実として直接扱えないものか？",
        ],
        **PAPER_TYPE_SECTION_PROFILES["humanities_or_social_science"],
    },
    "survey_or_review": {
        "paper_type": "survey_or_review",
        "reader_lens": "サーベイの脈絡、分類体系、証拠の境界を整理する必要のある研究読者向け",
        "section_focus": [
            "サーベイの範囲",
            "選定・除外基準",
            "テーマ分類",
            "手法の系譜",
            "合意と対立",
            "未解決問題",
        ],
        "required_checks": ["サーベイの範囲、文献の選定、分類体系、合意と対立、未解決問題を説明する必要がある。"],
        "formula_rules": ["分類軸、選定・除外の基準、証拠の集約規則、meta-analysis の統計量のみを残す。"],
        "avoid_rules": ["サーベイ中の代表的な結論を、著者自身が行った単一の実験結果として書かない。"],
        "boundary_questions": [
            "検索範囲、選定・除外基準、分類軸は、どの研究の流れを見落とすか？",
            "サーベイが示すのは分野の合意か、著者の分類か、それとも未解決の対立か？",
            "どのトレンド結論がカバレッジ内の文献分布に由来し、技術成熟度の判断として直接扱えないか？",
        ],
        **PAPER_TYPE_SECTION_PROFILES["survey_or_review"],
    },
}

WRITING_CONTRACT_RULES: dict[str, Any] = {
    "required_sections": NOTE_REQUIRED_SECTIONS,
    "paper_type_values": PAPER_TYPE_VALUES,
    "note_plan_required_fields": NOTE_PLAN_REQUIRED_FIELDS,
    "note_plan_field_types": NOTE_PLAN_FIELD_TYPES,
    "note_plan_required_field_checks": REQUIRED_FIELD_CHECKS,
    "grounding_required_sections": (
        "研究課題",
        "データとタスク定義",
        "手法の骨子",
        "主要な結果",
        "深掘り分析",
        "限界",
    ),
    "allowed_grounding_reference_forms": ("section_id", "pages"),
    "excluded_model_input_fields": (
        "evidence",
        "evidence_pack",
        "candidate_chunks",
        "section_texts",
        "summary",
        "summary_hints",
    ),
    "old_bundle_reference_prefixes": (
        "synthesis_bundle.evidence",
        "bundle.evidence",
        "synthesis_bundle.candidate_chunks",
        "synthesis_bundle.section_texts",
        "synthesis_bundle.summary",
        "bundle.candidate_chunks",
        "bundle.section_texts",
        "bundle.summary",
    ),
    "old_evidence_reference_tokens": (
        "evidence_pack",
        "summary.paper_type",
        "problem_evidence",
        "task_evidence",
        "data_evidence",
        "method_evidence",
        "mechanism_evidence",
        "results_evidence",
        "ablation_evidence",
        "limitations_evidence",
        "candidate_chunks",
        "section_texts",
    ),
    "figure_decision_values": (
        "review_pending",
        "insert",
        "placeholder",
        "low_priority",
        "visual_defect",
        "skip",
    ),
    "usable_insert_candidate": {
        "kinds": ("figure", "table"),
        "visual_quality_status": "usable_candidate",
        "requires_source_image_path": True,
    },
    "allowed_usable_placeholder_reasons": (
        "visual_defect",
        "materialization_blocked",
    ),
    "manual_visual_review_required_statuses": (
        "usable_candidate",
        "needs_visual_quality_check",
        "review",
    ),
    "automatic_fail_closed_visual_statuses": (
        "reject_visual_quality",
        "asset_candidate_missing",
    ),
    "visual_review_contract": {
        "selected_render_dpi": 300,
        "page_preview_dpi": 96,
        "review_fields": (
            "status",
            "reviewed_asset_sha256",
            "preserved_scientific_elements",
            "omitted_scientific_elements",
            "notes",
            "failure_reason",
            "repair_attempts",
            "revised_bbox",
        ),
        "review_status_values": ("pending", "pass", "fail", "repair_requested"),
        "repair_limit": 1,
        "asset_sha256_bound": True,
        "caption_free_visual_body_required": True,
        "decision_freeze_before": "note_plan",
        "review_evidence_fields": (
            "candidate_path",
            "page_preview_path",
            "source_pdf_path",
            "source_page",
            "caption",
            "bbox_pt",
            "normalized_bbox",
            "render_dpi",
        ),
        "repairable_failure_reasons": (
            "caption_contamination",
            "surrounding_prose_contamination",
            "scientific_content_clipped",
            "insufficient_safety_margin",
        ),
        "terminal_failure_reasons": (
            "identity_mismatch",
            "caption_inseparable",
            "ambiguous_visual_body",
            "unreadable_source",
            "scientific_content_missing",
            "repair_limit_exhausted",
        ),
    },
    "note_plan_depth_requirements": {
        "required_section_focus_min_chars": 20,
        "required_section_focus_fields": ("focus", "reading_goal", "purpose"),
        "generic_focus_phrases": (
            "use the raw source to explain",
            "paper-specific role of",
            "explain the paper-specific role",
            "explain this section",
            "summarize this section",
        ),
    },
    "analysis_coverage_contract": {
        "central_claim_fields": tuple(CENTRAL_CLAIM_FIELD_TYPES),
        "central_claim_field_types": CENTRAL_CLAIM_FIELD_TYPES,
        "central_claim_required_field_checks": REQUIRED_FIELD_CHECKS,
        "required_plan_fields": (
            "central_claims",
            "claim_boundaries",
            "negative_or_limiting_results",
            "mechanism_result_map",
            "comparative_positioning",
            "reuse_takeaways",
            "followup_questions",
        ),
        "final_quality_review_checks": (
            "central_claims_are_supported_by_raw_sections_or_pages",
            "key_experimental_settings_and_numbers_are_present",
            "mechanisms_or_protocol_choices_are_mapped_to_results",
            "comparisons_explain_positioning_against_alternatives",
            "discussion_or_limitation_claims_are_explained_mechanistically",
            "proven_claims_are_separated_from_unproven_or_unvalidated_claims",
            "research_or_engineering_takeaways_are_specific_and_reusable",
            "followup_questions_are_specific_to_replication_or_extension",
        ),
    },
}


class MetadataRecord(TypedDict, total=False):
    title: str
    translated_title: str
    paper_id: str
    source_type: str
    source_url: str
    year: str
    authors: list[str]
    affiliations: list[str]
    venue: str
    doi: str
    abstract: str
    code_url: str
    project_url: str
    zotero_key: str
    arxiv_id: str
    metadata_sources: list[str]
    identity_confidence: str
    identity_confidence_reasons: list[str]


class EvidenceItem(TypedDict, total=False):
    claim: str
    evidence: str
    source_section: str
    page_hint: str


class CandidateChunk(TypedDict, total=False):
    text: str
    source_section: str
    actual_source_section: str
    is_abstract_fallback: bool
    page_hint: str
    kind_hint: str


class EquationCandidate(TypedDict, total=False):
    equation: str
    source_section: str
    kind_hint: str


class ReferenceCandidate(TypedDict, total=False):
    raw_text: str
    display_text: str
    page_hint: str
    doi: str
    arxiv_id: str
    wikilink: str
    vault_target: str
    match_status: str
    match_reason: str


class FigureQualitySignals(TypedDict, total=False):
    visual_quality_status: str
    quality_reason_codes: list[str]
    page_coverage_ratio: float
    visual_rect_count: int
    visual_body_ratio: float
    paragraph_text_chars: int
    table_body_rows: int
    caption_text_chars: int


class FigureAssetCandidate(TypedDict, total=False):
    filename: str
    path: str
    width: int
    height: int
    size_bytes: int
    label: str
    extraction_level: str
    quality_signals: FigureQualitySignals
    candidate_status: str


class SectionExtractionCoverage(TypedDict, total=False):
    coverage_status: str
    recognized_sections: list[str]
    core_sections_found: list[str]
    missing_core_sections: list[str]
    section_text_chars: dict[str, int]
    fallback_sections: list[str]


class PdfCoverage(TypedDict, total=False):
    total_pages: int | None
    text_max_pages: int | None
    text_pages_scanned: int
    truncated_due_to_page_limit: bool
    appendix_detected: bool
    appendix_start_page: int | None
    references_start_page: int | None
    section_stop_reason: str
    section_stop_page: int | None


class AppendixIndex(TypedDict, total=False):
    appendix_detected: bool
    start_page: int | None
    sections: list[dict[str, Any]]
    figure_captions: list[dict[str, Any]]
    table_captions: list[dict[str, Any]]


class AppendixEvidenceItem(TypedDict, total=False):
    evidence: str
    source_section: str
    page_hint: str
    kind_hint: str


class EvidencePack(TypedDict, total=False):
    paper_id: str
    problem_evidence: list[EvidenceItem]
    task_evidence: list[EvidenceItem]
    data_evidence: list[EvidenceItem]
    method_evidence: list[EvidenceItem]
    mechanism_evidence: list[EvidenceItem]
    results_evidence: list[EvidenceItem]
    ablation_evidence: list[EvidenceItem]
    limitations_evidence: list[EvidenceItem]
    equation_candidates: list[EquationCandidate]
    reference_candidates: list[ReferenceCandidate]
    figure_captions: list[dict[str, Any]]
    table_captions: list[dict[str, Any]]
    sections: list[dict[str, Any]]
    section_texts: dict[str, str]
    candidate_chunks: dict[str, list[CandidateChunk]]
    language_hint: str
    section_sources: dict[str, str]
    section_extraction_coverage: SectionExtractionCoverage
    pdf_coverage: PdfCoverage
    appendix_index: AppendixIndex
    appendix_evidence: dict[str, list[AppendixEvidenceItem]]
    quotes: list[dict[str, Any]]
    evidence_quality: str
    extraction_failures: list[str]


class FigurePlanItem(TypedDict, total=False):
    id: str
    caption: str
    kind: str
    section: str
    reason: str
    priority: int
    anchor_text: str
    insert_mode: str
    figure_asset_candidate: FigureAssetCandidate
    candidate_pages: list[dict[str, Any]]
    candidate_status: str
    matching_strategy: str


class FigurePlan(TypedDict, total=False):
    paper_id: str
    figures: list[FigurePlanItem]


class SynthesisBundle(TypedDict, total=False):
    paper_id: str
    title: str
    metadata: dict[str, Any]
    evidence_quality: str
    coverage: dict[str, Any]
    source_manifest: dict[str, Any]
    source_index: dict[str, Any]
    references: dict[str, Any]
    figure_plan: dict[str, Any]
    figure_table_manifest: dict[str, Any]
    pdf_assets: dict[str, Any]
    writing_contract: dict[str, Any]


def empty_metadata() -> MetadataRecord:
    return MetadataRecord(
        title="",
        paper_id="",
        source_type="",
        source_url="",
        year="",
        authors=[],
        affiliations=[],
        metadata_sources=[],
        identity_confidence="",
        identity_confidence_reasons=[],
    )


def empty_evidence_pack() -> EvidencePack:
    return EvidencePack(
        paper_id="",
        problem_evidence=[],
        task_evidence=[],
        data_evidence=[],
        method_evidence=[],
        mechanism_evidence=[],
        results_evidence=[],
        ablation_evidence=[],
        limitations_evidence=[],
        equation_candidates=[],
        reference_candidates=[],
        figure_captions=[],
        table_captions=[],
        sections=[],
        section_texts={},
        candidate_chunks={},
        language_hint="unknown",
        section_sources={},
        section_extraction_coverage={},
        pdf_coverage={},
        appendix_index={},
        appendix_evidence={},
        quotes=[],
        extraction_failures=[],
        evidence_quality="unknown",
    )


def empty_figure_plan() -> FigurePlan:
    return FigurePlan(paper_id="", figures=[])


def empty_synthesis_bundle() -> SynthesisBundle:
    return SynthesisBundle(
        paper_id="",
        title="",
        metadata={},
        evidence_quality="unknown",
        coverage={},
        source_manifest={},
        source_index={},
        references={},
        figure_plan={},
        figure_table_manifest={},
        pdf_assets={},
        writing_contract={},
    )
