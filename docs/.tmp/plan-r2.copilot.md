# MUST NOT 集中セクション方針および authoring スキル修正計画（r2）

作成日: 2026-02-23  
改訂理由: 4 件のレビュー（Codex / Composer / GPT / Opus）に基づく修正  
対象ファイル（実体）: `.agents/skills/meta-skill.ai-directive-files-authoring/SKILL.md`  
パス補足: `.github/skills/`, `.cursor/skills/`, `.claude/skills/`, `.agent/skills/`,
`.gemini/skills/`, `.opencode/skills/`, `.windsurf/skills/` はすべて `../.agents/skills` へのシンボリックリンクであり、
実体は `.agents/skills/` の 1 ファイルのみ。修正はこの 1 ファイルに対して行えばよい。  
ステータス: 草案（具体的な変更なし）

---

## 0. r1 からの主要変更点

| 変更箇所                    | r1 の記述                                                      | r2 の修正                                                   | レビュー根拠     |
| --------------------------- | -------------------------------------------------------------- | ----------------------------------------------------------- | ---------------- |
| 結論（確立度）              | 「合理的かつ効果的な慣行として確立されている」                 | 「構造化 + 事後検証の複合アプローチとして支持される」に修正 | Codex, GPT, Opus |
| 研究的根拠                  | Semantic Gravity Wells への言及なし                            | セクション 1.3 を追加                                       | Opus             |
| "working memory" 効果       | 直接的効果として記述                                           | 合理的推論として明記                                        | Opus             |
| A-1 スキーマ                | `exceptions` / `verification` が省略（r1 の変更 A では未記載） | 完全スキーマを明示                                          | Composer, GPT    |
| A-2 statement 案            | "does not constitute an enforceable prohibition"               | "MUST be classified as explanatory" + 相互参照に修正        | Opus             |
| 「主述語」基準              | 自然言語的定義のみ                                             | 構文的判定手続きを補足                                      | Codex, GPT       |
| prohibitions.override       | 「確認が必要」（未解決事項に掲載）                             | 問題なしと確定（確認不要）し削除                            | Composer         |
| definitions.tier-separation | 説明的として許容（明示なし）                                   | 説明的として許容することを明示                              | Composer         |
| 未解決事項の整理            | Phase 2 を Section 8 末尾に埋め込み                            | Phase 2 を実施計画に明示                                    | Composer         |

---

## 1. MUST NOT 集中セクションの有効性：研究上の根拠と設計論的規範

### 1.1 LLM のコンテキスト処理と "lost-in-the-middle" 現象

大規模言語モデル（LLM）は、長いコンテキスト内の情報を均等に処理しない。
先行研究（Liu et al. 2023 など）が示す **"lost-in-the-middle"** 現象では、
プロンプトの先頭部分と末尾部分の情報が、中間部分と比較して有意に強く活性化される。

この非線形な注意分布は、AI directive files の設計に直接の含意を持つ：

- **禁止事項（MUST NOT）は失敗コストが高い**：生成途中で禁止違反が起きると取り消しが困難。
- **禁止事項が中間に埋もれると遵守率が下がる**：長い指示の中でコンテキストの中間に配置された禁止事項は、先頭・末尾に比べて忘却・無視されやすい。

### 1.2 指示階層（Instruction Hierarchy）の実証知見

OpenAI の "Instruction Hierarchy" 研究（Wallace et al. 2024）や
Anthropic の Constitutional AI に関する知見は、次を支持する：

- 制約は明示的・独立的・早期配置の場合に最も遵守されやすい。
- 制約が他のコンテンツに埋め込まれると、モデルの注意が薄れ、遵守率が低下しやすい。
- 禁止のカテゴリを一カ所に集め、早期に提示する設計は、
  生成開始前に禁止事項を活性化しやすくする効果があると**合理的に推論される**。

**重要な限界**：OpenReview 2025 の研究では、system/user プロンプト分離によっても
命令階層の安定的な確立に失敗し、モデルが制約タイプに対して優先度指定を無視する傾向が
確認されている。「ワーキングメモリ相当への保持」は直接実証された結論ではなく、
合理的推論として位置づける。

### 1.3 Semantic Gravity Wells：否定制約の逆活性化リスク（重要な反証）

Semantic Gravity Wells（arXiv 2601.08070, 2026）は、否定制約が LLM で失敗する
メカニズムを特定した研究であり、MUST NOT 集中セクション設計に直接の含意を持つ：

