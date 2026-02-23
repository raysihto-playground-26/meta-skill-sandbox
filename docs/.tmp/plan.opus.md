# MUST NOT 集中セクション方針および authoring スキル修正計画

作成日: 2026-02-23
対象ファイル: `.agents/skills/meta-skill.ai-directive-files-authoring/SKILL.md`
ステータス: 変更方針プラン（実装前）

> **ファイルパスについて**: `.agents/skills/` が実体ディレクトリであり、
> `.cursor/skills/`, `.claude/skills/`, `.github/skills/`, `.agent/skills/`,
> `.gemini/skills/`, `.opencode/skills/`, `.windsurf/skills/` はすべて
> `../.agents/skills` へのシンボリックリンクである。
> 本文書では実体パス `.agents/skills/` を正規パスとして使用する。

---

## 0. 本文書の位置づけ

本文書は、先行する草案（以下「現考案」）の分析結果を踏まえ、
研究的根拠の補完・違反箇所の精査・修正方針の統合を行った変更方針プランである。

現考案の優れた点を継承しつつ、以下の課題を修正・補完する:

- 研究的根拠における重要な反証（Semantic Gravity Wells）の欠落
- 適用強度 Medium の定義の精密化
- 先行実装（本ブランチの前回コミット）との整合性の回復
- 結論の確立度評価の補正

---

## 1. MUST NOT 集中セクションの有効性: 研究的根拠と設計論的規範

### 1.1 LLM のコンテキスト処理と "lost-in-the-middle" 現象

大規模言語モデル（LLM）は、長いコンテキスト内の情報を均等に処理しない。
先行研究（Liu et al. 2023 など）が示す **"lost-in-the-middle"** 現象では、
プロンプトの先頭部分と末尾部分の情報が、中間部分と比較して有意に強く活性化される。

この非線形な注意分布は、AI directive files の設計に直接の含意を持つ:

- **禁止事項（MUST NOT）は失敗コストが高い**: 生成途中で禁止違反が起きると取り消しが困難。
- **正の制約（MUST）は生成を誘導する**: モデルは正の目標に向けて生成しようとする自然な傾向を持つ。
- **禁止事項が中間に埋もれると遵守率が下がる**: 長い指示の中でコンテキストの中間に配置された
  禁止事項は、先頭・末尾に比べて忘却・無視されやすい。

### 1.2 指示階層（Instruction Hierarchy）の実証知見

OpenAI の "Instruction Hierarchy" 研究（Wallace et al. 2024）や
Anthropic の Constitutional AI に関する知見は、次を支持する:

- 制約は**明示的・独立的・早期配置**の場合に最も遵守される。
- 制約が他のコンテンツに埋め込まれると、モデルの注意が薄れ、遵守率が低下する。
- **禁止のカテゴリを一カ所に集め、早期に提示する**設計は、
  生成開始前に禁止事項をワーキングメモリ相当の領域に保持させる効果があると推論される。

**補足（命令階層の限界）**: OpenReview 2025 の研究では、system/user プロンプト分離ですら
命令階層の安定的な確立に失敗し、モデルが「制約タイプに対する本質的なバイアス」を持ち
優先度指定を無視する傾向が確認されている。
「ワーキングメモリ相当の領域に保持させる効果」は合理的推論であるが、
直接の実証データに基づく結論ではない点に留意が必要である。

### 1.3 Semantic Gravity Wells: 否定制約の逆活性化リスク

**現考案に欠落していた重要な反証。**

Semantic Gravity Wells（arXiv 2601.08070, 2026）は、否定制約が LLM で失敗する
メカニズムを特定した研究であり、MUST NOT 集中セクションの設計に直接の含意を持つ:

- **Priming Failure（違反の 87.5%）**: 禁止対象を**明示的に言及すること自体が、
  その対象を抑制するのではなく逆に活性化する**。
  「X をしてはならない」と記述することで、モデルは X を強く想起する。
