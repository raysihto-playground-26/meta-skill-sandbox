# MUST NOT 集中セクション方針および authoring スキル修正：統合プラン（claude 案）

作成日: 2026-02-23
レビュー対象: r1 草案、r2 改訂版、plan.codex、plan.gpt、plan.opus、plan.composer の計 6 ドキュメント
対象ファイル（実体）: `.agents/skills/meta-skill.ai-directive-files-authoring/SKILL.md`
パス補足: `.cursor/skills/`, `.github/skills/`, `.claude/skills/`, `.agent/skills/`,
`.gemini/skills/`, `.opencode/skills/`, `.windsurf/skills/` はすべて `../.agents/skills` へのシンボリックリンク。
修正対象は実体 1 ファイルのみ。
ステータス: 統合プラン（AI directive files への変更は本ドキュメントに含まない）

---

## 0. 本プランの位置づけと目的

### 0.1 位置づけ

本プランは、以下の 6 ドキュメントを総合的に検証し、統合したものである：

| ドキュメント | 主要な貢献 |
|---|---|
| r1 草案 (`must-not-section-policy-and-remediation-plan.md`) | 初期フレームワーク：強度分類、違反特定、変更 A/B/C の骨格 |
| r2 改訂版 (`must-not-section-policy-and-remediation-plan-r2.md`) | 4 レビューの統合：Semantic Gravity Wells 追加、規範オペレータ判定手続き精密化、A-2 statement 改善 |
| plan.gpt | 機械検証可能性への強い要求、「確立度」主張の抑制、規範オペレータ決定手続きの構文的固定 |
| plan.codex | Medium+ 概念、lint 化志向、`.agents`/`.cursor` 同期問題の提起、`statement_modal` フィールド提案 |
| plan.opus | Semantic Gravity Wells の反証統合、先行実装（コミット `23a7787`）の評価、A-2 statement の肯定的義務化 |
| plan.composer | A-1 スキーマ補完、Phase 2 の明示化、`definitions.tier-separation` の取り扱い、`prohibitions.override` 確認不要の判定 |

### 0.2 目的

1. **命題への回答**：MUST NOT 集中セクションの有効性がどこまで「確立」されているかを、
   研究・実証・設計論の各面から正確に位置づける。
2. **適用強度の確定**：Medium 強度の操作的定義を、検証可能な手続きとして確立する。
3. **meta-circular 回復方針の確定**：authoring スキルの唯一の確定違反に対する修正方針を、
   6 プランの収束点として確定する。
4. **分岐点の記録**：6 プラン間で意見が分かれた論点について、採否の根拠を明示する。

### 0.3 非目的

- AI directive files の具体的な変更（MUST NOT）。
- 学術論文の正確な引用検証を本プランの受け入れ条件とすること。
- 全ディレクティブファイルへの横展開（別タスク）。

---

## 1. MUST NOT 集中セクションの有効性：統合的評価

### 1.1 LLM のコンテキスト処理と "lost-in-the-middle" 現象

Liu et al. (2023) "Lost in the Middle" は、LLM が長コンテキストの情報を
位置依存的に処理することを実証した研究である。
GPT-3.5-Turbo, Claude-1.3, MPT-30B-Instruct, LongChat-13B 等のモデルで、
情報がコンテキスト中間にあるとき性能が有意に低下する **U 字型カーブ** が確認されている。

AI directive files への含意：

- 禁止事項は失敗コストが高く、中間に埋もれると遵守率が低下する。
- 先頭付近への配置は、遵守率を補助的に高める合理的な推論として支持される。
- ただし、この研究は情報検索タスクに対する知見であり、
  「指示遵守」への効果は直接実証されたものではない。

### 1.2 指示階層（Instruction Hierarchy）の実証知見と限界

OpenAI "Instruction Hierarchy"（Wallace et al. 2024）等は、
制約が明示的・独立的・早期配置の場合に遵守されやすいことを支持する。

