# MUST NOT 集中セクション方針および authoring スキル改善計画（r3 統合版）

作成日: 2026-02-23
基盤文書: `must-not-section-policy-and-remediation-plan-r2.md`, `plan.codex.md`, `plan.composer.md`, `plan.gpt.md`, `plan.opus.md`
対象ファイル（実体）: `.agents/skills/meta-skill.ai-directive-files-authoring/SKILL.md`
パス補足: `.cursor/skills/`, `.github/skills/`, `.claude/skills/`, `.agent/skills/`,
`.gemini/skills/`, `.opencode/skills/`, `.windsurf/skills/` はすべて `../.agents/skills` へのシンボリックリンクであり、
実体は `.agents/skills/` の 1 ファイルのみ。修正はこの 1 ファイルに対して行えばよい。
ステータス: 統合プラン（具体的なファイル変更なし）

---

## 0. 本文書の目的と前提

### 0.1 目的

本文書は、以下の命題に対する統合的な回答である：

1. AI directive files において、MUST NOT のみを集めた独立セクションをファイル序盤に配置することは、
   研究成果やメカニズム上の常識・規範として確立されているのか。
2. 確立されているとして、どこまでの強さで適用するのが最も効果につながるのか。
3. authoring スキルが meta-circular を満たしていない現状を、どのような方針で改善すべきか。

### 0.2 統合の方法

r2 本体計画および 4 件のエージェントレビュー（Codex / Composer / GPT / Opus）を
包括的に検証し、合意点の抽出・対立点の解決・欠落の補完を行った。

各エージェントプランの主要な貢献を以下に要約する：

| エージェント | 主要貢献                                                                                                                                                                                                                                  |
| ------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| GPT          | 「確立されている」の断言強度への警告、Medium 強度の「主述語」判定を機械検証可能にする必要性の指摘、判定手続き（決定規則）の明文化提案                                                                                                     |
| Codex        | 根拠表現を「強い実務ベストプラクティス」に抑える方針、`.agents` と他パスの同期問題の提起、`statement_modal` 等の明示フィールド導入構想、検証メソッド追加提案（`must-not-locality-validation`, `one-modal-per-rule-validation`）           |
| Opus         | Semantic Gravity Wells（arXiv 2601.08070, 2026）の反証としての統合、先行実装（ブランチ前回コミット）との整合性分析、A-2 statement を "MUST be classified as explanatory" とする肯定的義務形式の提案                                       |
| Composer     | ルール A-1 スキーマ不足（`exceptions` / `verification` 欠落）の指摘、Phase 2（prohibitions 序盤移動）の実施計画への明示的組込み、`definitions.tier-separation` の規範的禁止化の将来オプション提示、`prohibitions.override` の確認不要判定 |

### 0.3 非目的

- LLM の注意特性に関する個別論文の正確な引用検証を、本プランの受け入れ条件にしない。
- 全 AI directive files への横展開は、本プランでは必須としない（別タスク候補）。
- AI directive files の具体的なファイル変更は本プランの範囲外である。

### 0.4 用語定義

本文書における用語を以下に定義する：

- **AI directive files**: `.agents/skills/` 配下の Markdown ファイル（YAML frontmatter + 単一 fenced YAML ブロック構成）。
- **authoring スキル**: `.agents/skills/meta-skill.ai-directive-files-authoring/SKILL.md`。AI directive files の書式・構造・ルールを定義するメタスキル。
- **rule record**: `id`, `layer`, `priority`, `statement`, `conditions`, `exceptions`, `verification` を持つ構造化レコード。
- **meta-circular**: authoring スキルが定義するすべてのルールを、authoring スキル自身が遵守している状態。
- **規範オペレータ（deontic operator）**: 後述の判定手続きにより `statement` フィールドから特定される、ルールの主たる義務・禁止を表す RFC モーダル。

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

**重要な限界**（GPT, Opus 合意）：

- OpenReview 2025 の研究では、system/user プロンプト分離によっても
  命令階層の安定的な確立に失敗し、モデルが制約タイプに対して優先度指定を無視する傾向が確認されている。
- 「ワーキングメモリ相当への保持」は直接実証された結論ではなく、合理的推論として位置づける。
- 強制力は「研究の断言」ではなく、runner/linter で機械的に検証できる設計に依存する（GPT）。

### 1.3 Semantic Gravity Wells：否定制約の逆活性化リスク（重要な反証）

