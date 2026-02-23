# プランファイル解析レポート: plan-r1.en.*.md 集約分析

## 1. 対象と背景

本レポートは、`docs/.tmp/report_p1_p2_gap_analysis.md` で特定された P1（Conflict Resolution Ambiguity）および P2（Condition Identifier Vocabulary）の課題を解決するために作成された 5 本のプランファイルを分析し、それぞれの特徴をまとめたものである。

対象プランファイル:

- `docs/.tmp/plan-r1.en.claude.md`
- `docs/.tmp/plan-r1.en.codex.md`
- `docs/.tmp/plan-r1.en.copilot.md`
- `docs/.tmp/plan-r1.en.cursor.md`
- `docs/.tmp/plan-r1.en.gpt.md`

対象ファイル（修正対象）: `.agents/skills/meta-skill.ai-directive-files-authoring/SKILL.md`

---

## 2. 各プランの概要と特徴づけ

### 2.1 plan-r1.en.claude.md

**全体の特徴**: 最も詳細で構造化されたプラン。変更単位に ID を付与し、実行計画・リスク評価・将来課題まで網羅する。

**他にない特色**:

1. **`canonical-terms` によるエイリアス定義**: P2-A において、`definitions` に新規追加する識別子に対して `canonical-terms` キーを導入し、スペース区切りの元表記を明示的に紐づける。例: `creating-ai-directive-file` の `canonical-terms: ["creating AI directive file"]`。これにより、将来の正規形と人間可読表記の対応関係がファイル内で保持される。

2. **`condition_identifiers` 規約文の追加（Change P2-D）**: `interpretation` に新キーを追加し、「condition 識別子はハイフン区切り小文字で definitions のキーと一致すること」を MUST として宣言する。将来の不整合を防止するための規約を仕様内に組み込む点が特徴的である。

3. **影響範囲の完全なインベントリ**: 2.4 節で、`["creating AI directive file", "editing AI directive file"]` を使用する 35 ルール、yaml-include-\* の 6 ルール、tier-separation の 4 ルールを列挙。変更漏れを防ぐための網羅的な一覧を提供する。

4. **`failure_states_and_degradation` との整合性**: P1 の設計根拠において、既存の `rule-conflict` failure state の記述と整合させることを明示。変更が既存仕様の他セクションに与える影響を考慮している。

5. **Tier 分離による実行計画**: Phase 1・Phase 2 それぞれに Tier 0〜5 の段階を定義し、各 Tier のスコープ・出力形式・停止条件を表形式で明示。authoring skill の tier-separation 原則に沿った実行手順を提供する。

---

### 2.2 plan-r1.en.codex.md

**全体の特徴**: フェーズ駆動型で、ベースラインインベントリと検証の整備を重視する。

**他にない特色**:

1. **Phase 0: ベースラインインベントリ**: 変更適用前に、使用されている識別子・定義済み識別子・ステータス（exact match / alias only / missing）のマッピング表を構築することを必須とする。他プランにはない事前インベントリフェーズであり、変更の網羅性を担保する。

2. **Phase 3: 検証の整備**: P1・P2 の修正に加え、検証ステップの追加・更新を独立したフェーズとして設ける。識別子の存在確認、トークン照合、複合条件の妥当性を機械的に検証できるようにする。

3. **AC6: 検証による機械的検出**: 受入基準として「AC1〜AC5 の違反を検証が機械的に検出できること」を明示。修正内容だけでなく、その検証可能性までを成果物に含める。

4. **リスクとコントロールの対応**: 各リスクに対して Control を 1 対 1 で紐づける形式。例: 「部分的正規化で混在が残る」→「Phase 0 のインベントリを完了証拠として必須とする」。

5. **単一の決定論的パス**: P1 について「単一の決定論的パスが存在する」ことを exit condition として明示。曖昧さの排除を出口条件として定義する。

---

### 2.3 plan-r1.en.copilot.md

**全体の特徴**: 複数のアプローチを提示し、推奨と代替を明確に区別する。将来の拡張や他セクションとの整合性を考慮した項目を多く含む。

**他にない特色**:

1. **Approach 2（代替案）の明示的検討**: P2 について、Approach 1（conditions を definitions のハイフン形式に合わせる）に加え、Approach 2（definitions のキーをスペース区切りに変更して conditions に合わせる）を記載。YAML キーにスペースを使う場合の引用の必要性や保守性の観点から Approach 1 を推奨する理由を説明する。

2. **識別子の表記形式**: 新規追加する trigger 識別子に `creating-AI-directive-file` のように PascalCase を部分的に用いる（AI, YAML を大文字）。他プランの小文字統一とは異なる表記方針を採用する。

3. **P1-B の任意性**: `interpretation.priority` の修正（P1-B）を「optional, for clarity」と明記。必須変更と任意変更を区別している。

4. **将来検討項目の拡張**: `MUST_vs_SHOULD` と `prohibition_vs_other` の layer/priority スコープの見直し、`triggers` セクションの導入、複合条件の BNF 等の形式文法の定義を「Items for future consideration」として列挙。P1・P2 以外の conflict policy や構造拡張まで視野に入れている。

5. **変更規模の評価表**: 各変更（P1-A, P1-B, P2-A, P2-B, P2-C）について、対象セクションと影響範囲を表形式で整理。例: P2-C は「約 30 ルール」と明示する。

---

### 2.4 plan-r1.en.cursor.md

**全体の特徴**: **AI directive ファイルの編集を行わない**という制約に基づき、runner/linter 側の挙動で決定論性を実現する方針を採用する。5 本中唯一、対象ファイルの修正を前提としない。

