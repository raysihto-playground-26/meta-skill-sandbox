# MUST NOT 集中セクション方針および meta-circular 改善計画（r3統合版）

作成日: 2026-02-23  
ステータス: 統合プラン（実装禁止条件下）  
対象: AI directive files 方針の統合設計（本書は計画のみ）

---

## 0. 本書のスコープと統合元

### 0.1 スコープ

本書は、次の命題に対する統合回答と改善計画を示す。

1. AI directive files において、`MUST NOT` を独立セクションとして序盤に集約する方針は、どの程度確立しているか。
2. その方針をどの強度で適用するのが最も効果的か。
3. authoring スキルが `MUST NOT` 集中ルールを自己適用できていない（meta-circular 非遵守）現状を、どこを目標にどう改善するか。

### 0.2 統合元ドキュメント

- `docs/.tmp/must-not-section-policy-and-remediation-plan-r2.md`
- `docs/.tmp/plan.gpt.md`
- `docs/.tmp/plan.codex.md`
- `docs/.tmp/plan.opus.md`
- `docs/.tmp/plan.composer.md`

### 0.3 制約

- 本タスクでは AI directive files 本体の具体的変更は実施しない（計画のみ）。
- `.agents/skills/` が実体であり、他の `.*/skills` はシンボリックリンクとして扱う。

---

## 1. 命題への統合結論（r3最終判断）

### 1.1 「MUST NOT 集中セクションは確立しているか」

**結論**: 「集中配置“単独”が万能に確立」とは言い切れない。  
一方で、**「構造化（独立・序盤配置）+ 事後検証（verification）」の複合アプローチ**としては、合理的かつ高信頼の実務規範として支持される。

### 1.2 「どこまでの強さで適用するか」

**結論**: **Medium 強度を MUST で運用**する。  
Strong / Strict は採用しない。

理由（統合要点）:

- Medium は「規範的禁止」を集約しつつ、説明的 `MUST NOT` を許容でき、構造肥大を回避できる。
- Strong / Strict は `MUST NOT` 記述の膨張・複雑化を生み、可読性/保守性の低下を招く。
- Semantic Gravity Wells の知見上、否定対象の過剰明示は priming リスクを増大しうる。

---

## 2. 研究根拠と限界の統合整理

### 2.1 支持根拠

1. **lost-in-the-middle**（Liu et al. 2023 等）  
   長文コンテキストで中間情報が不利になりやすく、制約の早期・独立配置に設計上の合理性がある。

2. **Instruction Hierarchy**（Wallace et al. 2024）  
   制約の明示性・独立性が遵守性に寄与する方向を支持。

3. **仕様設計規範（RFC 2119 等）**  
   禁止（MUST NOT）を明示的・独立的に扱う設計は、文書規範上の整合性が高い。

### 2.2 重要な限界・反証

1. **Semantic Gravity Wells（arXiv:2601.08070, 2026）**  
   否定制約の失敗機序（Priming Failure / Override Failure）を示し、  
   「禁止を並べるだけで遵守が上がる」という単純命題を否定。

2. **命令階層の安定性限界（OpenReview 2025 言及）**  
   優先度指定だけでは安定的統制が難しいケースがあり、配置効果の過信は不適切。

### 2.3 r3 の確立度評価

| 観点 | 評価 |
|---|---|
| 制約の独立・序盤配置が有利である設計合理性 | 高 |
| 「集中配置のみ」で遵守保証できるという主張 | 低 |
| 「集中配置 + verification」の複合運用 | 高 |
| 最適配置位置の定量的最適解 | 未確定 |

---

## 3. 現状問題（meta-circular 非遵守）の統合診断

### 3.1 確定問題

1. `explanatory-must-not-permitted` が `authoring_obligations` にあり、  
   `statement` 内で規範的 `MUST NOT` を持つため、`prohibitions-dedicated-section` と衝突。

2. 同ルールは「allowed」と「MUST NOT be treated」を同居させ、  
   `one-obligation-per-rule` の観点で分離が望ましい。

### 3.2 非違反として扱う境界領域（Medium 前提）

- `statement` 内でも、列挙・引用・例示としての `MUST NOT` は規範オペレータ扱いにしない。
- rule record 外（interpretation / definitions / verification / degradation 等）の `MUST NOT` は説明的使用として許容。

### 3.3 追加で明確化すべき点