- **Override Failure（違反の 12.5%）**: 後段の FFN 層が禁止トークンへの正の寄与
  （+0.39）を生成し、前段の抑制シグナルを約 4 倍の強度で上書きする。
- **抑制の非対称性**: 成功時は 22.8 ポイントの確率低減、失敗時はわずか 5.2 ポイント
  （4.4 倍の非対称性）。層 23-27 が制約効果の因果的責任を持つ。

**設計への含意**:

- MUST NOT を集中セクションに「並べるだけ」では、priming effect により
  禁止対象を繰り返し活性化するリスクがある。
- 緩和策として、(a) 事後検証（verification）による担保、
  (b) 禁止対象の直接名指しを最小化する記述スタイルが推奨される。
- **配置戦略は遵守率向上の手段であって保証ではなく、
  verification メソッドによる事後検証こそが真の遵守保証である。**

### 1.4 規範論・仕様設計論からの観点

法令・技術仕様書（RFC、法律条文、セキュリティポリシー等）の設計慣行でも、
禁止事項は独立した条項・セクションとして前置される:

- RFC 2119 は MUST NOT を MUST と同格の normative keyword として定義し、
  仕様文書の構造的明確性を求める。
- 法律条文では「禁止行為の列挙」が「義務の列挙」よりも厳格に管理される傾向がある。
- セキュリティポリシーでは "deny-by-default" の原則として禁止事項を先頭に置く設計が標準。

### 1.5 結論: 確立度の評価

| 観点                                       | 確立度 | 備考                                                    |
| ------------------------------------------ | ------ | ------------------------------------------------------- |
| LLM 注意メカニズム（lost-in-middle）の実証 | 高     | 複数の独立研究で再現                                    |
| 禁止事項の早期配置が遵守率を高める         | 中〜高 | 実証は直接的ではないが、lost-in-middle から合理的に導出 |
| 独立セクション化による明瞭性向上           | 高     | 仕様設計論・法令設計論で確立                            |
| MUST NOT の明示的言及による逆活性化リスク  | 高     | Semantic Gravity Wells (2026): priming failure 87.5%    |
| 構造化 + 事後検証の組合せ                  | 高     | 配置だけでなく verification による担保が必須            |
| 「どれだけ早期に配置するか」の最適点       | 中     | 先頭付近が望ましいが定量的最適点は未確定                |

**総合評価**: MUST NOT を独立した専用セクションとしてファイルの序盤に集約する設計は、
LLM の処理特性・仕様設計論・実証研究から**合理的な慣行として支持される**。
ただし、Semantic Gravity Wells の知見により、「集中配置すれば遵守率が上がる」は
単純には成り立たず、**「構造化された専用セクション + 事後検証（verification）」の
複合的アプローチとして確立されている**と評価すべきである。
「集めれば効く」という単純命題は確立されていない。

---

## 2. 適用強度の選択

### 2.1 強度の段階

| 強度レベル | 内容                                                                                                                                                                                                                                                 |
| ---------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Weak**   | SHOULD be in a dedicated section。例外が広く認められる。                                                                                                                                                                                             |
| **Medium** | 規範的 MUST NOT（rule record の statement フィールドの主述語が MUST NOT であるもの）はすべて `prohibitions` に置く。説明的 MUST NOT（interpretation, definitions, verification フィールド内、および statement フィールドで主述語でないもの）は許容。 |
| **Strong** | あらゆる rule record の statement フィールドに含まれる MUST NOT はセクションを問わず `prohibitions` に移動する。                                                                                                                                     |
| **Strict** | ファイル全体を通じ MUST NOT のテキストが `prohibitions` セクション以外に現れることを禁じる。                                                                                                                                                         |

### 2.2 推奨強度と根拠

**推奨強度: Medium（MUST として適用）**

理由:

- `explanatory-must-not-permitted` / `explanatory-must-not-for-clarity` の両ルールが示すとおり、
  MUST NOT という語の出現と「規範的禁止」の出現は区別される。