**限界**（GPT 案・Opus 案で共通して指摘）：
OpenReview 2025 の研究では、system/user プロンプト分離でも命令階層の安定的確立に失敗し、
モデルが制約タイプに対する本質的なバイアスを持つことが確認されている。
「ワーキングメモリ相当への保持」は直接実証された結論ではなく、合理的推論として位置づける。

### 1.3 Semantic Gravity Wells：否定制約の逆活性化リスク

Semantic Gravity Wells（Rana, arXiv 2601.08070, 2026）は、6 プランの中で
Opus 案が初めて導入し、r2 改訂版に統合された重要な反証研究である。

核心的知見：

- **Priming Failure（違反の 87.5%）**：禁止対象の明示的言及が、抑制ではなく
  逆に対象を活性化する。成功時の確率低減（22.8pt）に対し、
  失敗時はわずか 5.2pt（4.4 倍の非対称性）。
- **Override Failure（違反の 12.5%）**：後段 FFN 層が禁止トークンへの正の寄与
  （+0.39）を生成し、前段の抑制シグナルを約 4 倍の強度で上書きする。
- **層 23–27 が因果的責任**：activation patching によりこれらの層の置換で
  制約効果が逆転することが確認されている。

**6 プランの収束点**（設計への含意）：

- MUST NOT を集中配置するだけでは遵守保証にならない。
  priming effect により逆活性化するリスクがある。
- **配置戦略は補助的手段、verification による事後検証が真の遵守保証手段**。
- Strong/Strict 強度（MUST NOT レコードの膨張）は priming リスクを増大させる
  可能性があり、これが Medium 推奨の追加根拠となる。

### 1.4 仕様設計論・規範論

法令・技術仕様書の設計慣行として、禁止事項の独立セクション化・前置は確立されている
（RFC 2119、deny-by-default 原則等）。この観点での確立度は高い。

### 1.5 結論：確立度の統合評価

| 観点 | 確立度 | 6 プラン間の合意度 |
|---|---|---|
| LLM 注意メカニズム（lost-in-middle）の実証 | 高 | 全プランで合意 |
| 禁止事項の早期配置が遵守率を補助的に高める | 中 | 全プランで「合理的推論」に収束（r1 の「高」を下方修正） |
| MUST NOT 集中配置による明示化の構造的メリット | 高 | 全プランで合意 |
| MUST NOT 明示言及による逆活性化リスク | 高 | Opus 案で導入、r2 で統合。GPT/Codex/Composer 案は言及なし |
| 構造化 + 事後検証の複合アプローチ | 高 | r2・Opus 案で明示的合意。他プランも verification 重視で実質的に同方向 |
| 配置位置の定量的最適点 | 中 | 未確定について全プランで合意 |

**統合的結論**：

「MUST NOT を独立した専用セクションに集約する」設計は、**合理的な慣行として支持される**。
ただし「集めれば遵守率が上がる」という単純命題は確立されておらず、
**「構造化された専用セクション＋事後検証（verification）」の複合アプローチとして
合理的に確立されている** と評価すべきである。

r1 草案の「合理的かつ効果的な慣行として確立されている」は楽観的すぎるが、
「研究上の定理として確立されている」と主張する文書は 6 プラン中存在しない。
GPT 案の「高信頼の設計慣行」、r2 の「複合的アプローチとして確立」が
最も正確な表現として収束している。

---

## 2. 適用強度の確定

### 2.1 強度の段階（6 プラン共通フレームワーク）

| 強度 | 内容 |
|---|---|
| **Weak** | SHOULD be in a dedicated section。例外を広く許容。 |
| **Medium** | `statement` の規範オペレータが MUST NOT である rule record は `prohibitions` に集約（MUST）。説明的 MUST NOT は許容。 |
| **Strong** | あらゆる rule record の `statement` に含まれる MUST NOT は `prohibitions` に移動。 |
| **Strict** | ファイル全体で MUST NOT のテキストが `prohibitions` 以外に出現することを禁止。 |

### 2.2 推奨強度：Medium（MUST として適用）

6 プラン全てが Medium を推奨し、Strict を不採用とする点で完全に合意している。
Codex 案の「Medium+」は、Medium を MUST 適用とする点で r2 の方針と実質同一である。

