#!/usr/bin/env python3
"""Scaffolded JSON contracts for the paper-deep-notes core workflow."""

from __future__ import annotations

from typing import Any, TypedDict

from locales import get_locale

_LOCALE = get_locale()

NOTE_REQUIRED_SECTIONS: tuple[str, ...] = _LOCALE["NOTE_REQUIRED_SECTIONS"]

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

PAPER_TYPE_SECTION_PROFILES: dict[str, dict[str, dict[str, Any]]] = _LOCALE["PAPER_TYPE_SECTION_PROFILES"]

PAPER_TYPE_CONTRACTS: dict[str, dict[str, Any]] = _LOCALE["PAPER_TYPE_CONTRACTS"]

WRITING_CONTRACT_RULES: dict[str, Any] = {
    "required_sections": NOTE_REQUIRED_SECTIONS,
    "paper_type_values": PAPER_TYPE_VALUES,
    "note_plan_required_fields": NOTE_PLAN_REQUIRED_FIELDS,
    "note_plan_field_types": NOTE_PLAN_FIELD_TYPES,
    "note_plan_required_field_checks": REQUIRED_FIELD_CHECKS,
    "grounding_required_sections": _LOCALE["GROUNDING_REQUIRED_SECTIONS"],
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