- interpretation、definitions、failure_states_and_degradation などのフィールド内の MUST NOT は
  **説明的（explanatory）** であり、これらを `prohibitions` に引き上げると:
  - 説明文にルールレコードスキーマを適用する必要が生じ、ファイル構造が肥大化する。
  - 「何が normative か」の境界が曖昧になり、かえって遵守確認が困難になる。
- **Strong** や **Strict** は、説明的 MUST NOT の排除または構造的オーバーヘッドを生むため、
  ファイルの可読性・保守性が低下し、効果は Medium を大きく超えない。
- Semantic Gravity Wells の知見からも、MUST NOT の出現箇所を過剰に増やす
  （Strong/Strict による prohibition レコードの膨張）は priming リスクを増大させる。

### 2.3 Medium 強度の操作的定義

> rule record の `statement` フィールドが **MUST NOT を主述語として含む**場合、
> そのルールは `prohibitions.items` に配置しなければならない（MUST）。
>
> `statement` フィールドで MUST NOT が主述語でなく参照・列挙・例示として登場する場合、
> および rule record 外のフィールド（description, behavior, degradation, verification 等）
> に MUST NOT が登場する場合は、説明的使用として扱い `prohibitions` への移動を要しない。

**「主述語」の判定基準**: statement の文構造において、MUST NOT が文の述語動詞を
修飾している（文の主たる義務・禁止を表明している）場合を主述語とする。
括弧内での言及（例: `(MUST NOT)`）、例示内での列挙（例: `e.g. ... MUST NOT ...`）、
主語の説明としての登場（例: `All normative prohibitions (MUST NOT) MUST ...`）は
主述語に該当しない。

---

## 3. 現状の authoring スキルにおける meta-circular 非遵守箇所

### 3.1 調査方法

SKILL.md 全体を通じ、`statement` フィールドに MUST NOT が含まれるルールを列挙し、
そのルールが属するセクションと MUST NOT の文法的役割を確認した。

### 3.2 確定違反

#### 違反 1: `explanatory-must-not-permitted` の配置

| 項目           | 値                                                                                                                                                                                                                                     |
| -------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ルール ID      | `explanatory-must-not-permitted`                                                                                                                                                                                                       |
| 所属セクション | `authoring_obligations`                                                                                                                                                                                                                |
| statement      | "When describing interpretation, semantics, or verification (as opposed to primary normative statement fields), descriptive use of the phrase MUST NOT is allowed and **MUST NOT be treated** as additional enforceable prohibitions." |
| 違反内容       | statement フィールドの主述語に MUST NOT が含まれるが、`prohibitions` セクションに配置されていない                                                                                                                                      |
| 参照ルール     | `prohibitions-dedicated-section`: "All normative prohibitions (MUST NOT) MUST be in a dedicated section."                                                                                                                              |

#### 副次的問題: `explanatory-must-not-permitted` の複合述語

| 項目       | 値                                                                                                                                                                                                                                                                                             |
| ---------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ルール ID  | `explanatory-must-not-permitted`                                                                                                                                                                                                                                                               |
| 問題内容   | statement が "is allowed"（許可）と "MUST NOT be treated"（禁止）の 2 つの述語を含む                                                                                                                                                                                                           |
| 参照ルール | `one-obligation-per-rule`: "Every enforceable rule MUST be one obligation per rule."                                                                                                                                                                                                           |
| 解釈の余地 | "is allowed" を MAY（許可）と読めば MUST/MUST NOT 述語は 1 つのみであり、形式的には `one-obligation-per-rule` の検証基準（"Each rule has exactly one MUST or one MUST NOT predicate"）を満たす。ただし、"is allowed" の曖昧性自体が `no-ambiguous-modals` の精神に反するため、分割が望ましい。 |

### 3.3 非違反の確認（statement に MUST NOT を含むが主述語でないケース）

