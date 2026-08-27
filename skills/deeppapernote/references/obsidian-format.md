# Obsidian Format

## Heading Rules

- Use `#` for the note title only.
- Use `##` for major sections.
- Use `###` only when a section genuinely needs internal structure.
- Do not flatten everything into bullet points.
- For method, system, benchmark, or clinical empirical papers, prefer meaningful `###` subheadings in technical sections instead of one long undifferentiated block.
- For method, framework, or system papers, default to `### 機構フロー` inside `手法の骨子` and write it as a numbered 3 to 4 step flow.

## File Naming

Default file name:
- sanitized English title with underscores
- default note layout is folder-per-paper:
  - `<領域>/<paper_slug>/<paper_slug>.md`
  - `<領域>/<paper_slug>/images/...`
- when deciding `<領域>`, prefer matching an existing first-level domain folder under the user's papers directory
- domain routing uses the editable taxonomy in `references/domain_rules.yaml`: application domains are checked before fallback method domains
- reuse existing first-level folders conservatively; method-only evidence should not force reuse of an unrelated application folder
- only create a new domain folder when no existing domain is a reasonable fit
- do not save new papers directly into the bare papers root
- always create the paper-local `images/` directory during final save, even if no real image is inserted
- the paper-local `images/` directory is part of the required note layout, not an optional optimization

If the user already has a vault convention, preserve it.

## Markdown Style

- Prefer short paragraphs over long bullet lists.
- Use bullets for metadata and sharply list-shaped content.
- Keep code or metric identifiers in backticks.
- When English proper nouns (model names, dataset names, method names, metric names, venue abbreviations) or standalone key numeric values appear inline within Japanese prose, wrap them in backticks for visual separation — e.g. `GPT-4`、`SQuAD`、`BLEU`、`87.3%`.
- Preserve stable internal links where useful.
- Use normal LaTeX delimiters for math:
  - inline math: `$...$`
  - display math:
    `$$`
    `...`
    `$$`
- Do not wrap formulas in backticks or fenced code blocks unless you are literally showing source code.

## Core Info Block

`## 基本情報` is a fixed metadata zone.

Formatting and scope rules:
- Core info field schema: use only the following fields, in this order, and no free prose:
  `タイトル`, `タイトル訳`, `著者`, `所属`, `発表時期`, `発表媒体`, `DOI`, `arXiv`, `論文リンク`, `コード / プロジェクト`, `データ / リソース`, `論文タイプ`
- keep each entry in `- フィールド名: 値` form
- omit fields that are unavailable or not applicable; do not add placeholder rows just to fill the schema
- do not add interpretation, commentary, judgment, or takeaway lines inside `基本情報`
- do not use the last metadata bullet as a place to append extra analysis
- move explanatory content to `一言まとめ`、`深掘り分析`、`私のメモ` or another true analysis section

## YAML Frontmatter

Every note must start with an Obsidian properties block **above** the `#` title heading.

Required fields:
- `tags`: use `papers/<domain>` hierarchy, e.g. `papers/NLP`, `papers/CV`, `papers/multimodal`
- `aliases`: English short name or common abbreviation for wikilink resolution
- `date`: ISO publication date; use `YYYY` if only the year is known
- `doi`: DOI string without the `https://doi.org/` prefix; omit the field entirely if unavailable

Example:

```yaml
---
tags:
  - papers/NLP
aliases:
  - "Paper Short Name"
date: 2024-05-01
doi: 10.18653/v1/2024.acl-long.1
---
```

Rules:
- Do not invent placeholder values for missing fields; omit them instead.
- The `tags` field must always be present with at least one `papers/<domain>` tag.
- `aliases` should be the paper's short name or acronym (e.g. "GPT-4", "LoRA"), not a paraphrase.

## Figure Placeholder Style

Use this callout format only for placeholders that remain unresolved in the final note:

```md
> [!figure] Fig. 3 データ分布と品質評価
> 推奨位置：データとタスク定義
> 配置理由：この図はサンプル構成・対話長の統計・専門家による品質チェック結果を同時に示しており、`PsyInterview` データの境界を理解する上で最も重要な図の一つである。
> 現在の状態：プレースホルダを保持。現在の抽出結果では局所的なサブ図しか取得できず、独立して解釈可能な完全な原図として安定的に復元できない。
```

Formatting rules:
- keep the original paper numbering, for example `Fig. 3` or `Table 2`
- keep a short human-readable label on the first line
- always include `推奨位置`
- always include `配置理由`
- always include `現在の状態`

`現在の状態` should be explicit, for example:
- `プレースホルダを保持。高信頼度の全体図が見つからない。`
- `プレースホルダを保持。現在は疑わしい局所サブ図しかマッチせず、安定的な置き換えには不十分。`

The structured `[FIGURE_PLACEHOLDER] ... [/FIGURE_PLACEHOLDER]` block is legacy/internal only.
Do not use it in the final user-facing note unless you are debugging the pipeline.

If a real image has been selected and materialized into the vault, do not keep the `[!figure]` callout for that same figure.
Prefer an Obsidian embed, or use a Markdown image embed when that is the available path.
The embed must be followed immediately by exactly one italic caption line:

```md
![[Research/Papers/DeepPaperNote/paper_slug/images/page_003_img_01.png]]
*論文原図番号：Fig. 2。データ生成のフロー図。ここに挿入するのは、手法の骨子の理解に最も役立つためである。*
```

## Default Section Order

1. `基本情報`
2. `要旨の翻訳`
3. `新規性`
4. `一言まとめ`
5. `研究課題`
6. `データとタスク定義`
7. `手法の骨子`
8. `主要な結果`
9. `深掘り分析`
10. `限界`
11. `私のメモ`
12. `参考文献`

When abstract metadata exists, `要旨の翻訳` should be a single Japanese translation block for the original abstract rather than a bilingual subsection pair.

This order is the stable backbone, not a full outline.
When the paper is complex, add `###` subsections such as:
- `### データソース`
- `### タスク定義`
- `### 機構フロー`
- `### なぜ結果が成立するのか`
- `### 誤読されやすい箇所`

## 参考文献 Section Format

Entries in `## 参考文献` should link to existing notes in the vault where possible.
If the synthesis bundle includes `references.candidates`, use confirmed candidate `wikilink` values when present. When `wikilink` is empty, treat `display_text` as the plain-text fallback.
Follow this priority order for each reference:

1. **Vault lookup first**: check whether the cited paper already has a note in the vault.
   - Match by note basename (the `<paper_slug>` part of the folder name).
   - Match by the `aliases` field in the note's YAML frontmatter.
2. **If a match is found**: write a wikilink that separates the target from the display text:
   ```
   - [[paper_slug_or_alias|Human Readable Title]]
   ```
3. **If no match is found**: do not invent a wikilink target. Write the reference as plain text instead:
   ```
   - Vaswani et al. (2017). Attention Is All You Need.
   ```
   Use the candidate `display_text` as the plain fallback when available.

Rules:
- Never use a raw English paper title as the wikilink target; it will not match vault filenames.
- To derive a likely slug from a title: lowercase the title and replace spaces and special characters with underscores — but only use the result as the target if you have confirmed the file exists.
- List only papers cited or directly relevant to this note.
- Do not add extra DOIs or author metadata when using wikilink format; the display text is enough.