- **Priming Failure（違反の 87.5%）**：禁止対象を明示的に言及すること自体が、
  抑制ではなく逆に対象を活性化する。「X をしてはならない」と記述することで、
  モデルは X を強く想起する。
- **Override Failure（違反の 12.5%）**：後段の FFN 層が禁止トークンへの正の寄与
  （+0.39）を生成し、前段の抑制シグナルを約 4 倍の強度で上書きする。
- **抑制の非対称性**：成功時は 22.8 ポイントの確率低減、失敗時はわずか 5.2 ポイント
  （4.4 倍の非対称性）。

**設計への含意**：

- MUST NOT を集中セクションに「並べるだけ」では、priming effect により
  禁止対象を繰り返し活性化するリスクがある。
- **配置戦略は遵守率向上の補助的手段であって保証ではなく、
  verification メソッドによる事後検証こそが真の遵守保証手段である。**
- Strong/Strict 強度（MUST NOT レコードの膨張）は priming リスクを増大させる可能性がある。

### 1.4 規範論・仕様設計論からの観点

法令・技術仕様書（RFC、法律条文、セキュリティポリシー等）の設計慣行でも、
禁止事項は独立した条項・セクションとして前置される：

- RFC 2119 は MUST NOT を MUST と同格の normative keyword として定義し、仕様文書の構造的明確性を求める。
- セキュリティポリシーでは "deny-by-default" の原則として禁止事項を先頭に置く設計が標準。

### 1.5 結論：確立度の評価

| 観点                                       | 確立度 | 備考                                                                  |
| ------------------------------------------ | ------ | --------------------------------------------------------------------- |
| LLM 注意メカニズム（lost-in-middle）の実証 | 高     | 複数の独立研究で再現                                                  |
| 禁止事項の早期配置が遵守率を補助的に高める | 中     | 直接実証ではなく合理的推論；Semantic Gravity Wells が反証の存在を示す |
| MUST NOT 集中配置による明示化メリット      | 高     | 仕様設計論・法令設計論で確立；ただし保証ではなく補助                  |
| MUST NOT 明示言及による逆活性化リスク      | 高     | Semantic Gravity Wells (2026)：priming failure 87.5%                  |
| 構造化（専用セクション）+ 事後検証の複合   | 高     | 配置だけでなく verification による担保が必須                          |
| 「どれだけ早期に配置するか」の最適点       | 中     | 先頭付近が望ましいが定量的最適点は未確定；逆活性化の可能性も考慮      |

**総合評価**：MUST NOT を独立した専用セクションとしてファイルの序盤に集約する設計は、
LLM の処理特性・仕様設計論・実証研究から**合理的な慣行として支持される**。
ただし Semantic Gravity Wells の知見から、「集中配置すれば遵守率が上がる」は単純には成り立たず、
**「構造化された専用セクション + 事後検証（verification）」の複合的アプローチとして
合理的に確立されている**と評価すべきである。配置のみによる効果が確立されているわけではない。

---

## 2. 適用強度の選択

### 2.1 強度の段階

| 強度レベル | 内容                                                                                                                                                                                                                                             |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Weak**   | SHOULD be in a dedicated section。例外が広く認められる。                                                                                                                                                                                         |
| **Medium** | 規範的 MUST NOT（rule record の `statement` フィールドの「規範オペレータ」が MUST NOT であるもの）はすべて `prohibitions` に置く。説明的 MUST NOT（rule record 外フィールド、および `statement` で規範オペレータが MUST NOT でないもの）は許容。 |
| **Strong** | あらゆる rule record の `statement` フィールドに含まれる MUST NOT はセクションを問わず `prohibitions` に移動する。                                                                                                                               |
| **Strict** | ファイル全体を通じ MUST NOT のテキストが `prohibitions` セクション以外に現れることを禁じる。                                                                                                                                                     |

### 2.2 推奨強度と根拠

**推奨強度：Medium（MUST として適用）**

理由：

- `explanatory-must-not-permitted` / `explanatory-must-not-for-clarity` の両ルールが示すとおり、
  MUST NOT という語の出現と「規範的禁止」の出現は区別される。
- interpretation、definitions、failure_states_and_degradation などのフィールド内の MUST NOT は
  説明的（explanatory）であり、これらを `prohibitions` に引き上げると：
  - 説明文にルールレコードスキーマを適用する必要が生じ、ファイル構造が肥大化する。
  - 「何が normative か」の境界が曖昧になり、かえって遵守確認が困難になる。