| ルール ID                            | セクション              | MUST NOT の出現形態                  | 判定       |
| ------------------------------------ | ----------------------- | ------------------------------------ | ---------- |
| `explanatory-must-not-for-clarity`   | `authoring_obligations` | 主語として登場。主述語は SHOULD。    | **非違反** |
| `use-normative-keywords`             | `authoring_obligations` | RFC keywords の列挙。主述語は MUST。 | **非違反** |
| `prohibitions-dedicated-section`     | `authoring_obligations` | 括弧内の説明。主述語は MUST。        | **非違反** |
| `non-prohibition-must-not-annotated` | `authoring_obligations` | 主語/条件として登場。主述語は MUST。 | **非違反** |
| `define-conflict-policy`             | `authoring_obligations` | 例示内。主述語は MUST。              | **非違反** |

### 3.4 rule record 外の MUST NOT（説明的使用として許容）

以下は rule record の statement フィールド以外に登場する MUST NOT であり、
`explanatory-must-not-permitted` が定義する許容範囲に該当する:

| 箇所                                                        | フィールド種別        | 現状のアノテーション                                                 |
| ----------------------------------------------------------- | --------------------- | -------------------------------------------------------------------- |
| `interpretation.unknown_keys`                               | interpretation prose  | なし（解釈意味論の文脈で許容）                                       |
| `interpretation.unspecified_behavior`                       | interpretation prose  | `(see no-assume-unspecified)` 相互参照あり（先行実装で追加）         |
| `precedence_and_conflict.conflict_policy.MUST_vs_MUST`      | conflict policy prose | `(see no-silent-conflict-resolution)` 相互参照あり（先行実装で追加） |
| `failure_states_and_degradation.failure_states[0].behavior` | behavior prose        | `(see no-invent)` 相互参照あり（元から存在）                         |
| `failure_states_and_degradation.degradation`                | degradation prose     | `(see no-assume-compliance)` 相互参照あり（先行実装で追加）          |
| `definitions.tier-separation.description`                   | definition prose      | なし（定義的文脈で許容）                                             |
| `one-obligation-per-rule` の verification                   | verification field    | なし（メタ言語的・検証文脈で許容）                                   |

---

## 4. 先行実装（本ブランチ前回コミット）の評価

### 4.1 先行実装の内容

本ブランチの前回コミット `23a7787` で以下の変更が行われた:

| 変更 | 内容                                                                                                          |
| ---- | ------------------------------------------------------------------------------------------------------------- |
| A    | `no-assume-unspecified` prohibition レコード追加（`interpretation.unspecified_behavior` の MUST NOT を抽出）  |
| B    | `no-silent-conflict-resolution` prohibition レコード追加（`conflict_policy.MUST_vs_MUST` の MUST NOT を抽出） |
| C    | `no-assume-compliance` prohibition レコード追加（`degradation` の MUST NOT を抽出）                           |
| D    | 上記 A〜C に対応するインライン `(see prohibition-id)` 相互参照追加                                            |
| E    | `non-prohibition-must-not-annotated` authoring ルール追加                                                     |

### 4.2 Medium 強度基準での評価

| 変更 | Medium での必要性 | 理由                                                                                                                                                                     |
| ---- | ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| A〜C | **不要**          | 元の MUST NOT は rule record の statement フィールドではなく、interpretation/conflict_policy/degradation のフリーテキスト内。Medium 定義では説明的使用として許容される。 |
| D    | **不要**          | `explanatory-must-not-permitted` が既にこれらを許容。相互参照は有益だが meta-circularity 回復には無関係。                                                                |
| E    | **不要**          | 既存の `prohibitions-dedicated-section` + `explanatory-must-not-permitted` で十分にカバーされる問題域を新ルールで再定義。                                                |

### 4.3 先行実装が解決していない核心的違反

**`explanatory-must-not-permitted` の statement に MUST NOT が主述語として残っている。**
先行実装は interpretation/definitions/failure_states の MUST NOT に対処したが、
authoring_obligations 内の rule record statement における唯一の真の違反を修正していない。

