# MUST NOT 集中セクション方針および authoring スキル修正計画（Cursor 統合案）

- **作成日**: 2026-02-23
- **作成者**: Cursor（統合検証）
- **対象（実体）**: `.agents/skills/meta-skill.ai-directive-files-authoring/SKILL.md`
- **補足**: `.agents/skills/` が実体。`.*/skills/`（`.cursor/skills/` 等）はシンボリックリンク。修正は実体 1 ファイルのみ。
- **ステータス**: 統合プラン（実装前）
- **制約**: 本プラン作成時点では AI directive files の具体的な変更は禁止（MUST NOT）。

---

## 0. 本プランの位置づけ

本プランは、以下を総合的・包括的に検証し、統合した提案である：

- `docs/.tmp/must-not-section-policy-and-remediation-plan-r2.md`（方針ドキュメント r2）
- `docs/.tmp/plan.gpt.md`
- `docs/.tmp/plan.codex.md`
- `docs/.tmp/plan.opus.md`
- `docs/.tmp/plan.composer.md`

---

## 1. 命題への回答：MUST NOT 集中セクションの確立度と適用強度

### 1.1 「確立されている」か

**結論：単純な「確立」ではなく、「合理的な慣行として支持される」に留める。**

| 観点                                           | 確立度 | 根拠                                                                   |
| ---------------------------------------------- | ------ | ---------------------------------------------------------------------- |
| LLM 注意メカニズム（lost-in-the-middle）の実証 | 高     | Liu et al. 2023 等、複数の独立研究で再現                               |
| 禁止事項の早期配置が遵守率を補助的に高める     | 中     | 直接実証ではなく合理的推論；Semantic Gravity Wells が反証を示す        |
| 独立セクション化による明瞭性向上               | 高     | RFC 2119、法令設計論、deny-by-default で確立                           |
| MUST NOT 明示言及による逆活性化リスク          | 高     | Semantic Gravity Wells (arXiv 2601.08070, 2026)：priming failure 87.5% |
| **構造化（専用セクション）+ 事後検証の複合**   | **高** | 配置のみでは保証にならない；verification による担保が必須              |

**総合評価**：MUST NOT を独立した専用セクションとしてファイルの序盤に集約する設計は、**「構造化された専用セクション + 事後検証（verification）」の複合的アプローチとして合理的に確立されている**。配置のみによる効果が確立されているわけではない。

### 1.2 どこまでの強さで適用するか

**推奨：Medium 強度を MUST（強制）として適用する。**

- **Weak**：SHOULD。例外が広く認められる。→ 規範の一貫性に不足。
- **Medium**：規範的 MUST NOT は `prohibitions` に集約。説明的 MUST NOT は許容。→ **採用**。
- **Strong**：あらゆる statement 内 MUST NOT を prohibitions へ。→ 構造肥大、priming リスク増大。
- **Strict**：ファイル全体で MUST NOT を prohibitions 以外に禁じる。→ 可読性・保守性低下。

**Medium を採る理由**：

1. `explanatory-must-not-permitted` が示すとおり、MUST NOT の「出現」と「規範的禁止」は区別される。
2. interpretation / definitions / verification 等の説明的 MUST NOT を prohibitions に昇格させると構造が肥大化する。
3. Semantic Gravity Wells の知見から、Strong/Strict は priming リスクを増大させる。
4. 機械検証可能な判定手続き（規範オペレータ）で境界を明確化できる。

---

## 2. 現状：authoring スキルの meta-circular 非遵守

### 2.1 確定違反

| 項目           | 値                                                                                                                                                                                                                                     |
| -------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ルール ID      | `explanatory-must-not-permitted`                                                                                                                                                                                                       |
| 所属セクション | `authoring_obligations`                                                                                                                                                                                                                |
| statement      | "When describing interpretation, semantics, or verification (as opposed to primary normative statement fields), descriptive use of the phrase MUST NOT is allowed and **MUST NOT be treated** as additional enforceable prohibitions." |
| 規範オペレータ | MUST NOT（"MUST NOT be treated" が最初の「数える」モーダル）                                                                                                                                                                           |
| 違反内容       | 規範オペレータが MUST NOT だが `prohibitions` に配置されていない                                                                                                                                                                       |
| 参照ルール     | `prohibitions-dedicated-section`                                                                                                                                                                                                       |

### 2.2 副次的問題：複合述語

| 項目       | 値                                                                  |
| ---------- | ------------------------------------------------------------------- |
| ルール ID  | `explanatory-must-not-permitted`                                    |
| 問題内容   | "is allowed"（許可）と "MUST NOT be treated"（禁止）の 2 述語が同居 |
| 参照ルール | `one-obligation-per-rule`                                           |

### 2.3 目指す状態

- **meta-circular 完全遵守**：authoring スキル自身が `prohibitions-dedicated-section`・`one-obligation-per-rule` を満たす。
- **機械検証可能**：規範オペレータ判定手続きに基づき、prohibition の配置を検証できる。

---

## 3. 改善方針：最小変更・最大整合

### 3.1 基本原則

1. **`explanatory-must-not-permitted` を分割**し、規範的禁止を `prohibitions` に移す。
2. **1 ルール 1 述語**を徹底する。
3. **規範オペレータ判定手続き**を明文化し、将来的な lint 化を可能にする。
4. AI directive files の具体的な変更は本プランでは実施しない（別タスクで実施）。