**Strict を不採用とする根拠（6 プランの収束点）**：

- 説明的 MUST NOT の prohibition 移動は構造肥大化を招く（全プランで合意）。
- Semantic Gravity Wells の観点から prohibition レコードの膨張は priming リスクを増大させる（r2・Opus）。
- Medium で遵守効果の大部分は達成される（全プランで合意）。

### 2.3 規範オペレータ判定手続き（Medium 強度の操作的定義）

6 プラン間で最も議論が分かれた論点の一つが「主述語」の定義である。

| プラン | アプローチ |
|---|---|
| r1・Composer | 「主述語として含む」（自然言語的定義） |
| r2 | 構文的判定手続き（左から走査、数える/数えないの条件リスト） |
| GPT | r2 と同方向の走査ベース手続き + 明示的な「数える/数えない」分類 |
| Codex | `statement_modal` 明示フィールド導入を提案（将来方向） |
| Opus | r2 準拠（走査ベース手続き）|

**本プランの採用方針**：r2 の構文的判定手続きを基盤とし、GPT 案の明確化を取り込む。
Codex 案の `statement_modal` フィールドは有用な将来方向だが、スキーマ変更を伴うため別タスクとする。

**採用する判定手続き**：

`statement` フィールドを左から走査し、以下の条件で「数える/数えない」を判定する。
最初に「数える」と判定された RFC モーダル（MUST NOT / MUST / SHOULD NOT / SHOULD / MAY）が
そのルールの**規範オペレータ**となる。

**「数えない（説明的）」の条件**（いずれかを満たす場合）：

1. 単引用符または二重引用符で囲まれたトークンとして出現（例：`'MUST NOT'`）
2. "the phrase MUST NOT" 等、語句としての言及であることが明示されている出現
3. RFC keywords の列挙として現れている出現（例：`(MUST, MUST NOT, SHOULD, ...)`）
4. 括弧内での説明として現れている出現（例：`All normative prohibitions (MUST NOT) MUST ...`）
5. 「e.g.」「for example」に続く例示の一部として現れている出現

**「数える（規範）」の条件**：上記に該当しない出現。

**Medium 強度のルール**：

> `statement` の規範オペレータが **MUST NOT** である rule record は、
> `prohibitions.items` に配置しなければならない（MUST）。
> 規範オペレータが MUST NOT 以外の rule record、
> および rule record 外のフィールドに登場する MUST NOT は、
> 説明的使用として扱い、`prohibitions` への移動を要しない。

### 2.4 GPT 案の「機械検証可能性」への応答

GPT 案は、Medium 強度の判定手続きが `verification-machine-checkable` と緊張する点を
正当に指摘している。本プランの判定手続き（上記 2.3）は、正規表現ベースの
近似的な機械チェックが可能な水準に達しているが、自然言語の曖昧性を完全には排除できない。
lint 化は別タスク候補として残す（セクション 8.4）。

---

## 3. 現状の meta-circular 非遵守箇所：統合的特定

### 3.1 確定違反（6 プラン全てで合意）

**違反 1：`explanatory-must-not-permitted` の配置**

| 項目 | 値 |
|---|---|
| ルール ID | `explanatory-must-not-permitted` |
| 所属セクション | `authoring_obligations` |
| statement | `"When describing interpretation, semantics, or verification (as opposed to primary normative statement fields), descriptive use of the phrase MUST NOT is allowed and MUST NOT be treated as additional enforceable prohibitions."` |
| 規範オペレータ | MUST NOT（"MUST NOT be treated" が走査で最初の「数える」モーダル） |
| 違反内容 | 規範オペレータが MUST NOT だが `prohibitions` に配置されていない |
| 参照ルール | `prohibitions-dedicated-section` |

**副次的問題：複合述語（6 プラン全てで合意）**

| 項目 | 値 |
|---|---|
| 問題内容 | "is allowed"（許可）と "MUST NOT be treated"（禁止）の 2 述語が同居 |
| 参照ルール | `one-obligation-per-rule` |
| 備考 | "is allowed" を MAY 相当と読めば形式的には 1 MUST NOT 述語のみとも解釈できるが、"is allowed" の曖昧性が `no-ambiguous-modals` の精神に反するため分割が望ましい（r2 の評価を採用） |

