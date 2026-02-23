# MUST NOT 集中セクション方針および authoring スキル修正計画

作成日: 2026-02-23  
対象ファイル（実体）: `.agents/skills/meta-skill.ai-directive-files-authoring/SKILL.md`

> **パス補足**: `.github/skills/`, `.cursor/skills/`, `.claude/skills/`, `.agent/skills/`,
> `.gemini/skills/`, `.opencode/skills/`, `.windsurf/skills/` はすべて `../.agents/skills` へのシンボリックリンクであり、
> 実体は `.agents/skills/` の 1 ファイルのみ。修正は実体ファイルに対してのみ行う。

ステータス: 変更方針プラン（AI directive files への具体的変更は含まない）

---

## 0. 本文書の目的・スコープ

本文書は以下の二つの問いに答え、修正計画を定義する。

1. **確立性の問い**：AI directive files において MUST NOT のみを集めた独立セクションをファイルの序盤に配置することは、遵守率向上のための有効な慣行として確立されているか。確立されているとして、どの強度で適用するのが最も効果につながるか。
2. **修正の問い**：authoring スキルは現状 MUST NOT 集中セクション外に MUST NOT 記述があり meta-circular を満たしていない。目指すべき状態・方針・手順は何か。

AI directive files への具体的な変更はスコープ外とする。

---

## 1. MUST NOT 集中セクションの有効性：研究上の根拠と設計論的規範

### 1.1 LLM のコンテキスト処理と "lost-in-the-middle" 現象

大規模言語モデル（LLM）は、長いコンテキスト内の情報を均等に処理しない。
Liu et al. 2023（"Lost in the Middle: How Language Models Use Long Contexts"）が示す
**"lost-in-the-middle"** 現象では、プロンプトの先頭部分と末尾部分の情報が、
中間部分と比較して有意に強く活性化される。

AI directive files の設計への含意：

- **禁止事項（MUST NOT）は失敗コストが高い**：生成途中での禁止違反は取り消しが困難。
- **禁止事項が中間に埋もれると遵守率が下がる**：長いコンテキストの中間に配置された禁止事項は、先頭・末尾に比べて忘却・無視されやすい。
- **早期配置・独立セクション化の補助的効果**：禁止事項を先頭付近の独立セクションに集めることで、モデルが生成開始前に禁止事項をより強く活性化する状態を作りやすい。

### 1.2 指示階層（Instruction Hierarchy）の実証知見と限界

Wallace et al. 2024（"The Instruction Hierarchy: Training LLMs to Prioritize Privileged Instructions"）等の研究は、制約が明示的・独立的・早期配置の場合に遵守されやすい傾向を支持する。

**重要な限界**：OpenReview 2025 に掲載された研究では、system/user プロンプト分離でも命令階層の安定的な確立に失敗し、モデルが優先度指定を無視する傾向が確認されている。「早期配置により禁止事項がワーキングメモリ相当の領域に保持される」は直接実証された結論ではなく、lost-in-the-middle 現象から合理的に導出される推論として位置づける。

### 1.3 Semantic Gravity Wells：否定制約の逆活性化リスク（重要な反証）

Semantic Gravity Wells（arXiv:2601.08070, 2026）は、否定制約が LLM で失敗するメカニズムを
特定した研究であり、MUST NOT 集中セクション設計に直接の含意を持つ：

- **Priming Failure（違反の 87.5%）**：禁止対象を明示的に言及すること自体が、抑制ではなく逆に対象を活性化する。「X をしてはならない」と記述することで、モデルは X を強く想起する。
- **Override Failure（違反の 12.5%）**：後段の FFN 層が禁止トークンへの正の寄与（+0.39）を生成し、前段の抑制シグナルを約 4 倍の強度で上書きする。
- **抑制の非対称性**：成功時は 22.8 ポイントの確率低減、失敗時はわずか 5.2 ポイント（4.4 倍の非対称性）。

**設計への含意**：

- MUST NOT を集中セクションに「並べるだけ」では、priming effect により禁止対象を繰り返し活性化するリスクがある。
- **配置戦略は遵守率向上の補助的手段であって保証ではなく、verification メソッドによる事後検証こそが真の遵守保証手段である。**
- Strong/Strict 強度（MUST NOT レコードの膨張）は priming リスクを増大させる可能性がある。

