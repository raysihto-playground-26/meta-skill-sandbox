# MUST NOT 集中セクション方針および authoring スキル修正計画

作成日: 2026-02-23  
対象ファイル: `.agents/skills/meta-skill.ai-directive-files-authoring/SKILL.md`  
ステータス: 草案（具体的な変更なし）

---

## 1. MUST NOT 集中セクションの有効性：研究上の根拠と設計論的規範

### 1.1 LLM のコンテキスト処理と "lost-in-the-middle" 現象

大規模言語モデル（LLM）は、長いコンテキスト内の情報を均等に処理しない。
先行研究（Liu et al. 2023 など）が示す **"lost-in-the-middle"** 現象では、
プロンプトの先頭部分と末尾部分の情報が、中間部分と比較して有意に強く活性化される。

この非線形な注意分布は、AI directive files の設計に直接の含意を持つ：

- **禁止事項（MUST NOT）は失敗コストが高い**：生成途中で禁止違反が起きると取り消しが困難。
- **正の制約（MUST）は生成を誘導する**：モデルは正の目標に向けて生成しようとする自然な傾向を持つ。
- **禁止事項が中間に埋もれると遵守率が下がる**：長い指示の中でコンテキストの中間に配置された禁止事項は、
  先頭・末尾に比べて忘却・無視されやすい。

### 1.2 指示階層（Instruction Hierarchy）の実証知見

OpenAI の "Instruction Hierarchy" 研究（Wallace et al. 2024）や
Anthropic の Constitutional AI に関する知見は、次を支持する：

- 制約は**明示的・独立的・早期配置**の場合に最も遵守される。
- 制約が他のコンテンツに埋め込まれると（例：長い説明文の末尾や中間）、
  モデルの注意が薄れ、遵守率が低下する。
- **禁止のカテゴリを一カ所に集め、早期に提示する**設計は、
  生成開始前に禁止事項をワーキングメモリ相当の領域に保持させる効果がある。

### 1.3 規範論・仕様設計論からの観点

法令・技術仕様書（RFC、法律条文、セキュリティポリシー等）の設計慣行でも、
禁止事項は独立した条項・セクションとして前置される：

- RFC 2119 は MUST NOT を MUST と同格の normative keyword として定義し、
  仕様文書の構造的明確性を求める。
- 法律条文では「禁止行為の列挙」が「義務の列挙」よりも厳格に管理される傾向がある。
- セキュリティポリシーでは "deny-by-default" の原則として禁止事項を先頭に置く設計が標準。

### 1.4 結論：確立度の評価

| 観点 | 確立度 | 備考 |
|------|--------|------|
| LLM 注意メカニズム（lost-in-middle）の実証 | 高 | 複数の独立研究で再現 |
| 禁止事項の早期配置が遵守率を高める | 中〜高 | 実証は直接的ではないが、lost-in-middle から合理的に導出される |
| 独立セクション化による明瞭性向上 | 高 | 仕様設計論・法令設計論で確立 |
| 「どれだけ早期に配置するか」の最適点 | 中 | ファイル先頭付近（frontmatter 直後）が望ましいが、定量的な最適点は未確定 |

**総合評価**：MUST NOT を独立した専用セクションとしてファイルの序盤に集約する設計は、
LLM の処理特性・仕様設計論・実証研究の三つの観点から**合理的かつ効果的な慣行として確立されている**と判断してよい。

---

## 2. 適用強度の選択

### 2.1 強度の段階

| 強度レベル | 内容 |
|-----------|------|
| **Weak**（推奨） | SHOULD be in a dedicated section。例外が広く認められる。 |
| **Medium**（現状の SKILL.md の意図） | 規範的 MUST NOT（rule record の statement フィールドが MUST NOT で始まるもの）はすべて `prohibitions` に置く。説明的 MUST NOT（interpretation, definitions, verification フィールド内のもの）は許容。 |
| **Strong** | あらゆる rule record の statement フィールドに含まれる MUST NOT はセクションを問わず `prohibitions` に移動する。 |
| **Strict** | ファイル全体を通じ MUST NOT のテキストが `prohibitions` セクション以外に現れることを禁じる。 |

### 2.2 推奨強度と根拠

**推奨強度：Medium（現状の SKILL.md に定義された意図を維持・徹底）**

理由：
- `explanatory-must-not-permitted` / `explanatory-must-not-for-clarity` の両ルールが示すとおり、
  MUST NOT という語の出現と「規範的禁止」の出現は区別される。
- interpretation、definitions、failure_states_and_degradation などのフィールド内の MUST NOT は
  **説明的（explanatory）** であり、これらを `prohibitions` に引き上げると：
  - 説明文（behavior, description, degradation フィールド）にルールレコードスキーマを適用する
    必要が生じ、ファイル構造が肥大化する。
  - 「何が normative か」の境界が曖昧になり、かえって遵守確認が困難になる。
- **Strong** や **Strict** は、説明的 MUST NOT の排除または構造的オーバーヘッドを生むため、
  ファイルの可読性・保守性が低下し、効果は Medium を大きく超えない可能性が高い。