### 3.2 非違反の確認（6 プラン全てで合意）

| ルール ID | MUST NOT の出現形態 | 規範オペレータ | 判定 |
|---|---|---|---|
| `explanatory-must-not-for-clarity` | 例示（"e.g. listing RFC keywords..."）。 | SHOULD | 非違反 |
| `use-normative-keywords` | RFC keywords 列挙 `(MUST, MUST NOT, ...)`。 | MUST | 非違反 |
| `prohibitions-dedicated-section` | 括弧内説明 `(MUST NOT)` | MUST | 非違反 |
| `define-conflict-policy` | 例示内 `e.g. MUST vs MUST` | MUST | 非違反 |

### 3.3 rule record 外の MUST NOT（説明的使用として許容）

| 箇所 | フィールド種別 |
|---|---|
| `interpretation.unknown_keys` | interpretation prose |
| `interpretation.unspecified_behavior` | interpretation prose |
| `precedence_and_conflict.conflict_policy.MUST_vs_MUST` | conflict policy prose |
| `failure_states_and_degradation.failure_states[0].behavior` | behavior prose |
| `failure_states_and_degradation.degradation` | degradation prose |
| `definitions.tier-separation.description` | definition prose |
| `one-obligation-per-rule` の verification | verification field |

### 3.4 `definitions.tier-separation` の取り扱い（分岐点）

Composer 案は、`definitions.tier-separation.description` 内の "MUST NOT interleave" が
tier-separation 適用時に実質的な規範的禁止として機能する点を指摘した。

| プラン | 判断 |
|---|---|
| r2 | 説明的として許容。将来の `no-interleave-tiers` 追加を別タスク候補に |
| Composer | 説明的として許容するが、許容範囲に definitions を含む旨を明示すべき |
| 他プラン | 明示的な言及なし |

**本プランの採用方針**：r2・Composer の方向に従い、現状は説明的使用として許容する。
`explanatory-must-not-permitted` の A-2 書き換え時に definitions フィールドを
許容範囲に明示的に含める（r2 の A-1・A-2 案は既にこれを反映済み）。
将来の `no-interleave-tiers` prohibition 化は別タスク候補として残す。

---

## 4. 6 プラン間の分岐点と採否判断

### 4.1 先行実装（コミット `23a7787`）の扱い

Opus 案のみがこの論点を詳細に分析している。

| 先行変更 | Medium での必要性 | Opus の評価 |
|---|---|---|
| `no-assume-unspecified` 等 3 prohibition | 不要（元は rule record 外の MUST NOT） | 有害ではなく、暗黙制約の明示化として価値がある |
| インライン `(see prohibition-id)` 相互参照 | 不要 | トレーサビリティ向上に有益 |
| `non-prohibition-must-not-annotated` authoring ルール | 不要 | 既存ルールとの重複あり、将来の指針として残す価値はある |

**本プランの判断**：

先行実装の扱いは、本プランが対象とする方針レイヤーの範囲外である
（具体的なファイル変更方針は本プランでは取り扱わない）。
ただし、方針レベルでの推奨は以下の通り：

- **先行実装は revert せず維持する方向を推奨**。
  Medium 基準では不要だが、`design-assume-probabilistic` の精神に沿い、
  暗黙の制約の明示化として正の価値がある。
  revert は git 履歴にノイズを生じ、有用な明示化が失われる。
- **核心的違反の修正は先行実装とは独立して実施する必要がある**。
  先行実装は `explanatory-must-not-permitted` の statement 内の MUST NOT 主述語を
  修正していないため、meta-circular 違反は未解決のままである。

### 4.2 A-2（`explanatory-must-not-permitted` 書き換え後）の statement

6 プラン間で最も微妙な分岐点の一つ。