### 1.4 規範論・仕様設計論からの観点

法令・技術仕様書（RFC、法律条文、セキュリティポリシー等）の設計慣行でも、禁止事項は独立した条項・セクションとして前置される：

- RFC 2119（Bradner, 1997）は MUST NOT を MUST と同格の normative keyword として定義し、仕様文書の構造的明確性を求める。禁止事項の明示化・分離は仕様設計論において確立された慣行である。
- セキュリティポリシーでは "deny-by-default" の原則として禁止事項を先頭に置く設計が標準となっている。

### 1.5 確立度の評価

| 観点 | 確立度 | 根拠・備考 |
|------|--------|-----------|
| LLM 注意メカニズム（lost-in-middle）の実証 | 高 | Liu et al. 2023；複数の独立研究で再現 |
| 禁止事項の早期配置が遵守率を補助的に高める | 中 | 直接実証ではなく合理的推論；lost-in-middle から導出 |
| MUST NOT 集中配置による明示化メリット | 高 | RFC 2119 等の仕様設計論・法令設計論で確立；ただし保証ではなく補助 |
| MUST NOT 明示言及による逆活性化リスク | 高 | Semantic Gravity Wells (arXiv:2601.08070, 2026)：priming failure 87.5% |
| 構造化（専用セクション）+ 事後検証の複合 | 高 | 配置だけでなく verification による担保が必須という結論は複数研究から支持 |
| 「どれだけ早期に配置するか」の定量的最適点 | 中 | 先頭付近が望ましいが定量的最適点は未確定；priming リスクも考慮 |

**総合評価**：MUST NOT を独立した専用セクションとしてファイルの序盤に集約する設計は、LLM の処理特性・仕様設計論・実証研究から**合理的な慣行として支持される**。ただし Semantic Gravity Wells の知見から、「集中配置すれば遵守率が上がる」は単純には成り立たず、**「構造化された専用セクション + 事後検証（verification）」の複合的アプローチとして合理的に確立されている**と評価すべきである。配置のみによる効果は確立されていない。

---

## 2. 適用強度の選択

### 2.1 強度の段階

| 強度レベル | 定義 |
|-----------|------|
| **Weak** | SHOULD be in a dedicated section。例外が広く認められる。 |
| **Medium** | rule record の `statement` フィールドの「規範オペレータ」（後述）が MUST NOT であるすべての rule record を `prohibitions.items` に配置する。rule record 外フィールドの MUST NOT および `statement` で規範オペレータが MUST NOT でないものは説明的使用として許容する。 |
| **Strong** | あらゆる rule record の `statement` フィールドに含まれる MUST NOT はセクションを問わず `prohibitions` に移動する。 |
| **Strict** | ファイル全体を通じ MUST NOT のテキストが `prohibitions` セクション以外に現れることを禁じる。 |

### 2.2 推奨強度：Medium（MUST として適用）

**Medium 強度を MUST（強制）として適用する。**

採用理由：

- MUST NOT という語の出現と「規範的禁止」の出現は区別されなければならない。interpretation・definitions・failure_states_and_degradation 等のフィールド内の MUST NOT は説明的（explanatory）であり、これらを `prohibitions` に引き上げると説明文にルールレコードスキーマを適用する必要が生じ、ファイル構造が肥大化する。
- Semantic Gravity Wells の知見から、Strong/Strict は MUST NOT レコードを膨張させ、priming リスクを増大させる可能性がある。
- Medium 強度で大部分の遵守補助効果を達成でき、Strong/Strict の追加効果は小さい。
- 「何が normative か」の境界を明確に保つことで、機械検証可能性が高まる。

### 2.3 Medium 強度の操作的定義：規範オペレータ判定手続き

**用語定義**

- **規範オペレータ（deontic operator）**：`statement` フィールドを左から走査して、「数える」と判定した最初の RFC モーダル（MUST NOT / MUST / SHOULD NOT / SHOULD / MAY）。

**「数えない（説明的）」の条件**（以下のいずれかを満たす出現）：