- Semantic Gravity Wells の知見から、Strong/Strict は MUST NOT レコードを膨張させ、
  priming リスクを増大させる可能性がある。
- lost-in-the-middle の軽減効果は Medium で大部分を達成できるため、
  Strong/Strict の追加効果は小さい。

### 2.3 Medium 強度の操作的定義：規範オペレータ判定手続き

**用語定義**：

- **規範オペレータ（deontic operator）**：`statement` フィールドを左から走査して、
  「数える」と判定した最初の RFC モーダル（MUST NOT / MUST / SHOULD NOT / SHOULD / MAY）。

**「数えない（説明的）」の条件**（以下のいずれかを満たす場合）：

1. 単引用符または二重引用符で囲まれたトークンとして出現している（例：`'MUST NOT'`）。
2. "the phrase MUST NOT"、"phrase MUST NOT" 等、語句としての言及であることが明示されている出現。
3. RFC keywords の列挙として現れている出現（例：`(MUST, MUST NOT, SHOULD, ...)`）。
4. 括弧内での説明として現れている出現（例：`All normative prohibitions (MUST NOT) MUST ...`）。
5. 「e.g.」「for example」に続く例示の一部として現れている出現。

**「数える（規範）」の条件**：上記「数えない」に該当しない出現。

**Medium 強度のルール**：

> `statement` の規範オペレータが **MUST NOT** である rule record は、
> `prohibitions.items` に配置しなければならない（MUST）。  
> 規範オペレータが MUST NOT 以外である rule record、および rule record 外のフィールド
> （description, behavior, degradation, verification 等）に登場する MUST NOT は、
> 説明的使用として扱い、`prohibitions` への移動を要しない。

---

## 3. 現状の authoring スキルにおける meta-circular 非遵守箇所の特定

### 3.1 調査方法

SKILL.md 全体を通じ `statement` フィールドに MUST NOT が含まれるルールを列挙し、
規範オペレータ判定手続き（セクション 2.3）を適用した。

### 3.2 確定違反

#### 違反 1：`explanatory-must-not-permitted` の配置

| 項目           | 値                                                                                                                                                                                                                                   |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| ルール ID      | `explanatory-must-not-permitted`                                                                                                                                                                                                     |
| 所属セクション | `authoring_obligations`                                                                                                                                                                                                              |
| statement      | `"When describing interpretation, semantics, or verification (as opposed to primary normative statement fields), descriptive use of the phrase MUST NOT is allowed and MUST NOT be treated as additional enforceable prohibitions."` |
| 規範オペレータ | MUST NOT（"MUST NOT be treated" が走査の最初の「数える」モーダル）                                                                                                                                                                   |
| 違反内容       | 規範オペレータが MUST NOT だが `prohibitions` セクションに配置されていない                                                                                                                                                           |
| 参照ルール     | `prohibitions-dedicated-section`                                                                                                                                                                                                     |

#### 副次的問題：`explanatory-must-not-permitted` の複合述語

| 項目       | 値                                                                                                                                                                 |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| ルール ID  | `explanatory-must-not-permitted`                                                                                                                                   |
| 問題内容   | "is allowed"（許可）と "MUST NOT be treated"（禁止）の 2 述語が同居している                                                                                        |
| 参照ルール | `one-obligation-per-rule`                                                                                                                                          |
| 解釈の余地 | "is allowed" を MAY 相当と読めば形式的には 1 MUST NOT 述語のみとも解釈できるが、"is allowed" の曖昧性自体が `no-ambiguous-modals` の精神に反するため分割が望ましい |

### 3.3 非違反の確認（`statement` に MUST NOT を含むが規範オペレータでないケース）

| ルール ID                          | セクション              | MUST NOT の出現形態                                                     | 規範オペレータ | 判定       |
| ---------------------------------- | ----------------------- | ----------------------------------------------------------------------- | -------------- | ---------- |
| `explanatory-must-not-for-clarity` | `authoring_obligations` | "e.g. listing RFC keywords" として例示。主オペレータは SHOULD。         | SHOULD         | **非違反** |
| `use-normative-keywords`           | `authoring_obligations` | RFC keywords 列挙 `(MUST, MUST NOT, ...)` の一部。主オペレータは MUST。 | MUST           | **非違反** |
| `prohibitions-dedicated-section`   | `authoring_obligations` | 括弧内説明 `(MUST NOT)` として登場。主オペレータは MUST。               | MUST           | **非違反** |
| `define-conflict-policy`           | `authoring_obligations` | 例示内（`e.g. MUST vs MUST: halt`）として登場。主オペレータは MUST。    | MUST           | **非違反** |