Semantic Gravity Wells（arXiv 2601.08070, 2026）は、否定制約が LLM で失敗する
メカニズムを特定した研究であり、MUST NOT 集中セクション設計に直接の含意を持つ
（Opus が指摘、r2 で統合済み）：

- **Priming Failure（違反の 87.5%）**：禁止対象を明示的に言及すること自体が、
  抑制ではなく逆に対象を活性化する。「X をしてはならない」と記述することで、
  モデルは X を強く想起する。
- **Override Failure（違反の 12.5%）**：後段の FFN 層が禁止トークンへの正の寄与
  （+0.39）を生成し、前段の抑制シグナルを約 4 倍の強度で上書きする。
- **抑制の非対称性**：成功時は 22.8 ポイントの確率低減、失敗時はわずか 5.2 ポイント
  （4.4 倍の非対称性）。

**設計への含意（全エージェント合意）**：

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

**総合評価（全エージェント合意に基づく統合結論）**：

MUST NOT を独立した専用セクションとしてファイルの序盤に集約する設計は、
LLM の処理特性・仕様設計論・実証研究から**合理的な設計慣行として支持される**。

ただし以下の限定が不可欠である：

1. 「集中配置すれば遵守率が上がる」は単純には成り立たない（Semantic Gravity Wells の反証）。
2. **「構造化された専用セクション + 事後検証（verification）」の複合的アプローチとして
   合理的に確立されている**と評価すべきである。配置のみによる効果は確立されていない。
3. 「確立された定理」や「メカニズム上の常識」としてではなく、
   **LLM の位置依存特性 + 仕様設計上の明瞭性 + 検証容易性に基づく高信頼の設計慣行**
   として位置づけるのが適切である（GPT, Codex 合意）。

---

## 2. 適用強度の選択

### 2.1 強度の段階

| 強度レベル | 内容                                                                                                                                                                                                                                             |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Weak**   | SHOULD be in a dedicated section。例外が広く認められる。                                                                                                                                                                                         |
| **Medium** | 規範的 MUST NOT（rule record の `statement` フィールドの「規範オペレータ」が MUST NOT であるもの）はすべて `prohibitions` に置く。説明的 MUST NOT（rule record 外フィールド、および `statement` で規範オペレータが MUST NOT でないもの）は許容。 |
| **Strong** | あらゆる rule record の `statement` フィールドに含まれる MUST NOT はセクションを問わず `prohibitions` に移動する。                                                                                                                               |
| **Strict** | ファイル全体を通じ MUST NOT のテキストが `prohibitions` セクション以外に現れることを禁じる。                                                                                                                                                     |

### 2.2 推奨強度と根拠（全エージェント合意）

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

GPT・Codex が指摘した「主述語判定の非決定性」を解消するため、
r2 で導入された構文的判定手続きを本プランでも採用する。

**規範オペレータ（deontic operator）の定義**：

`statement` フィールドを左から走査して、「数える」と判定した最初の RFC モーダル
（MUST NOT / MUST / SHOULD NOT / SHOULD / MAY）を規範オペレータとする。

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

### 2.4 判定手続きの限界と将来展望

**現在の限界**（GPT, Codex 指摘）：

- 上記の判定手続きは人間にとっては明確だが、完全な機械検証には正規表現以上の
  自然言語解析を要する場面がありうる。
- authoring スキル自身が掲げる `verification-machine-checkable` との完全な整合は
  現時点では「将来の lint 化」に委ねている。

**将来の改善候補**（Codex 提案）：

- rule record に `statement_modal` 等の明示フィールド（`MUST`, `MUST_NOT`, `SHOULD` 等）を
  導入し、`statement` テキストの曖昧判定を回避する構造的解決。
- 判定手続きを linter として実装し、`verification-machine-checkable` の充足度を向上させる。

---

## 3. 現状の authoring スキルにおける meta-circular 非遵守箇所の特定

### 3.1 調査方法

SKILL.md 全体を通じ `statement` フィールドに MUST NOT が含まれるルールを列挙し、
規範オペレータ判定手続き（セクション 2.3）を適用した。

### 3.2 確定違反（全エージェント合意）

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

| 項目           | 値                                                                                                                                                                                                  |
| -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ルール ID      | `explanatory-must-not-permitted`                                                                                                                                                                    |
| 問題内容       | "is allowed"（許可）と "MUST NOT be treated"（禁止）の 2 述語が同居している                                                                                                                         |
| 参照ルール     | `one-obligation-per-rule`                                                                                                                                                                           |
| 解釈と統合判断 | "is allowed" を MAY 相当と読めば形式的には 1 MUST NOT 述語のみとも解釈できるが、"is allowed" の曖昧性自体が `no-ambiguous-modals` の精神に反するため分割が望ましい（r2, GPT, Codex, Composer 合意） |

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