1. 単引用符または二重引用符で囲まれたトークンとして出現している（例：`'MUST NOT'`）。
2. "the phrase MUST NOT"、"phrase MUST NOT" 等、語句としての言及であることが明示されている出現。
3. RFC keywords の列挙として現れている出現（例：`(MUST, MUST NOT, SHOULD, ...)`）。
4. 括弧内での説明として現れている出現（例：`All normative prohibitions (MUST NOT) MUST ...`）。
5. "e.g."、"for example"、"such as" に続く例示の一部として現れている出現。

**「数える（規範）」の条件**：上記「数えない」に該当しない出現。

**Medium 強度のルール（適用対象）**：

> - `statement` の規範オペレータが **MUST NOT** である rule record は、`prohibitions.items` に配置しなければならない（MUST）。
> - 規範オペレータが MUST NOT 以外の rule record は、`statement` 内に MUST NOT が出現しても、`prohibitions` への移動を要しない。
> - rule record 外のフィールド（description, behavior, degradation, verification 等）に登場する MUST NOT は、説明的使用として扱い `prohibitions` への移動を要しない。

**判定の将来的な lint 化**：本手続きは人手判定を主体とするが、将来的に機械実行可能な linter として実装することで `verification-machine-checkable` の充足度が向上する。これは別タスク候補として残す。

---

## 3. 現状の authoring スキルにおける meta-circular 非遵守箇所

### 3.1 調査方法

対象ファイル（`.agents/skills/meta-skill.ai-directive-files-authoring/SKILL.md`）全体を通じ、`statement` フィールドに MUST NOT が含まれるすべての rule record を列挙し、セクション 2.3 の規範オペレータ判定手続きを適用した。

### 3.2 確定違反

#### 違反 1：`explanatory-must-not-permitted` の配置誤り

| 項目 | 値 |
|------|-----|
| ルール ID | `explanatory-must-not-permitted` |
| 現在の所属セクション | `authoring_obligations` |
| statement（現状） | `"When describing interpretation, semantics, or verification (as opposed to primary normative statement fields), descriptive use of the phrase MUST NOT is allowed and MUST NOT be treated as additional enforceable prohibitions."` |
| 規範オペレータ判定 | "MUST NOT be treated" が走査の最初の「数える」モーダル → 規範オペレータは **MUST NOT** |
| 違反内容 | 規範オペレータが MUST NOT であるにもかかわらず `prohibitions.items` に配置されていない |
| 参照ルール | `prohibitions-dedicated-section`：「All normative prohibitions (MUST NOT) MUST be in a dedicated section.」 |

#### 副次的問題：複合述語

| 項目 | 値 |
|------|-----|
| ルール ID | `explanatory-must-not-permitted` |
| 問題内容 | statement が "is allowed"（許可）と "MUST NOT be treated"（禁止）の 2 述語を含む |
| 参照ルール | `one-obligation-per-rule`：「Every enforceable rule MUST be one obligation per rule.」 |
| 解釈の余地 | "is allowed" を MAY 相当と読めば形式的には MUST NOT 述語は 1 つのみとも解釈できるが、"is allowed" の曖昧性自体が `no-ambiguous-modals` の精神に反するため、分割が望ましい |

### 3.3 非違反の確認（`statement` に MUST NOT を含むが規範オペレータでないケース）

| ルール ID | セクション | MUST NOT の出現形態 | 規範オペレータ | 判定 |
|-----------|-----------|---------------------|---------------|------|
| `explanatory-must-not-for-clarity` | `authoring_obligations` | "e.g. listing RFC keywords" として例示。 | SHOULD | **非違反** |
| `use-normative-keywords` | `authoring_obligations` | RFC keywords の列挙 `(MUST, MUST NOT, ...)` の一部。 | MUST | **非違反** |
| `prohibitions-dedicated-section` | `authoring_obligations` | 括弧内説明 `(MUST NOT)` として登場。 | MUST | **非違反** |
| `define-conflict-policy` | `authoring_obligations` | 例示内 `e.g. MUST vs MUST: halt` として登場。 | MUST | **非違反** |
| `one-obligation-per-rule` | `authoring_obligations` | verification フィールド内での言及。statement の外。 | MUST（statement） | **非違反**（rule record 外） |