| プラン | A-2 statement の方向性 |
|---|---|
| r1 | "is classified as explanatory and does not constitute an enforceable prohibition" |
| r2 | "MUST be classified as explanatory; enforcement ... governed by no-treat-..." |
| GPT | 定義文（"are non-normative"）または検証可能な規範文へ |
| Codex | rule record として残すなら検証可能な単一モーダルで。定義文なら interpretation へ移動 |
| Opus | r2 と同一（"MUST be classified" + 相互参照） |
| Composer | r1 と同一（"is classified ... does not constitute"） |

**本プランの採用方針**：r2・Opus の「MUST be classified as explanatory」+ 相互参照を採用する。

根拠：
- r1/Composer の "does not constitute" は RFC モーダルに該当しないため
  `use-normative-keywords` との整合性が弱い（Opus 案の D-6 指摘）。
- "MUST be classified" は肯定的義務として明確な RFC モーダルであり、
  規範オペレータは MUST（MUST NOT ではない）となるため `prohibitions` 外に配置可能。
- 相互参照により A-1 との関係が明示され、トレーサビリティが向上する。
- Codex 案の「interpretation へ移動」は、`explanatory-must-not-permitted` が
  authoring_obligations のルールとしての機能（「この使い方は許容される」という指針）を
  失うため不採用。

### 4.3 `.agents`/`.cursor` の同期問題

Codex 案が「2 ファイル同時更新を必須とする」と指摘したが、
実際には `.cursor/skills` は `.agents/skills` へのシンボリックリンクであるため、
実体ファイルの更新が自動的にすべてのシンボリックリンク先に反映される。
この問題は**実際には存在しない**。

ただし、シンボリックリンク構造を知らないエージェントが独立にファイルを作成し
リンク構造を壊すリスクはあり、運用上の注意として記録する価値はある。

### 4.4 `statement_modal` 明示フィールドの導入

Codex 案の提案。規範オペレータを `statement` の自然言語解析に頼らず、
明示的なフィールドとして宣言する方向性。

**本プランの判断**：有用な将来方向として記録するが、
rule-record-schema の変更（全ルールへのフィールド追加）を伴うため、
本タスクの範囲外とする。規範オペレータ判定手続き（2.3）で
現時点では十分に操作可能である。

### 4.5 `prohibitions` セクションの位置移動

| プラン | 判断 |
|---|---|
| r1 | 別タスク（未解決事項） |
| r2 | Phase 2 として実施計画に明示 |
| GPT | 別タスク（任意） |
| Codex | YAML ブロック前半への移動を推奨 |
| Opus | 別タスクだが、Semantic Gravity Wells の知見から効果は限定的 |
| Composer | 本タスクの一部として扱うか、少なくとも Phase 2 に明記すべき |

**本プランの採用方針**：r2・Composer の方向に従い、Phase 2 として明示する。
ただし Opus の指摘のとおり、位置移動の効果は補助的であり、
verification の強化と組み合わせることが重要であることを明記する。

---

## 5. 目標設定

### 5.1 Meta-circular 完全遵守状態の定義

> authoring スキルが定義するすべてのルールを、authoring スキル自身が遵守している状態。

具体的には以下を同時に満たす状態：

1. `prohibitions-dedicated-section` 遵守：
   `prohibitions.items` 以外の全 rule record で、`statement` の規範オペレータが MUST NOT でない。
2. `one-obligation-per-rule` 遵守：
   すべての rule record で `statement` に規範述語が 1 つのみ。
3. `no-ambiguous-modals` 遵守：
   曖昧なモーダル（"is allowed" 等）が定義なしに使われていない。
4. `rule-record-schema` 遵守：
   全 rule record が id, layer, priority, statement, conditions, exceptions, verification を持つ。
5. YAML 構造の健全性：標準パーサで解析可能。

### 5.2 遵守の確認基準

上記 5 条件の成立を、以下の方法で検証する：

| 条件 | 検証方法 |
|---|---|
| 1 | 全 rule record の `statement` に対し規範オペレータ判定手続き（2.3）を適用 |
| 2 | 全 rule record の `statement` に対し RFC モーダルの出現数を確認 |
| 3 | 全 rule record の `statement` に対しモーダル曖昧性チェック |
| 4 | 全 rule record のフィールド存在チェック |
| 5 | YAML パーサによる解析 |

