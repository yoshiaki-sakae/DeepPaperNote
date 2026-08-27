# Paper Types

Every note keeps the same 12 top-level sections from `NOTE_REQUIRED_SECTIONS`.
Paper type only changes the typed semantics of shared sections and the recommended `###` subsections used in `note_plan.section_plan`.

Use `contracts_by_paper_type[note_plan.paper_type]` as the canonical structured source:
- `section_semantics`: how each fixed top-level section should be interpreted for this paper type.
- `recommended_subsections`: paper-type-specific `###` candidates for technical or analytical sections.
- `boundary_questions`: paper-type-specific questions that should shape `central_claims`, `claim_boundaries`, `negative_or_limiting_results`, `mechanism_result_map`, `comparative_positioning`, and `followup_questions`.

## `AI_method`

section_semantics:
- 研究課題: 手法が解決しようとする具体的な技術課題と、既存手法の弱点。
- データとタスク定義: データセット、入出力、評価タスク、実験設定。
- 手法の骨子: モデル、アルゴリズム、学習または推論の機構。
- 主要な結果: 主結果、強力なbaseline、ablation、重要な数値。
- 深掘り分析: 手法がなぜ有効か、どこが脆弱か、再現と拡張のコスト。

recommended_subsections:
- 手法の骨子: `機構フロー`, `モデル構造`, `学習目標`, `推論とサンプリングの経路`, `重要な実装の詳細`
- 主要な結果: `主結果と強力なbaseline`, `ablationが結局何を示しているか`, `失敗または不安定な設定`
- 深掘り分析: `なぜ有効か`, `計算量と拡張性`, `再現時の注意点`

boundary_questions:
- 中核となる機構の効果は、主結果によって示唆されるだけでなく、どの実験やablationによって裏付けられているか？
- どの比較は、現在のデータ・baseline・計算資源・プロトコルの下でのみ有効であることを示すにとどまり、汎用的な場面へ外挿できないか？
- 論文は失敗・劣化・不安定・コスト増大の証拠を示しているか。示していない場合、結論の境界はどこにあるか？

## `benchmark_or_dataset`

section_semantics:
- 研究課題: この benchmark/dataset が補おうとしている評価またはデータのギャップ。
- データとタスク定義: データの出所、タスクの分割、ラベル/設問の定義、サンプルの範囲。
- 手法の骨子: データ構築、選別、アノテーション、評価プロトコル。モデルの pipeline としては書かない。
- 主要な結果: baselineの性能、難易度の分布、カバー範囲とバイアス。
- 深掘り分析: それが実際に測定できているものと、代表できないもの。

recommended_subsections:
- データとタスク定義: `データの出所`, `タスクの分割`, `アノテーション/選別プロトコル`
- 手法の骨子: `構築フロー`, `評価プロトコル`, `Baseline 設定`
- 主要な結果: `baselineの性能`, `難易度の分布`, `カバー範囲とバイアス`
- 深掘り分析: `benchmark が実際に測定できているもの`, `適用の境界`

boundary_questions:
- この benchmark/dataset が実際に測定している構成概念は何か。どの能力は間接的な近似にすぎないか？
- タスク・ラベル・サンプリング・フィルタリング・評価プロトコルは、どのようなカバレッジの欠落やバイアスを持ち込むか？
- baselineの結果は、評価セットに識別力があることを示しているのか、それとも特定の種類のモデルがそのプロトコルに適応しているだけなのか？
- サンプルの長さ、コーパスの長さ、人口統計、クラス分布、データのアクセス可能性、プライバシー上の制約は、再現と外挿にどのように影響するか？

## `clinical_or_psychology_empirical`

section_semantics:
- 研究課題: 臨床・心理学・行動科学における研究課題、仮説、または変数間の関係。
- データとタスク定義: サンプルの出所、選択・除外基準、変数/尺度、測定方法。
- 手法の骨子: 研究デザイン、群分け、測定手順、統計分析の道筋。
- 主要な結果: 主要な効果、相関、群間差、不確実性または有意性。
- 深掘り分析: 結果の解釈、因果の境界、臨床/心理学的意義、外挿の限界。