### 3.2 規範オペレータ判定手続き（Medium 強度の操作的定義）

**用語**：規範オペレータ = `statement` を左から走査し、「数える」と判定した最初の RFC モーダル（MUST NOT / MUST / SHOULD NOT / SHOULD / MAY）。

**「数えない（説明的）」の条件**（いずれかを満たす場合）：

1. 単引用符または二重引用符で囲まれたトークン（例：`'MUST NOT'`）
2. "the phrase MUST NOT" 等、語句としての言及が明示されている
3. RFC keywords の列挙（例：`(MUST, MUST NOT, ...)`）
4. 括弧内の説明（例：`All normative prohibitions (MUST NOT) MUST ...`）
5. 「e.g.」「for example」に続く例示の一部

**「数える（規範）」**：上記に該当しない出現。

**Medium 強度のルール**：`statement` の規範オペレータが MUST NOT である rule record は `prohibitions.items` に配置しなければならない（MUST）。

---

## 4. 具体的な変更設計（実施時参照）

### 4.1 変更 A-1：`prohibitions.items` に新規追加

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

### 4.2 変更 A-2：`explanatory-must-not-permitted` の statement 書き換え

規範オペレータを MUST（肯定的義務）に変更し、prohibition への相互参照で補完する。

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

**設計理由**："does not constitute" は RFC モーダルに該当せず `use-normative-keywords` と緊張するため、"MUST be classified as explanatory" + 相互参照とする（Opus 案を採用）。

### 4.3 変更 B：`explanatory-must-not-for-clarity` は変更不要

規範オペレータは SHOULD。MUST NOT は例示として登場するのみ。変更 A 実施後に整合性を確認する。

### 4.4 definitions フィールドの扱い

`explanatory-must-not-permitted` の許容範囲に definitions を含める。`definitions.tier-separation.description` の "MUST NOT interleave" は現状説明的使用として許容。将来的に `no-interleave-tiers` を prohibitions に追加する選択肢は別タスク候補。

---

## 5. 実施計画（Phase 1：meta-circular 回復）

| Tier       | 内容                                                                                                                   |
| ---------- | ---------------------------------------------------------------------------------------------------------------------- |
| **Tier 0** | 全 rule record を列挙し、違反確定リストを最新化                                                                        |
| **Tier 1** | 変更 A-1（prohibition 追加）+ A-2（statement 書き換え）を実施                                                          |
| **Tier 2** | YAML パース・構造検証・`prohibitions-dedicated-section` 遵守・`one-obligation-per-rule` 遵守・rule-record スキーマ確認 |
| **Tier 3** | 人間レビューで意図の保持を確認                                                                                         |

### 5.1 受け入れ基準

- `prohibitions.items` 以外の全 rule record において `statement` の規範オペレータが MUST NOT でない
- YAML が標準パーサで正常に解析できる
- rule record スキーマ（id, layer, priority, statement, conditions, exceptions, verification）が全ルールで維持されている
- `explanatory-must-not-permitted` と `no-treat-explanatory-must-not-as-prohibition` の間に意味的な矛盾がない

---

## 6. Phase 2 および未解決事項

### 6.1 `prohibitions` セクションの序盤移動（別タスク）

lost-in-the-middle 対策の補助的強化として、YAML ブロック内で `prohibitions` を `interpretation` および `precedence_and_conflict` の直後に移動する。Semantic Gravity Wells の知見から、移動による効果は補助的。事後検証の強化と組み合わせることが重要。

### 6.2 その他

- **他の AI directive files への展開**：スキルファイルが増えた場合、同じ Medium 強度を適用するか、authoring スキルへの参照に統一するかを決定する。
- **規範オペレータ判定の lint 化**：判定手続きを機械実行可能な linter として実装し、`verification-machine-checkable` を充足する。
- **Semantic Gravity Wells の緩和策**：禁止対象の直接名指しを避け、望ましい状態を肯定的に記述するガイドラインの追加を検討する。

---

## 7. 各プランからの統合判断

| 論点                  | GPT              | Codex        | Opus                        | Composer           | r2 方針        | 本プラン |
| --------------------- | ---------------- | ------------ | --------------------------- | ------------------ | -------------- | -------- |
| 確立度表現            | 過剰断言を避ける | 強い慣行     | Semantic Gravity Wells 反証 | —                  | 複合アプローチ | 採用     |
| 規範オペレータ        | 構文的判定手続き | 構文ルール化 | —                           | —                  | 左から走査     | 採用     |
| A-2 statement         | —                | —            | MUST be classified          | —                  | r2 案          | 採用     |
| definitions 含む      | —                | —            | —                           | 明示               | 含める         | 採用     |
| prohibitions.override | —                | —            | —                           | 確認不要           | 確認不要       | 採用     |
| Phase 2 明示          | 別タスク         | —            | —                           | 本タスクに組み込み | 別タスク       | 別タスク |

---

## 8. まとめ

1. **MUST NOT 集中セクション**は「構造化 + 事後検証」の複合として合理的に確立されている。配置のみの効果は単純には成り立たない。
2. **適用強度**は Medium（MUST）とする。規範オペレータ判定手続きで機械検証可能にする。
3. **authoring スキル**は `explanatory-must-not-permitted` の分割により meta-circular 遵守を回復する。
4. **本プラン**は AI directive files の具体的な変更を含まない。実施は別タスクとする。