### 3.4 rule record 外の MUST NOT（説明的使用として許容）

以下は rule record の `statement` フィールド以外に登場する MUST NOT であり、
`explanatory-must-not-permitted` が定義する許容範囲に該当する：

| 箇所                                                        | フィールド種別               |
| ----------------------------------------------------------- | ---------------------------- |
| `interpretation.unknown_keys`                               | interpretation prose         |
| `interpretation.unspecified_behavior`                       | interpretation prose         |
| `precedence_and_conflict.conflict_policy.MUST_vs_MUST`      | conflict policy prose        |
| `failure_states_and_degradation.failure_states[0].behavior` | behavior prose               |
| `failure_states_and_degradation.degradation`                | degradation prose            |
| `definitions.tier-separation.description`                   | definition prose（注を参照） |
| `one-obligation-per-rule` の verification                   | verification field           |

**注：`definitions.tier-separation.description` について**

この記述中の "MUST NOT interleave" は、tier-separation が適用される文脈では
実質的に規範的禁止として機能する。`explanatory-must-not-permitted` が許容範囲として明示する
"interpretation, semantics, or verification" に definitions フィールドが含まれるかは
SKILL.md 内で明記されていない。

現状は definitions フィールドを許容範囲に含める（説明的使用として扱う）ものとして進める。
将来的に `no-interleave-tiers` として prohibitions に独立ルールを追加し definitions から
参照する形への整理は別タスク候補として残す。

---

## 4. 目標設定

### 4.1 目指すべき状態

**Meta-circular 完全遵守状態の定義**：

> authoring スキルが定義するすべてのルールを、authoring スキル自身が遵守している状態。
> 具体的には：`prohibitions-dedicated-section`・`one-obligation-per-rule`・
> `no-ambiguous-modals` が要求する条件を、authoring スキル自身が満たしている状態。

### 4.2 遵守の確認基準

1. `prohibitions.items` 以外のすべての rule record において、
   `statement` の規範オペレータが MUST NOT でないこと。
2. `explanatory-must-not-permitted` が定義する「説明的 MUST NOT」の許容範囲が
   ファイル内に整合的に適用されていること。
3. `one-obligation-per-rule` が要求する「1 ルール 1 述語」が、
   すべての rule record において満たされていること。
4. YAML が標準パーサで正常に解析できること。
5. 全 rule record がルールレコードスキーマ
   （id, layer, priority, statement, conditions, exceptions, verification）に適合していること。

---

## 5. 修正方針

### 5.1 基本方針

**最小変更・最大整合**原則：既存の構造・ルール数・意図を変えず、
`explanatory-must-not-permitted` の記述をリファクタリングすることで meta-circular 遵守を回復する。

### 5.2 具体的な変更方針

#### 変更 A：`explanatory-must-not-permitted` を分割する

現状の 1 ルール（2 述語）を、以下の 2 ルールに分割する：

**分割後ルール A-1（`prohibitions.items` の末尾に追加）**

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

**分割後ルール A-2（`authoring_obligations` に残留・statement 書き換え）**

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

**A-2 の statement 設計について**：

r1 で提案した "does not constitute an enforceable prohibition" という否定的断言は、
`use-normative-keywords` が要求する RFC-style normative keywords の使用に照らして
曖昧になる可能性がある（"does not constitute" はいずれの RFC モーダルにも該当しない）。
r2 では "MUST be classified as explanatory" という肯定的義務 + `no-treat-explanatory-must-not-as-prohibition` への相互参照とすることで、この問題を回避する。

#### 変更 B：`explanatory-must-not-for-clarity` の確認（変更なし）

`statement` の規範オペレータが SHOULD であり、MUST NOT は例示として登場しているため変更不要。
変更 A 実施後に両ルールの整合性を確認すること。

#### 変更 C：順序調整（変更 A に含む）

A-1 を `prohibitions.items` の末尾に追加することで完了。

### 5.3 `prohibitions.override` の適用範囲（確認済み・変更不要）

`prohibitions.override` は format_obligations / content_obligations / authoring_obligations を
明示的に上書きする。`explanatory-must-not-permitted` が `authoring_obligations` に残留する場合も、
新規 prohibition A-1 が authoring_obligations の A-2 を上書きしうるが、両者は補完関係にあり
矛盾しない。**この点は確認不要**（r1 の未解決事項から削除）。