---

## 6. 修正方針

### 6.1 基本方針

**最小変更・最大整合**：既存の構造・意図を保持しつつ、
`explanatory-must-not-permitted` のリファクタリングで meta-circular 遵守を回復する。

6 プラン全てがこの原則に合意している。

### 6.2 変更 A：`explanatory-must-not-permitted` の分割

6 プラン全てが分割アプローチに合意している。

**A-1（新規 prohibition レコード、`prohibitions.items` 末尾に追加）**

```yaml
- id: "no-treat-explanatory-must-not-as-prohibition"
  layer: L2
  priority: 92
  statement: "MUST NOT treat descriptive uses of the phrase 'MUST NOT' in interpretation,
    semantics, definitions, or verification fields as additional enforceable prohibitions."
  conditions: ["creating AI directive file", "editing AI directive file"]
  exceptions: ["none"]
  verification: "No interpretation, semantics, definitions, or verification field treats
    descriptive MUST NOT as an enforceable prohibition; human or pattern check."
```

**A-2（`authoring_obligations` に残留、statement 書き換え）**

```yaml
- id: "explanatory-must-not-permitted"
  layer: L2
  priority: 92
  statement: "Descriptive use of the phrase MUST NOT in interpretation, semantics,
    definitions, or verification text (as opposed to primary normative statement fields)
    MUST be classified as explanatory; enforcement as a separate prohibition is governed
    by no-treat-explanatory-must-not-as-prohibition."
  conditions: ["creating AI directive file", "editing AI directive file"]
  exceptions: ["none"]
  verification: "Descriptive uses of MUST NOT in interpretation, semantics, definitions,
    or verification text are classified as explanatory and cross-reference
    no-treat-explanatory-must-not-as-prohibition for enforcement."
```

**設計判断の要約**：

| 判断項目 | 採用内容 | 根拠 |
|---|---|---|
| A-1 の `statement` | MUST NOT で始まる規範的禁止 | 規範オペレータ = MUST NOT → `prohibitions` に配置 |
| A-1 に definitions を含める | 含める | r2・Composer の指摘を反映。`definitions.tier-separation` の扱いを明示化 |
| A-2 の `statement` | "MUST be classified" + 相互参照 | r2・Opus の方向。`use-normative-keywords` との整合性が最も高い |
| A-2 の規範オペレータ | MUST（"MUST be classified"） | MUST NOT ではないため `authoring_obligations` に残留可能 |
| `exceptions` / `verification` | 完全スキーマで記述 | Composer 案の指摘（r1 で欠落していた）を反映 |

### 6.3 変更 B：`explanatory-must-not-for-clarity` の確認（変更なし）

全プランで変更不要に合意。主述語が SHOULD であり MUST NOT は例示。
変更 A 実施後に整合性を確認する。

### 6.4 変更 C：順序調整（変更 A に含む）

A-1 を `prohibitions.items` の末尾に追加することで完了。

### 6.5 `prohibitions.override` の適用範囲（確認不要）

Composer 案が「問題なし」と判定し、r2 で未解決事項から削除済み。
`prohibitions.override` は `authoring_obligations` を上書き対象に含み、
A-1（prohibition）と A-2（authoring_obligations）は補完関係にあり矛盾しない。

### 6.6 変更量の評価

| 変更 | 対象 | 影響範囲 |
|---|---|---|
| A-1: 新ルール追加 | `prohibitions.items` 末尾 | 1 ルールレコード追加 |
| A-2: statement 書き換え | `authoring_obligations.explanatory-must-not-permitted` | statement + verification のみ変更 |
| B: 確認のみ | なし | 変更なし |

---

## 7. 実施計画

### 7.1 Phase 1：meta-circular 遵守の回復