### 3.4 rule record 外の MUST NOT（説明的使用として許容）

以下は rule record の `statement` フィールド以外に登場する MUST NOT であり、説明的使用として許容される：

| 箇所 | フィールド種別 |
|------|---------------|
| `interpretation.unknown_keys` | interpretation prose |
| `interpretation.unspecified_behavior` | interpretation prose |
| `precedence_and_conflict.conflict_policy.MUST_vs_MUST` | conflict policy prose |
| `failure_states_and_degradation.failure_states[0].behavior` | behavior prose |
| `failure_states_and_degradation.degradation` | degradation prose |
| `definitions.tier-separation.description` | definition prose（注を参照） |
| `one-obligation-per-rule` の verification | verification field |

**注：`definitions.tier-separation.description` について**

この記述中の "MUST NOT interleave" は、tier-separation が適用される文脈では実質的に規範的禁止として機能する。現状の `explanatory-must-not-permitted` が許容範囲として明示する "interpretation, semantics, or verification" に definitions フィールドが含まれるかは SKILL.md 内で明記されていない。

本プランでは definitions フィールドを説明的使用として許容するものとして進める。将来的に `no-interleave-tiers` として prohibitions に独立ルールを追加し definitions から参照する形への整理は別タスク候補として残す。

---

## 4. 目標設定

### 4.1 meta-circular 完全遵守状態の定義

> authoring スキルが定義するすべてのルールを、authoring スキル自身が遵守している状態。
> 具体的には：`prohibitions-dedicated-section`・`one-obligation-per-rule`・`no-ambiguous-modals` が要求する条件を、authoring スキル自身が満たしている状態。

### 4.2 遵守の確認基準（受け入れ基準）

1. `prohibitions.items` 以外のすべての rule record において、`statement` の規範オペレータが MUST NOT でないこと。
2. 説明的 MUST NOT の許容範囲（rule record 外フィールド、および `statement` で規範オペレータが MUST NOT でないもの）がファイル内に整合的に適用されていること。
3. `one-obligation-per-rule` が要求する「1 ルール 1 述語」が、すべての rule record において満たされていること。
4. YAML が標準パーサで正常に解析できること。
5. 全 rule record がルールレコードスキーマ（id, layer, priority, statement, conditions, exceptions, verification）に適合していること。

---

## 5. 修正方針

### 5.1 基本方針

**最小変更・最大整合**原則：既存の構造・ルール数・意図を変えず、`explanatory-must-not-permitted` の記述をリファクタリングすることで meta-circular 遵守を回復する。

### 5.2 具体的な変更設計

#### 変更 A：`explanatory-must-not-permitted` を 2 ルールに分割する

現状の 1 ルール（複合述語）を、以下の 2 ルールに分割する。

---

**ルール A-1（新規・`prohibitions.items` の末尾に追加）**

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

設計意図：

- 規範オペレータが MUST NOT であるため `prohibitions.items` に配置する。
- `prohibitions.override` による上書き対象範囲（format_obligations / content_obligations / authoring_obligations）と矛盾しない（A-2 との関係は補完的）。

---

**ルール A-2（既存ルール `explanatory-must-not-permitted` の statement・verification 書き換え）**

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

設計意図：

- statement の規範オペレータを MUST NOT から MUST（"MUST be classified as"）に変更し、`authoring_obligations` に残留させる。
- "does not constitute an enforceable prohibition"（否定的断言・RFC モーダルなし）は採用しない。`use-normative-keywords` が要求する RFC-style normative keywords の使用と整合するため、肯定的義務 + 相互参照の形式を採用する。
- "is allowed" という曖昧な許可表現を削除し、`no-ambiguous-modals` への準拠を回復する。

---

#### 変更 B：`explanatory-must-not-for-clarity` の確認（変更なし）

`statement` の規範オペレータが SHOULD であり、MUST NOT は例示として登場しているため変更不要。変更 A 実施後に両ルールの整合性を確認すること。

### 5.3 `prohibitions.override` の適用範囲（確認済み）