**適用の境界線（Medium 強度の定義）**：

> rule record の `statement` フィールドが **MUST NOT を主述語として含む**場合、
> そのルールは `prohibitions.items` に配置しなければならない。
> `statement` フィールドで MUST NOT が主述語でなく参照・列挙・例示として登場する場合、
> および rule record 外のフィールド（description, behavior, degradation, verification など）
> に MUST NOT が登場する場合は、説明的使用として扱い `prohibitions` への移動を要しない。

---

## 3. 現状の authoring スキルにおける meta-circular 非遵守箇所の特定

### 3.1 調査方法

SKILL.md 全体を通じ `statement:` フィールドに MUST NOT が含まれるルールを列挙し、
そのルールが属するセクションを確認した。

### 3.2 特定された違反

#### 違反 1（確定）：`explanatory-must-not-permitted` の配置

| 項目 | 値 |
|------|-----|
| ルール ID | `explanatory-must-not-permitted` |
| 所属セクション | `authoring_obligations` |
| statement | `"When describing interpretation, semantics, or verification (as opposed to primary normative statement fields), descriptive use of the phrase MUST NOT is allowed and **MUST NOT be treated** as additional enforceable prohibitions."` |
| 違反内容 | statement フィールドの主述語に MUST NOT が含まれるが、`prohibitions` セクションに配置されていない |
| 参照ルール | `prohibitions-dedicated-section`: "All normative prohibitions (MUST NOT) MUST be in a dedicated section." |

#### 副次的問題：`explanatory-must-not-permitted` の複合述語

| 項目 | 値 |
|------|-----|
| ルール ID | `explanatory-must-not-permitted` |
| 違反内容 | statement が "is allowed" （MUST 相当の許可）と "MUST NOT be treated"（禁止）の **2つの述語**を含む |
| 参照ルール | `one-obligation-per-rule`: "Every enforceable rule MUST be one obligation per rule." |

### 3.3 境界ケース（違反非確定・要判断）

以下は statement フィールドに MUST NOT が現れるが、主述語ではない（説明的・列挙的）ため、
**現状定義では違反に該当しない**と判断されるケース：

| ルール ID | セクション | MUST NOT の出現形態 | 判定 |
|-----------|-----------|---------------------|------|
| `explanatory-must-not-for-clarity` | `authoring_obligations` | 例示・列挙（"e.g. listing RFC keywords, describing conflict policy..."）として登場。主述語は SHOULD。 | **非違反**（説明的使用） |
| `use-normative-keywords` | `authoring_obligations` | RFC keywords の列挙として登場。主述語は MUST。 | **非違反**（説明的使用） |
| `prohibitions-dedicated-section` | `authoring_obligations` | 主語の説明として登場（"All normative prohibitions (MUST NOT)"）。主述語は MUST。 | **非違反**（説明的使用） |

### 3.4 rule record 外の MUST NOT（説明的使用として許容）

以下は rule record の statement フィールド以外（description, behavior, degradation, binding 等）
に登場する MUST NOT であり、`explanatory-must-not-permitted` が定義する許容範囲に該当する：

- `interpretation.unknown_keys` の prose
- `interpretation.unspecified_behavior` の prose
- `precedence_and_conflict.conflict_policy.MUST_vs_MUST` の prose
- `failure_states_and_degradation.failure_states[0].behavior` の prose
- `failure_states_and_degradation.degradation` の prose
- `definitions.tier-separation.description` の prose

---

## 4. 目標設定

### 4.1 目指すべき状態

**Meta-circular 完全遵守状態の定義**：

> authoring スキルが定義するすべてのルールを、authoring スキル自身が遵守している状態。
> 具体的には：`prohibitions-dedicated-section` が要求する「normative MUST NOT はすべて `prohibitions` に」
> という制約を、authoring スキル自身が満たしている状態。

### 4.2 遵守の確認基準

以下の条件をすべて満たすこと：

1. `prohibitions.items` 以外のすべての rule record において、
   `statement` フィールドの主述語が MUST NOT でないこと。
2. `explanatory-must-not-permitted` ルールが定義する「説明的 MUST NOT」の許容範囲が
   ファイル内に整合的に適用されていること。
3. `one-obligation-per-rule` が要求する「1 ルール 1 述語」が、
   `explanatory-must-not-permitted` ルール自身においても満たされていること。

---

## 5. 修正方針

### 5.1 基本方針

**最小変更・最大整合**原則：既存の構造・ルール数・意図を変えず、
`explanatory-must-not-permitted` の記述をリファクタリングすることで meta-circular 遵守を回復する。

### 5.2 具体的な変更方針（変更の記述のみ、実装なし）

#### 変更 A：`explanatory-must-not-permitted` を分割する

現状の 1 ルール（2 述語）を、以下の 2 ルールに分割する：

**分割後ルール A-1（`prohibitions` セクションへ移動）**  
- id: `no-treat-explanatory-must-not-as-prohibition`  
- statement: "MUST NOT treat descriptive uses of the phrase 'MUST NOT' in interpretation, semantics, or verification fields as additional enforceable prohibitions."  
- layer: L2 / priority: 92  
- conditions: ["creating AI directive file", "editing AI directive file"]