### 5.4 変更量の評価

| 変更                    | 対象                                                   | 影響範囲                                    |
| ----------------------- | ------------------------------------------------------ | ------------------------------------------- |
| A-1: 新ルール追加       | `prohibitions.items` の末尾                            | 1 ルールレコードの追加                      |
| A-2: 既存ルール書き換え | `authoring_obligations.explanatory-must-not-permitted` | statement + verification フィールドのみ変更 |
| B: 確認のみ             | なし                                                   | 変更なし                                    |

---

## 6. 適用強度についての最終方針

**Medium 強度を MUST（強制）として適用する。**

具体的な適用ルール（セクション 2.3 の規範オペレータ判定手続きを参照）：

- `statement` の規範オペレータが **MUST NOT** である rule record：
  `prohibitions.items` に置かなければならない（MUST）。
- `statement` の規範オペレータが MUST NOT 以外の rule record：
  `prohibitions` への移動を要しない（MUST NOT が他の方法で出現しても許容）。
- rule record 外のフィールドでの MUST NOT：
  許容される（`explanatory-must-not-permitted` の適用範囲）。

**Strict 強度を採用しない理由**：

- 説明的 MUST NOT をすべて `prohibitions` に移動するには rule record への昇格が必要となり、構造が大幅に肥大化する。
- Semantic Gravity Wells の知見から、MUST NOT レコードの膨張は priming リスクを増大させる。
- Medium 強度で大部分の遵守効果を達成できる。

---

## 7. 実施計画

### 7.1 Phase 1：meta-circular 遵守の回復（本タスク）

| Tier                         | 内容                                                                                                                                           |
| ---------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| **Tier 0（構造確認）**       | SKILL.md の全 rule record を列挙し、セクション 3.2〜3.4 の違反確定リストを最新化する。                                                         |
| **Tier 1（変更実施）**       | 変更 A（A-1 追加 + A-2 書き換え）を実施する。                                                                                                  |
| **Tier 2（客観的検証）**     | YAML パース検証・構造検証・`prohibitions-dedicated-section` 遵守確認・`one-obligation-per-rule` 遵守確認・rule-record スキーマ確認を実施する。 |
| **Tier 3（主観的品質確認）** | 変更後の記述が意図を保持しているか人間レビューで確認する。                                                                                     |

### 7.2 Phase 2：`prohibitions` セクションの序盤移動（別タスク）

lost-in-the-middle 対策の補助的強化として、YAML ブロック内で `prohibitions` セクションを
`interpretation` および `precedence_and_conflict` の直後に移動する。

- 大きな構造変更であり Phase 1 完了後に別タスクとして扱う。
- Semantic Gravity Wells の知見から、移動による効果は補助的なものと評価する。
  事後検証（verification メソッド）の強化と組み合わせることが重要。

### 7.3 受け入れ基準（Phase 1）

- `prohibitions.items` 以外のすべての rule record において `statement` の規範オペレータが MUST NOT でない。
- YAML が標準パーサで正常に解析できる。
- rule record スキーマ（id, layer, priority, statement, conditions, exceptions, verification）が全ルールで維持されている。
- `explanatory-must-not-permitted` と `no-treat-explanatory-must-not-as-prohibition` の間で意味的な矛盾がない。

---

## 8. 未解決・検討継続事項

1. **`definitions.tier-separation` の規範的禁止化**：
   現状は説明的使用として許容するが、将来的に `no-interleave-tiers` を prohibitions に追加し、
   definitions から参照する形への整理を別タスク候補として残す。

2. **他の AI directive files への展開**：
   本リポジトリでは `.agents/skills/` 配下にスキルは現在 1 ファイルのみ。
   ファイルが増えた場合は同じ Medium 強度（規範オペレータ判定手続き込み）を適用するか、
   authoring スキルへの参照（id/link）に統一するかを決める。

3. **Semantic Gravity Wells の緩和策の具体化**：
   AI directive files の記述スタイルとして priming リスクを低減する具体的ガイドライン
   （例：「禁止対象を直接名指しする代わりに望ましい状態を肯定的に記述する」）の追加は
   別タスクとして検討する価値がある。

4. **規範オペレータ判定の lint 化**：
   セクション 2.3 の判定手続きを機械実行可能な linter として実装することで、
   `verification-machine-checkable` の充足度が向上する。別タスク候補として残す。