`prohibitions.override` は format_obligations / content_obligations / authoring_obligations を明示的に上書きする。A-1（prohibition）と A-2（authoring_obligation）は補完関係にあり矛盾しない。変更後の構造に問題はない。

### 5.4 変更量の評価

| 変更 | 対象 | 影響範囲 |
|------|------|---------|
| A-1: 新ルール追加 | `prohibitions.items` の末尾 | 1 ルールレコードの追加 |
| A-2: 既存ルール書き換え | `authoring_obligations.explanatory-must-not-permitted` | statement + verification フィールドのみ変更 |
| B: 確認のみ | なし | 変更なし |

---

## 6. 実施計画

### 6.1 Phase 1：meta-circular 遵守の回復（優先タスク）

| Tier | 内容 | 完了条件 |
|------|------|---------|
| **Tier 0（構造確認）** | SKILL.md の全 rule record を列挙し、セクション 3.2〜3.4 の違反確定リストを現在のファイル状態に照らして最新化する。 | 違反ルールの確定リストが得られる |
| **Tier 1（変更実施）** | 変更 A（A-1 新規追加 + A-2 statement/verification 書き換え）を実施する。 | ファイルへの変更が完了する |
| **Tier 2（客観的検証）** | YAML パース検証（yaml-parse-validation）・構造検証（structure-validation）・`prohibitions-dedicated-section` 遵守確認・`one-obligation-per-rule` 遵守確認・rule-record スキーマ確認を実施する。 | すべての検証が成功する |
| **Tier 3（主観的品質確認）** | 変更後の記述が意図・整合性を保持しているか人間レビューで確認する。 | レビューで意味的矛盾がないことが確認される |

### 6.2 Phase 2：`prohibitions` セクションの序盤移動（別タスク候補）

lost-in-the-middle 対策の補助的強化として、YAML ブロック内で `prohibitions` セクションを `interpretation` および `precedence_and_conflict` の直後に移動する。

- 大きな構造変更であり Phase 1 完了後に独立したタスクとして扱う。
- Semantic Gravity Wells（arXiv:2601.08070, 2026）の知見から、移動による遵守改善効果は限定的であり、事後検証（verification メソッド）の強化と組み合わせることが重要。
- 移動を実施する場合、YAML パース検証・構造検証を必ず実施する。

### 6.3 Phase 1 受け入れ基準（チェックリスト）

- [ ] `prohibitions.items` 以外のすべての rule record において `statement` の規範オペレータが MUST NOT でない。
- [ ] YAML が標準パーサで正常に解析できる。
- [ ] rule record スキーマ（id, layer, priority, statement, conditions, exceptions, verification）が全ルールで維持されている。
- [ ] `explanatory-must-not-permitted`（A-2）と `no-treat-explanatory-must-not-as-prohibition`（A-1）の間で意味的な矛盾がない。
- [ ] `explanatory-must-not-for-clarity` との整合性が確認されている。

---

## 7. 未解決・検討継続事項

1. **`definitions.tier-separation` の規範的禁止化**：この記述中の "MUST NOT interleave" は将来的に `no-interleave-tiers` として prohibitions に独立ルール化し、definitions から参照する形への整理を別タスク候補として残す。

2. **他の AI directive files への展開**：本リポジトリでは `.agents/skills/` 配下にスキルは現在 1 ファイルのみ。ファイルが増えた場合は同じ Medium 強度（規範オペレータ判定手続き込み）を適用するか、authoring スキルへの参照（id/link）に統一するかを決める。

3. **Semantic Gravity Wells の緩和策の具体化**：AI directive files の記述スタイルとして priming リスクを低減する具体的ガイドライン（例：禁止対象を直接名指しする代わりに望ましい状態を肯定的に記述するスタイルガイド）の追加は別タスクとして検討する価値がある。

4. **規範オペレータ判定の lint 化**：セクション 2.3 の判定手続きを機械実行可能な linter として実装することで `verification-machine-checkable` の充足度が向上する。別タスク候補として残す。

5. **`prohibitions` セクションの位置（Phase 2）**：Phase 1 完了後に `interpretation` 直後への移動を検討する。Semantic Gravity Wells の知見から移動効果は限定的と評価するが、仕様設計論的な明示性の観点で有意義。
