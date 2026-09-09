# Output Language

DeepPaperNote supports three output schemas:

| Setting | Language |
|---|---|
| `zh-CN` | Simplified Chinese |
| `en` | English |
| `ja` | Japanese |

Resolve the profile through `user-configuration.md`. For a single command, use `--language en` (or `--language ja`) with `run_pipeline.py`, `build_synthesis_bundle.py`, `lint_note.py`, or `write_obsidian_note.py` where applicable. A Run Override never changes User Configuration.

## Simplified Chinese note schema

Use these top-level sections in this order:

1. `核心信息`
2. `原文摘要翻译`
3. `创新点`
4. `一句话总结`
5. `研究问题`
6. `数据与任务定义`
7. `方法主线`
8. `关键结果`
9. `深度分析`
10. `局限`
11. `我的笔记`
12. `引用`

Use `### 机制流程` for the mechanism-flow subsection. Chinese figure placeholders use the labels `建议位置：`, `放置原因：`, and `当前状态：`; a materialized image caption begins with `论文原图编号：`.

`原文摘要翻译` is a faithful Chinese translation of the source abstract. Preserve its meaning and scope; contribution claims, result interpretation, and hindsight judgment belong later unless the source abstract itself contains them.

## English note schema

Use these top-level sections in this order:

1. `Core Information`
2. `Abstract`
3. `Contributions`
4. `One-Sentence Summary`
5. `Research Question`
6. `Data and Task Definition`
7. `Method`
8. `Key Results`
9. `Deep Analysis`
10. `Limitations`
11. `Research Notes`
12. `References`

The allowed Core Information fields, in order, are:

`Title`, `Translated title`, `Authors`, `Institutions`, `Publication date`, `Venue`, `DOI`, `arXiv`, `Paper link`, `Code / Project`, `Data / Resources`, `Paper type`.

Use `### Mechanism Flow` for the mechanism-flow subsection. Each figure placeholder uses:

```md
> [!figure] Figure 2 Human-readable label
> Suggested location: Method
> Why it matters: This figure clarifies the execution path.
> Current status: Placeholder retained; the recovered crop is incomplete.
```

For a materialized image, use the normal image embed followed immediately by one italic caption beginning with `Original paper item:`.

`Abstract` is a faithful rendering of the source abstract in English. Preserve its meaning and scope; contribution claims, result interpretation, and hindsight judgment belong later unless the source abstract itself contains them.

The English style gate checks headings, Core Information labels, figure callouts, inserted-image captions, and prose. Mark original non-English metadata with inline code inside `Core Information`, or with inline code or a Markdown link inside `References`; closed fenced code blocks and URLs keep their normal source text. In prose, a CJK identifier or stable proper noun must be an HTTP Markdown link or Obsidian wikilink. A source formula may retain only these CJK `\operatorname{...}` labels: `输入`, `输出`, `损失`, `状态`, `动作`, `奖励`, `标签`, `样本`, `预测`, and `目标`. The surrounding text remains subject to the English gate; inline code and free-form math text do not exempt Chinese prose.

## Japanese note schema

Use these top-level sections in this order:

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

The allowed 基本情報 fields, in order, are:

`タイトル`, `タイトル訳`, `著者`, `所属`, `発表時期`, `発表媒体`, `DOI`, `arXiv`, `論文リンク`, `コード / プロジェクト`, `データ / リソース`, `論文タイプ`.

Use `### 機構フロー` for the mechanism-flow subsection. Each figure placeholder uses:

```md
> [!figure] Figure 2 図の内容を表す短い見出し
> 推奨位置：手法の骨子
> 配置理由：この図は実行経路を明確にする。
> 現在の状態：プレースホルダを保持。切り出した画像は不完全。
```

For a materialized image, use the normal image embed followed immediately by one italic caption beginning with `論文原図番号：`.

`要旨の翻訳` is a faithful Japanese translation of the source abstract. Preserve its meaning and scope; contribution claims, result interpretation, and hindsight judgment belong later unless the source abstract itself contains them.

Write natural Japanese prose (常体・敬体 consistently within a note). Keep stable proper nouns, model names, dataset names, and metric names in their original form; do not force-translate them. Mechanism-flow steps should name 入力 / 操作 / 出力 explicitly.

The Japanese style gate checks headings, 基本情報 labels, figure callouts, inserted-image captions, and prose. Because kanji are shared with Chinese, the gate looks for simplified-Chinese-only characters (机, 图, 论, 议, 态, ...) that never appear in Japanese; any such character in a heading, label, or prose line is a leftover from the Chinese template and fails `passes_style_gate`. Original Chinese metadata is allowed inside `基本情報` and `参考文献` when marked with inline code or a Markdown link, and URLs and closed fenced code blocks keep their source text. Lines that mix Japanese with four or more English words including English function words are also rejected as mixed-language prose.

Domain folders: the skill ships `references/domain_rules.yaml` with Chinese folder labels and `references/domain_rules.ja.yaml` with Japanese ones (医療・健康, 法律, 教育, 金融, ロボティクス, ソフトウェア工学, 生物医学, メンタルヘルス, 推薦システム, 大規模言語モデル, 機械学習, 未分類). When the resolved `output_language` is `ja`, `resolve_domain_subdir` selects the Japanese file automatically, so a Japanese Vault gets Japanese folder names without extra setup. To customize labels, keep a copy outside the skill, either at `~/.deeppapernote/domain_rules.yaml` (next to `config.json`) or at the path named by `DEEPPAPERNOTE_DOMAIN_RULES`; both take precedence over any shipped file, and fallback folder labels are resolved through the `healthcare`, `machine learning`, and `unclassified` aliases of that taxonomy. Existing domain folders already present under the papers root are still reused regardless of language.

## Contract ownership

`SKILL.md` owns the cross-stage Language Integrity Contract. This reference owns only the profile-specific schema and labels above; apply them under the resolved language carried by that contract.