### 4.4 先行実装の処分方針

| 選択肢                         | 内容                                                                                                             | 評価                                                                                                                                                  |
| ------------------------------ | ---------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| **A: 維持 + 核心修正を追加**   | 先行変更を残し、`explanatory-must-not-permitted` の分割を追加実施                                                | prohibition レコードとして有害ではなく、暗黙の制約を明示化した価値がある。Medium を超えるが構造的に整合する。相互参照はトレーサビリティを向上させる。 |
| **B: 巻き戻し + 核心修正のみ** | 先行コミットを revert し、現考案の最小変更のみ適用                                                               | 最小変更原則に最も合致。ただし有用な明示化が失われる。                                                                                                |
| **C: 部分維持 + 核心修正**     | 3 prohibition は維持、`non-prohibition-must-not-annotated` は削除、`explanatory-must-not-permitted` の分割を実施 | バランス型。ただし `non-prohibition-must-not-annotated` の削除はそれを参照する他のルールがないか確認が必要。                                          |

**推奨: 選択肢 A（維持 + 核心修正を追加）**

理由:

- 先行実装の 3 prohibition レコードは、暗黙の制約を明示的な構造化レコードにしたものであり、
  `design-assume-probabilistic`（指示遵守は確率的）の精神に沿う。
- 相互参照は `explanatory-must-not-permitted` だけでは保証されないトレーサビリティを提供する。
- 巻き戻しは git 履歴に不要なノイズを生む。
- `non-prohibition-must-not-annotated` は、既存ルールとの重複があるものの、
  Medium 定義を明示的にルールとして記述している点で、将来のスキルファイル作成時の指針となる。

---

## 5. 現考案の課題一覧

現考案（先行する草案ドキュメント）について特定された課題を以下にまとめる。

### 5.1 研究的根拠の欠落

| ID  | 課題                                                           | 重大度 | 詳細                                                                                                                                 |
| --- | -------------------------------------------------------------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------ |
| D-1 | Semantic Gravity Wells（arXiv 2601.08070, 2026）への言及がない | **高** | MUST NOT 集中配置の最も重要な反証。priming failure（87.5%）による逆活性化リスクが考慮されておらず、結論の確立度評価が楽観的すぎる。  |
| D-2 | 命令階層の限界への言及がない                                   | 中     | 「ワーキングメモリ相当の領域に保持させる効果がある」を直接の実証データに基づく結論として記述しているが、合理的推論として明記すべき。 |

### 5.2 結論の評価

| ID  | 課題                               | 重大度 | 詳細                                                                                                                                        |
| --- | ---------------------------------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------- |
| D-3 | 「確立されている」の範囲が広すぎる | 中     | 「合理的かつ効果的な慣行として確立されている」は、「構造化 + 事後検証の複合として確立」に限定すべき。配置のみによる効果は確立されていない。 |

### 5.3 ファイルパスの事実誤認

| ID  | 課題                                                                                             | 重大度 | 詳細                                                                                     |
| --- | ------------------------------------------------------------------------------------------------ | ------ | ---------------------------------------------------------------------------------------- |
| D-4 | 対象ファイルパスが `.agents/skills/...` ではなく `.cursor/skills/...` と記載されている箇所がある | 低     | `.agents/skills/` が実体。`.cursor/skills/` はシンボリックリンク。正規パスを使用すべき。 |

### 5.4 先行実装との非整合

| ID  | 課題                             | 重大度 | 詳細                                                                                                                                                                |
| --- | -------------------------------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| D-5 | 現考案は先行実装を考慮していない | 中     | 本ブランチの前回コミットで追加された 3 prohibition レコード・相互参照・authoring ルールが分析対象に含まれていない。修正計画は先行実装との整合を考慮する必要がある。 |

### 5.5 修正方針自体の課題