| Tier | 内容 |
|---|---|
| **Tier 0（構造確認）** | SKILL.md の全 rule record を列挙し、規範オペレータ判定手続き（2.3）で違反リストを最新化。先行実装の存在を確認。 |
| **Tier 1（変更実施）** | 変更 A（A-1 追加 + A-2 書き換え）を実施。 |
| **Tier 2（客観的検証）** | YAML パース検証、構造検証、`prohibitions-dedicated-section` 遵守確認、`one-obligation-per-rule` 遵守確認、rule-record スキーマ確認。 |
| **Tier 3（主観的品質確認）** | 変更後の記述が意図を保持しているか、人間レビューで確認。 |

### 7.2 Phase 2：`prohibitions` セクションの序盤移動（別タスク）

lost-in-the-middle 対策の補助的強化として、YAML ブロック内で `prohibitions` を
`interpretation` および `precedence_and_conflict` の直後に移動する。

- Phase 1 完了後の別タスクとして扱う。
- Semantic Gravity Wells の知見から、移動の効果は補助的なものと評価する。
  verification メソッドの強化と組み合わせることが重要。

### 7.3 受け入れ基準（Phase 1）

1. `prohibitions.items` 以外の全 rule record で `statement` の規範オペレータが MUST NOT でない。
2. 全 rule record で `statement` に規範述語が 1 つのみ。
3. YAML が標準パーサで正常解析可能。
4. 全 rule record が rule-record スキーマに適合。
5. `explanatory-must-not-permitted` と `no-treat-explanatory-must-not-as-prohibition` 間に意味的矛盾がない。

---

## 8. 未解決・検討継続事項

### 8.1 `definitions.tier-separation` の prohibition 化

現状は説明的使用として許容。将来 `no-interleave-tiers` を prohibitions に追加し、
definitions から参照する形への整理は別タスク候補。

### 8.2 他の AI directive files への展開

現時点では `.agents/skills/` 配下にスキルは 1 ファイルのみ。
ファイルが増えた場合に同じ Medium 強度を適用するか、authoring スキルへの参照に統一するか決定する。

### 8.3 Semantic Gravity Wells の緩和策の具体化

「禁止対象を直接名指しする代わりに望ましい状態を肯定的に記述する」等のガイドライン追加は、
AI directive files の記述スタイルとして priming リスクを低減する有用な方向性。別タスク。

### 8.4 規範オペレータ判定の lint 化

セクション 2.3 の判定手続きを機械実行可能な linter として実装することで、
`verification-machine-checkable` の充足度が向上する。
Codex 案の `statement_modal` フィールド導入も同方向の将来検討事項。

### 8.5 `non-prohibition-must-not-annotated` ルールの将来評価

先行実装で追加されたこのルールは、既存の `prohibitions-dedicated-section` +
`explanatory-must-not-permitted` との意味的重複がある。
スキルファイルが増加した段階で有用性を再評価する（Opus 案の指摘）。

---

## 付録 A：6 プラン間の主要な合意点・分岐点サマリー

### 完全合意（6/6）

- Medium 強度の推奨
- Strict の不採用
- `explanatory-must-not-permitted` が唯一の確定違反
- 分割アプローチ（A-1 prohibition + A-2 obligation 書き換え）
- 最小変更・最大整合の原則
- YAML パース検証・構造検証の必要性

### 多数合意（4/6 以上）

- 「確立されている」の表現抑制（r1 のみ楽観的。r2 で修正済み、GPT・Opus・Codex も同方向）
- 規範オペレータの構文的判定手続き化（r2・GPT・Opus・Codex。r1・Composer は自然言語的）
- Phase 2 の明示化（r2・Composer・Codex。GPT・r1 は別タスク扱い。Opus は効果限定的と注記）

### 分岐点（プラン固有）

- **Semantic Gravity Wells の統合**：Opus 案で初導入、r2 に統合。他プランでは言及なし。
  本プランでは統合を採用（研究の実在が確認済み）。
- **先行実装の評価**：Opus 案のみ。本プランでは方針レベルでの推奨を記載。
- **`statement_modal` フィールド**：Codex 案のみ。本プランでは将来検討事項に。
- **A-2 の "does not constitute" vs "MUST be classified"**：
  r1・Composer は前者、r2・Opus は後者。本プランでは後者を採用。