- `definitions` を説明的許容範囲に含める扱いを明示する（将来の誤読防止）。
- `prohibitions.override` は矛盾原因ではなく、補完関係で運用可能であることを前提にする。

---

## 4. 目標状態（To-Be）

### 4.1 目標定義

**meta-circular 完全遵守**:  
authoring スキルが自分自身に対して、次を満たす状態。

1. 規範オペレータが `MUST NOT` の rule record はすべて `prohibitions.items` に存在する。
2. 全 rule record が「1ルール1述語」を満たす。
3. 説明的 `MUST NOT` と規範的 `MUST NOT` の境界が明示され、検証可能である。

### 4.2 受け入れ基準（計画段階）

- `prohibitions.items` 以外の rule record に規範オペレータ `MUST NOT` が存在しない。
- rule-record スキーマ（`id, layer, priority, statement, conditions, exceptions, verification`）を全件満たす。
- YAML 構造/解析が成立する。
- `explanatory` 系ルールと prohibition 系ルールの間で意味矛盾がない。

---

## 5. 方針決定（r3）

### 5.1 採用強度

**Medium（MUST運用）**

### 5.2 Medium の操作的定義（統合版）

`statement` を左から走査し、最初に「数える」RFCモーダルを規範オペレータとする。  
対象モーダル: `MUST NOT`, `MUST`, `SHOULD NOT`, `SHOULD`, `MAY`

**数えない（説明的）例**:

1. `'MUST NOT'` のような引用トークン
2. `the phrase MUST NOT` のような語句言及
3. RFCキーワード列挙（例: `(MUST, MUST NOT, SHOULD, ...)`）
4. 括弧内の説明的注記
5. 例示（`e.g.` / `for example`）の一部

**数える（規範）**:

- 上記以外のモーダル出現

### 5.3 判定結果に基づく配置規則

- 規範オペレータが `MUST NOT` の rule record: `prohibitions.items` に配置（MUST）
- それ以外の rule record: `prohibitions` 移動不要
- rule record 外の `MUST NOT`: 説明的使用として許容（ただし誤解釈禁止）

---

## 6. 改善計画（実装禁止条件下の設計）

### 6.1 Phase 1（必須）: 核心違反の解消設計

**変更設計A（分割）**

1. `prohibitions.items` へ新規追加  
   `id: no-treat-explanatory-must-not-as-prohibition`
2. `authoring_obligations.explanatory-must-not-permitted` を  
   「説明的分類 + 相互参照」へ再定義
3. 各 rule record に `exceptions` / `verification` を必須充足

### 6.2 Phase 2（推奨・別タスク）: 配置最適化

- `prohibitions` セクションを YAML 前方へ移動し、可視性を高める。
- ただし効果は補助的と位置づけ、verification 強化と組み合わせる。

### 6.3 Phase 3（推奨・別タスク）: 機械検証化

- 規範オペレータ判定手続きの lint 化
- `must-not-locality` / `one-modal-per-rule` 相当の自動チェック整備

---

## 7. 実施時の検証計画

### 7.1 最低限の客観検証

1. YAML パース検証
2. 構造検証（単一YAMLブロック規律など）
3. rule-record スキーマ検証

### 7.2 方針準拠検証

1. `MUST NOT` 規範オペレータの所在検証（`prohibitions.items` への局所化）
2. `one-obligation-per-rule` 検証
3. 説明的 `MUST NOT` の誤規範化防止検証

---

## 8. リスクと継続検討事項

1. **Strong/Strict の費用対効果**  
   効果上積みが小さい一方で、文書肥大と可読性低下のリスクが高い。

2. **definitions 領域の解釈揺れ**  
   実質規範に読める表現は、将来 prohibition への昇格整理を検討する。

3. **配置改善の過信**  
   配置のみで遵守保証はできないため、verification を主軸に据える。

---

## 9. 最終方針要約（実行可能な意思決定）

1. `MUST NOT` 集中セクションは、**単独での万能策ではない**。  
2. 最適運用は、**Medium強度（MUST）+ 事後検証**。  
3. 目標は「authoring スキルの meta-circular 完全遵守」。  
4. 具体的改善は「核心違反の分割解消 → 配置最適化 → lint化」の段階実施。  
5. 本タスクでは実装せず、上記を統合計画として確定する。

---

## 参考（第三者研究・規範）

- Liu et al., 2023, Lost in the Middle
- Wallace et al., 2024, Instruction Hierarchy
- Semantic Gravity Wells, arXiv:2601.08070, 2026
- RFC 2119