**注：`definitions.tier-separation.description` について**（Composer 指摘）

この記述中の "MUST NOT interleave" は、tier-separation が適用される文脈では
実質的に規範的禁止として機能する。`explanatory-must-not-permitted` が許容範囲として明示する
"interpretation, semantics, or verification" に definitions フィールドが含まれるかは
SKILL.md 内で明記されていない。

**本プランの方針**：現状は definitions フィールドを許容範囲に含める（説明的使用として扱う）ものとして進める。
修正時に A-1 および A-2 の statement に "definitions" を明示的に追加することで、この曖昧性を解消する。
将来的に `no-interleave-tiers` として prohibitions に独立ルールを追加し definitions から
参照する形への整理は別タスク候補として残す。

---

## 4. 目標設定

### 4.1 目指すべき状態

**Meta-circular 完全遵守状態の定義**（全エージェント合意）：

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

### 4.3 副次的目標（GPT, Codex 提案）

- **機械検証可能性**：「どれが prohibition か」を構文ルールで判定できる状態を目指す。
- **再発防止**：meta-circular 違反が新ルール追加時に再発しないよう、検証メソッドの追加を検討する。

---

## 5. 修正方針

### 5.1 基本方針

**最小変更・最大整合**原則（全エージェント合意）：
既存の構造・ルール数・意図を変えず、
`explanatory-must-not-permitted` の記述をリファクタリングすることで meta-circular 遵守を回復する。

### 5.2 具体的な変更方針

#### 変更 A：`explanatory-must-not-permitted` を分割する

現状の 1 ルール（2 述語）を、以下の 2 ルールに分割する。

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

設計の要点：

- `statement` に definitions を明示的に含める（Composer 指摘の曖昧性を解消）。
- `exceptions` と `verification` を完備する（Composer 指摘のスキーマ不足を解消）。
- 規範オペレータは MUST NOT であり、`prohibitions.items` への配置は Medium 強度に適合する。

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

設計の要点：

- 規範オペレータは MUST（"MUST be classified"）であり、MUST NOT ではない。
  これにより `prohibitions` セクション外への配置が Medium 強度に適合する。
- r1 で提案された "does not constitute an enforceable prohibition" は、
  `use-normative-keywords` が要求する RFC-style normative keywords のいずれにも該当しない
  否定的断言であり不採用とする（Opus 指摘、r2 で修正済み）。
- "MUST be classified as explanatory" + `no-treat-explanatory-must-not-as-prohibition` への
  相互参照とすることで、肯定的義務として明確化し、`use-normative-keywords` との整合性を確保する。
- definitions を許容範囲に明示的に含める。

#### 変更 B：`explanatory-must-not-for-clarity` の確認（変更なし）

`statement` の規範オペレータが SHOULD であり、MUST NOT は例示として登場しているため変更不要。
変更 A 実施後に両ルールの整合性を確認すること。

#### 変更 C：順序調整（変更 A に含む）

A-1 を `prohibitions.items` の末尾に追加することで完了。

### 5.3 `prohibitions.override` の適用範囲（確認済み・変更不要）

`prohibitions.override` は format_obligations / content_obligations / authoring_obligations を
明示的に上書きする。`explanatory-must-not-permitted` が `authoring_obligations` に残留する場合も、
新規 prohibition A-1 が authoring_obligations の A-2 を上書きしうるが、両者は補完関係にあり
矛盾しない。**この点は確認不要**（Composer 確認済み、r2 で未解決事項から削除済み）。

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

**Strict 強度を採用しない理由**（全エージェント合意）：

- 説明的 MUST NOT をすべて `prohibitions` に移動するには rule record への昇格が必要となり、構造が大幅に肥大化する。
- Semantic Gravity Wells の知見から、MUST NOT レコードの膨張は priming リスクを増大させる。
- Medium 強度で大部分の遵守効果を達成できる。

---

## 7. 実施計画

### 7.1 Phase 1：meta-circular 遵守の回復（本タスクの核心）