| ID  | 課題                                                                      | 重大度 | 詳細                                                                                                                                                                                                                                                                                            |
| --- | ------------------------------------------------------------------------- | ------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| D-6 | 変更 A-2 の statement 書き換え案が `no-ambiguous-modals` に抵触する可能性 | 低     | 現考案の A-2 案 "is classified as explanatory and does not constitute an enforceable prohibition" の "does not constitute" は否定的断言であり、MUST/MUST NOT/SHOULD のいずれにも該当しない。`use-normative-keywords` が要求する RFC-style normative keywords の使用に照らして妥当か確認が必要。 |

---

## 6. 統合修正方針

### 6.1 核心修正: `explanatory-must-not-permitted` の分割

現考案の変更 A を採用し、先行実装との整合を確保する。

#### 変更 1: 新規 prohibition レコード追加

`prohibitions.items` の末尾に追加:

```yaml
- id: "no-treat-explanatory-must-not-as-prohibition"
  layer: L2
  priority: 92
  statement: "MUST NOT treat descriptive uses of the phrase 'MUST NOT' in interpretation, semantics, definitions, or verification fields as additional enforceable prohibitions."
  conditions: ["creating AI directive file", "editing AI directive file"]
  exceptions: ["none"]
  verification: "Descriptive uses of MUST NOT in non-statement fields are not modeled or enforced as separate prohibition rules."
```

#### 変更 2: `explanatory-must-not-permitted` の statement 書き換え

`authoring_obligations` に残留する `explanatory-must-not-permitted` の statement を、
MUST NOT を主述語として含まない形に書き換える:

```yaml
- id: "explanatory-must-not-permitted"
  layer: L2
  priority: 92
  statement: "Descriptive use of the phrase MUST NOT in interpretation, semantics, definitions, or verification text (as opposed to primary normative statement fields) MUST be classified as explanatory; enforcement as a separate prohibition is governed by no-treat-explanatory-must-not-as-prohibition."
  conditions: ["creating AI directive file", "editing AI directive file"]
  exceptions: ["none"]
  verification: "Descriptive uses of MUST NOT in interpretation, semantics, definitions, or verification text are classified as explanatory and cross-reference no-treat-explanatory-must-not-as-prohibition for enforcement."
```

> **現考案の D-6 課題への対処**: 現考案の A-2 案（"does not constitute"）を採用せず、
> "MUST be classified as explanatory" という肯定的義務 + prohibition への相互参照とすることで、
> `use-normative-keywords` との整合性を確保する。

#### 変更 3: 先行実装の変更は維持

先行実装で追加された以下の要素は維持する（セクション 4.4 の推奨 A に基づく）:

- `no-assume-unspecified`, `no-silent-conflict-resolution`, `no-assume-compliance`（prohibition レコード）
- インライン `(see prohibition-id)` 相互参照
- `non-prohibition-must-not-annotated`（authoring ルール）

### 6.2 確認事項（変更不要だが検証が必要）

| 対象                               | 確認内容                                                                                                                                                                                             |
| ---------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `explanatory-must-not-for-clarity` | 変更 1・2 の後、両ルールの整合性を確認。主述語が SHOULD のため変更不要。                                                                                                                             |
| `prohibitions.override` の適用範囲 | override は `authoring_obligations` を含むことを確認。`no-treat-explanatory-must-not-as-prohibition` が `authoring_obligations` に残留する `explanatory-must-not-permitted` と矛盾しないことを確認。 |
| YAML パース検証                    | 変更後に `yaml-parse-validation` が成功することを確認。                                                                                                                                              |

---

## 7. 変更後の meta-circular 遵守状態

### 7.1 変更後の状態

変更 1〜3 実施後、以下の条件がすべて満たされる:

1. **`prohibitions.items` 以外のすべての rule record において、
   `statement` フィールドの主述語が MUST NOT でない。**
   - `explanatory-must-not-permitted` の statement は "MUST be classified"（MUST、肯定的義務）に変更済み。
   - その他の非違反ケース（3.3 節）は変更なし。