**分割後ルール A-2（`authoring_obligations` に残留）**  
- id: `explanatory-must-not-permitted`  
- statement: "Descriptive use of the phrase MUST NOT in interpretation, semantics, or verification text (as opposed to primary normative statement fields) is classified as explanatory and does not constitute an enforceable prohibition."  
- layer: L2 / priority: 92  
- conditions: ["creating AI directive file", "editing AI directive file"]  
- ※ statement に MUST NOT を主述語として含まず、定義的・分類的な記述に変更。

#### 変更 B：`explanatory-must-not-for-clarity` の確認

`explanatory-must-not-for-clarity` は statement の主述語が SHOULD であり、
MUST NOT は例示として登場しているため、**変更不要**。
ただし、変更 A 後に両ルールの整合性を確認すること。

#### 変更 C：`prohibitions` セクション内の順序調整（推奨・任意）

移動した `no-treat-explanatory-must-not-as-prohibition` を、
`prohibitions.items` リストの末尾（既存 8 項目の後）に追加する。
これにより `prohibitions` セクションが「すべての normative MUST NOT」の単一ソースとなる。

### 5.3 変更量の評価

| 変更 | 対象 | 影響範囲 |
|------|------|---------|
| A-1: 新ルール追加 | `prohibitions.items` | 1 ルールレコードの追加 |
| A-2: 既存ルール statement 書き換え | `authoring_obligations.explanatory-must-not-permitted` | statement フィールドのみ変更 |
| B: 確認のみ | なし | 変更なし |
| C: 順序調整 | `prohibitions.items` の末尾 | A-1 の配置位置 |

---

## 6. 適用強度についての最終方針

### 6.1 「どこまでの強さで適用するか」への回答

**Medium 強度を MUST（強制）として適用する。**

具体的な適用ルール：

> - rule record の `statement` フィールドで MUST NOT が **主述語**である場合：
>   そのルールは必ず `prohibitions.items` に置かなければならない（MUST）。
> - `statement` フィールドで MUST NOT が参照・列挙・例示として登場する場合：
>   `prohibitions` への移動は必要なく、説明的使用として許容される（explanatory use）。
> - rule record 外のフィールド（description, behavior, degradation, verification 等）での MUST NOT：
>   許容される（`explanatory-must-not-permitted` ルールの適用範囲）。

### 6.2 Strict 強度を採用しない理由

- interpretation、definitions、failure_states_and_degradation 等のフィールドに登場する
  MUST NOT をすべて `prohibitions` に移動するには、それらをすべて rule record に昇格させる必要がある。
- これは SKILL.md の構造を大幅に変更し、ファイルサイズを増大させ、可読性を低下させる。
- lost-in-the-middle の軽減効果は Medium 強度で大部分を達成できるため、
  Strict 強度の追加効果は小さい。

---

## 7. 実施優先度・手順

### 7.1 推奨実施順序

1. **Tier 0（構造確認）**：SKILL.md の全 rule record を列挙し、
   `statement` フィールドで MUST NOT が主述語である全ルールを確定リスト化する。
2. **Tier 1（変更実施）**：変更 A（A-1 新規追加 + A-2 statement 書き換え）を実施する。
3. **Tier 2（整合性検証）**：
   - YAML パース検証（yaml-parse-validation）を実施する。
   - 構造検証（structure-validation）を実施する。
   - meta-circular 確認：`prohibitions-dedicated-section` の遵守を確認する。
   - `one-obligation-per-rule` の遵守を確認する。
4. **Tier 3（主観的品質確認）**：変更後の記述が意図を保持しているか、
  人間レビューまたは LLM レビューで確認する。

### 7.2 受け入れ基準

- 変更後に `prohibitions.items` 以外のすべての rule record において
  `statement` 主述語が MUST NOT でないこと。
- YAML が標準パーサで正常に解析できること。
- rule record のスキーマ（id, layer, priority, statement, conditions, exceptions, verification）
  が全ルールで維持されていること。

---

## 8. 未解決・検討継続事項

1. **`prohibitions` セクションの位置**：現状は YAML ブロックの中ほど（interpretation, precedence, definitions, failure_states の後）に配置されている。
   lost-in-the-middle 対策を最大化するなら、`interpretation` の直後（YAML ブロックの先頭付近）への移動が望ましいが、
   これは大きな構造変更であり、別タスクとして扱うべきか要検討。

2. **他の AI directive files への展開**：本リポジトリにスキルファイルが複数存在する場合、
   同様の分析を全ファイルに適用するか、authoring スキルの meta-circular 遵守回復を優先するか、
   方針を確定する必要がある。現時点では `.agents/skills/` 配下にスキルは 1 ファイルのみ。

3. **`prohibitions.override` の適用範囲の明示化**：現状の `prohibitions.override` は
   "format_obligations, content_obligations, authoring_obligations" を明示している。
   `explanatory-must-not-permitted` が `authoring_obligations` に残る場合、
   override の適用範囲に含まれることを確認する必要がある。