**他にない特色**:

1. **制約の明示**: 「Concrete edits to AI directive files are not allowed in this iteration」とし、directive テキストの内部不整合が残った状態でも、評価・検証を決定論的にすることを目標とする。

2. **Resolver アルゴリズムの仕様化**: P1 について、実装指向の短い仕様（コードまたはドキュメント）を成果物とする。layer → priority → conflict policy の順序をアルゴリズムとして記述する。

3. **Conflict-resolution テストの実装**: 異なる layer、同一 layer 異 priority、同一 layer 同一 priority の MUST vs MUST の 3 ケースをカバーするテスト・フィクスチャを成果物に含める。MUST-vs-MUST halt が tie の場合にのみ到達することを検証する。

4. **エイリアスルールによる識別子解決**: P2 について、directive ファイルを編集せず、runner/linter 側で「scope 」で始まりスペースを含むトークンに対して、スペースをハイフンに置換して definitions キーと照合する決定論的エイリアスルールを定義する。

5. **Reserved triggers の扱い**: definitions に存在しない識別子（「creating AI directive file」等）を、gap analysis で挙げられた識別子に限定した「reserved triggers」として runner/linter が扱う。厳密な「MUST be defined」解釈との衝突リスクを認識しつつ、明示的・監査済みリストに限定する方針を取る。

6. **リスク: エイリアスの副作用**: エイリアス適用が語彙のドリフトを隠蔽するリスクを指摘し、エイリアス適用時はレポートに含め、strict モードでは CI 失敗とする緩和策を提案する。

---

### 2.5 plan-r1.en.gpt.md

**全体の特徴**: 最も簡潔で、要点に絞った記述。実装順序を表形式で明示する。

**他にない特色**:

1. **簡潔な構成**: 6 セクション（Summary of Issues, P1, P2, Implementation Order, Success Criteria, References）に集約。他プランにない Purpose/Scope/Definitions の前置きを省略し、問題と解決策に集中する。

2. **Implementation Order 表**: Step 1〜5 で P1 と P2 の実施順序を表形式で示す。Step 4・5 で両課題に対する検証を統合する。実施順序の可視化が明確である。

3. **Scope 識別子の選択肢提示**: P2 において、scope 識別子の正規化について (a) conditions でハイフン形式を使用する、(b) スペース形式の定義を追加してその形式に統一する、の 2 案を簡潔に列挙。どちらを採用するかは実装者に委ねる形で記載する。

4. **オプションの Stepwise アルゴリズム**: P1 の Required Specification Updates において、「(1) layer order, (2) numeric priority, (3) conflict policy for ties を実行する段階的 conflict-resolution アルゴリズムを追加すること」を optional として記載する。

5. **References セクション**: ソース文書と対象ファイルのみを列挙する簡潔な参照リストを提供する。

---

## 3. プラン間の比較マトリクス

| 観点                         | Claude | Codex | Copilot | Cursor | GPT   |
| ---------------------------- | ------ | ----- | ------- | ------ | ----- |
| 対象ファイルの編集           | あり   | あり  | あり    | **なし** | あり  |
| 事前インベントリフェーズ     | なし   | **あり** | なし  | なし   | なし  |
| 検証の整備を独立フェーズ化   | なし   | **あり** | なし  | あり*  | なし  |
| 代替アプローチの提示         | なし   | なし  | **あり** | なし   | 部分的 |
| canonical-terms / エイリアス | **canonical-terms** | なし | なし | **runner 側エイリアス** | なし |
| 規約文の追加                 | **condition_identifiers** | なし | なし | なし | なし |
| 影響ルールの完全列挙         | **あり** | なし  | なし  | なし   | なし  |
| テスト・フィクスチャの成果物 | なし   | なし  | なし  | **あり** | なし  |
| 将来検討項目の詳細度         | 中     | 低    | **高** | 低     | 低    |

\* Cursor は runner/linter の仕様・実装を成果物とするため、検証は実装に含まれる。

---

## 4. まとめ

5 本のプランは、いずれも `report_p1_p2_gap_analysis.md` の P1・P2 を解消することを目的とし、layer → priority → conflict policy の決定論的カスケードと、condition 識別子の定義・照合可能性の確保という方向性で一致している。

一方で、**Cursor プラン**は「AI directive ファイルを編集しない」という制約に基づき、runner/linter 側の挙動変更とエイリアス・reserved triggers による対応という、他 4 本と根本的に異なるアプローチを採用している。

**Claude プラン**は、`canonical-terms`、`condition_identifiers` 規約、影響ルールの完全列挙、tier-separated 実行計画など、仕様拡張と実行管理の両面で最も詳細である。

**Codex プラン**は、Phase 0 のベースラインインベントリと Phase 3 の検証整備により、変更の網羅性と検証可能性を重視する。

**Copilot プラン**は、代替アプローチの検討、識別子表記方針、将来の conflict policy や構造拡張の検討項目など、設計選択の幅と将来拡張を意識した内容を持つ。

**GPT プラン**は、簡潔さを優先し、実装順序の明確化と選択肢の提示に特化している。

---

## 5. 参照

- ソース文書: `docs/.tmp/report_p1_p2_gap_analysis.md`
- 対象ファイル: `.agents/skills/meta-skill.ai-directive-files-authoring/SKILL.md`
- 分析対象プラン: `docs/.tmp/plan-r1.en.claude.md`, `plan-r1.en.codex.md`, `plan-r1.en.copilot.md`, `plan-r1.en.cursor.md`, `plan-r1.en.gpt.md`