2. **`explanatory-must-not-permitted` が定義する「説明的 MUST NOT」の許容範囲が
   ファイル内に整合的に適用されている。**
   - rule record 外のすべての MUST NOT（3.4 節）は説明的使用として許容。

3. **`one-obligation-per-rule` がすべてのルールで満たされている。**
   - 分割前の 2 述語問題が解消（`explanatory-must-not-permitted` → 1 MUST 述語、
     `no-treat-explanatory-must-not-as-prohibition` → 1 MUST NOT 述語）。

### 7.2 変更量の評価

| 変更                  | 対象                                                   | 影響範囲                                    |
| --------------------- | ------------------------------------------------------ | ------------------------------------------- |
| 1: 新ルール追加       | `prohibitions.items`                                   | 1 ルールレコードの追加                      |
| 2: 既存ルール書き換え | `authoring_obligations.explanatory-must-not-permitted` | statement + verification フィールドのみ変更 |
| 3: 先行実装維持       | なし                                                   | 変更なし                                    |
| 確認: 整合性検証      | ファイル全体                                           | 変更なし（検証のみ）                        |

---

## 8. 実施手順

### 8.1 推奨実施順序

1. **Tier 0（構造確認）**: 現在のファイル状態を再確認し、
   先行実装の変更が正しく存在することを検証する。
2. **Tier 1（変更実施）**: 変更 1（prohibition 追加）+ 変更 2（statement 書き換え）を実施する。
3. **Tier 2（客観的検証）**:
   - YAML パース検証（yaml-parse-validation）を実施する。
   - 構造検証（structure-validation）を実施する。
   - meta-circular 確認: `prohibitions-dedicated-section` の遵守を確認する。
   - `one-obligation-per-rule` の遵守を確認する。
   - 全 rule record が rule-record schema（id, layer, priority, statement,
     conditions, exceptions, verification）に適合することを確認する。
4. **Tier 3（主観的品質確認）**: 変更後の記述が意図を保持しているか、
   レビューで確認する。

### 8.2 受け入れ基準

- `prohibitions.items` 以外のすべての rule record において `statement` 主述語が MUST NOT でない。
- YAML が標準パーサで正常に解析できる。
- rule record スキーマが全ルールで維持されている。
- `explanatory-must-not-permitted` と `no-treat-explanatory-must-not-as-prohibition` の間で
  意味的な矛盾がない。

---

## 9. 未解決・検討継続事項

1. **`prohibitions` セクションの位置**: 現状は YAML ブロックの中ほど
   （interpretation → precedence → failure_states → definitions の後）に配置されている。
   lost-in-the-middle 対策を最大化するなら `interpretation` の直後への移動が理論的に望ましいが、
   Semantic Gravity Wells の知見から位置移動の効果は限定的であり、
   事後検証の方が信頼性が高い。大きな構造変更であり、別タスクとして扱うべきか要検討。

2. **他の AI directive files への展開**: 本リポジトリにスキルファイルが複数存在する場合、
   同様の分析を全ファイルに適用するか方針を確定する必要がある。
   現時点では `.agents/skills/` 配下にスキルは 1 ファイルのみ。

3. **`non-prohibition-must-not-annotated` ルールの将来的な評価**:
   先行実装で追加されたこのルールは、既存の `prohibitions-dedicated-section` +
   `explanatory-must-not-permitted` との意味的重複がある。
   スキルファイルが増加した段階で、このルールが実際に有用なガードレールとなっているか、
   あるいは冗長であるかを評価し、必要に応じて統合または削除を検討する。

4. **Semantic Gravity Wells の緩和策の具体化**: 本プランでは研究結果を根拠セクションに
   統合したが、AI directive files の記述スタイルとして priming リスクを具体的にどう
   低減するか（例: 「禁止対象を直接名指しする代わりに望ましい状態を肯定的に記述する」
   ガイドラインの追加）は、別タスクとして検討する価値がある。