| Tier                         | 内容                                                                                                                                           |
| ---------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| **Tier 0（構造確認）**       | SKILL.md の全 rule record を列挙し、セクション 3.2〜3.4 の違反確定リストを最新化する。                                                         |
| **Tier 1（変更実施）**       | 変更 A（A-1 追加 + A-2 書き換え）を実施する。                                                                                                  |
| **Tier 2（客観的検証）**     | YAML パース検証・構造検証・`prohibitions-dedicated-section` 遵守確認・`one-obligation-per-rule` 遵守確認・rule-record スキーマ確認を実施する。 |
| **Tier 3（主観的品質確認）** | 変更後の記述が意図を保持しているか人間レビューで確認する。                                                                                     |

### 7.2 Phase 2：`prohibitions` セクションの序盤移動（別タスク）

lost-in-the-middle 対策の補助的強化として、YAML ブロック内で `prohibitions` セクションを
`interpretation` および `precedence_and_conflict` の直後に移動する（Composer 提案を採用し、
Phase として明示化）。

- 大きな構造変更であり Phase 1 完了後に別タスクとして扱う。
- Semantic Gravity Wells の知見から、移動による効果は補助的なものと評価する。
  事後検証（verification メソッド）の強化と組み合わせることが重要。

### 7.3 Phase 3：検証メソッドの強化（別タスク・推奨）

Codex 提案に基づき、以下の検証メソッドの追加を検討する：

| 検証メソッド案                  | 目的                                                           |
| ------------------------------- | -------------------------------------------------------------- |
| `must-not-locality-validation`  | prohibition が `prohibitions.items` の外に存在しないことを確認 |
| `one-modal-per-rule-validation` | 1 ルール 1 モーダルを検査（複合述語の禁止）                    |

これらは Phase 1 の受け入れ条件ではないが、meta-circular 違反の再発防止に有効である。

### 7.4 受け入れ基準（Phase 1）

- `prohibitions.items` 以外のすべての rule record において `statement` の規範オペレータが MUST NOT でない。
- YAML が標準パーサで正常に解析できる。
- rule record スキーマ（id, layer, priority, statement, conditions, exceptions, verification）が全ルールで維持されている。
- `explanatory-must-not-permitted` と `no-treat-explanatory-must-not-as-prohibition` の間で意味的な矛盾がない。

---

## 8. r2 からの主要変更点

| 変更箇所               | r2 の記述                            | r3（本文書）の修正                                                                                                  | 根拠                   |
| ---------------------- | ------------------------------------ | ------------------------------------------------------------------------------------------------------------------- | ---------------------- |
| 確立度の表現           | 「合理的な慣行として支持される」     | 「高信頼の設計慣行として位置づける」に限定。「確立された定理」「メカニズム上の常識」としては扱わない旨を明記        | GPT, Codex             |
| 判定手続きの機械検証性 | 判定手続きを定義したが限界を明示せず | 限界（完全な機械検証には自然言語解析を要する場面がある）を明記し、将来の `statement_modal` フィールド導入構想を追記 | GPT, Codex             |
| definitions の許容範囲 | 暗黙的に許容                         | A-1, A-2 の statement に "definitions" を明示的に含め、曖昧性を解消                                                 | Composer               |
| 検証メソッド強化       | 言及なし                             | Phase 3 として `must-not-locality-validation` / `one-modal-per-rule-validation` を検討事項に追加                    | Codex                  |
| Phase 2 の位置づけ     | 実施計画に含むが別タスク扱い         | 同様に別タスク扱いだが、Phase として明示的にナンバリングし計画性を向上                                              | Composer               |
| エージェント貢献の明記 | レビュー根拠として表形式で言及       | セクション 0.2 に各エージェントの主要貢献を詳述し、統合の透明性を向上                                               | 本プランの自己完結要件 |
| 用語定義               | 本文中で暗黙的に使用                 | セクション 0.4 に用語定義を集約                                                                                     | 自己完結要件           |

---

## 9. 未解決・検討継続事項

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
   セクション 2.3 の判定手続きを機械実行可能な linter として実装し、
   `verification-machine-checkable` の充足度を向上させる。
   Codex 提案の `statement_modal` フィールド導入も合わせて検討する。

5. **説明文での MUST NOT の使用ガイドライン**：
   Codex が指摘した「説明文での MUST NOT を積極利用する方針の副作用」について、
   「必要時のみ許容（SHOULD NOT 常用）」に寄せるかどうかを検討する。
   現状は `explanatory-must-not-for-clarity` が SHOULD で推奨しているため、
   この推奨の強度を下げるかどうかが論点となる。