recommended_subsections:
- データとタスク定義: `サンプルと選択・除外基準`, `変数と尺度`, `測定手順`
- 手法の骨子: `研究デザイン`, `分析モデル`, `主要な比較`
- 主要な結果: `主要な効果`, `不確実性と有意性`, `臨床または心理学的解釈`
- 深掘り分析: `因果的解釈の境界`, `外挿の限界`

boundary_questions:
- サンプルの出所、選択・除外基準、測定ツール、アノテーション手順は、外挿をどのように制限するか？
- 結果が支持するのは相関か、予測か、群間差か、それとも因果的解釈か。論文のデザインが証明できる範囲を越えないこと。
- 臨床または心理学的意義は、未観測の交絡、尺度の閾値、テキスト/音声の欠損、場面的な制約に依存していないか？
- サンプルの構成、データの欠損、プライバシー上の制約、資料が非公開であることは、再現と再分析をどのように制限するか？

## `humanities_or_social_science`

section_semantics:
- 研究課題: 著者が説明しようとする社会・文化・歴史・制度または理論上の問い。
- データとタスク定義: 資料、事例、テキスト、インタビュー、アーカイブまたはコーパスの範囲。ML task としては書かない。
- 手法の骨子: 理論的枠組み、概念の区別、論証の道筋。
- 主要な結果: 中核となる解釈的知見、概念的貢献、または既存の見解への修正。
- 深掘り分析: 論証の強さ、資料の境界、解釈の代替可能性、転用可能性。

recommended_subsections:
- データとタスク定義: `資料の範囲`, `選択基準`, `事例またはコーパスの境界`
- 手法の骨子: `理論的枠組み`, `概念の区別`, `論証の道筋`
- 主要な結果: `中核となる解釈的知見`, `概念的貢献`
- 深掘り分析: `論証の強さ`, `代替的な解釈`, `資料の境界`

boundary_questions:
- 著者の解釈は、どの資料・事例・理論的前提に依存しているか？
- 同じ資料を同様に説明できる代替的な解釈は存在するか。論文はそれをどのように排除しているか、あるいは排除できていないか？
- どの結論が概念的貢献または規範的判断であって、そのまま経験的事実として扱えるものではないか？

## `survey_or_review`

section_semantics:
- 研究課題: サーベイが整理しようとしている分野の問い、論争、または知識のギャップ。
- データとタスク定義: 対象とする文献の範囲、検索/選別の基準、サーベイの対象。
- 手法の骨子: 分類体系、サーベイの構成方法、エビデンス統合の論理。個別論文の手法アーキテクチャとしては書かない。
- 主要な結果: 分野の合意、相違、動向、代表的な方向性、未解決の問い。
- 深掘り分析: サーベイがカバーしていない盲点、分類体系の説明力、今後の研究機会。

recommended_subsections:
- データとタスク定義: `サーベイの範囲`, `包含/除外基準`, `文献のカバレッジ`
- 手法の骨子: `分類体系`, `手法の系譜`, `エビデンスの構成方法`
- 主要な結果: `代表的な方向性`, `合意と相違`, `未解決の問い`
- 深掘り分析: `分類体系の限界`, `カバーされていない領域`, `今後の研究機会`

boundary_questions:
- 検索範囲、包含・除外基準、分類軸は、どの研究の流れを取りこぼすか？
- サーベイが示しているのは分野の合意か、著者による分類か、それともまだ解決されていない相違か？
- どの動向に関する結論が、カバー範囲内の文献分布に由来するにとどまり、そのまま技術成熟度の判断として扱えないか？

## Selection Rule

Choose one primary `note_plan.paper_type` from the synthesis bundle's allowed values first.
Then keep the fixed top-level sections and use that paper type's `section_semantics` plus `recommended_subsections` to write `note_plan.section_plan`.
