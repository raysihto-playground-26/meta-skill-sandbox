# MUST NOT 集中セクション方針および authoring スキル remediation 統合プラン（r3 / gpt）

作成日: 2026-02-23  
対象ファイル（実体）: `.agents/skills/meta-skill.ai-directive-files-authoring/SKILL.md`  
パス補足: `.agents/skills/` が実体であり、`.cursor/skills/` 等の他の `.*/skills/` はすべて `../.agents/skills` へのシンボリックリンクである。  
ステータス: プラン（具体的な変更は本書では行わない）

---

## 0. 目的・非目的・制約

### 0.1 目的

- **目的A（方針）**: AI directive files において、規範的禁止（normative MUST NOT）を **専用セクションに集約**し、遵守・検証を容易にする。
- **目的B（自己準拠）**: authoring スキルが、authoring スキル自身の規則（例: `prohibitions-dedicated-section`, `one-obligation-per-rule`, `no-ambiguous-modals`）を満たす **meta-circular** 状態を回復する。
- **目的C（反証込みの整合）**: MUST NOT 集約の「配置」だけに効果を帰属させず、**構造化 + 事後検証（verification）** の複合として整合的に成立させる。

### 0.2 非目的

- 個別研究の正確性・網羅性の検証を、受け入れ条件にしない（ただし本書で参照する研究的含意は、方針のトーン・リスク評価に反映する）。
- Strict 強度（ファイル全体で MUST NOT 文字列の出現を禁止）を必須目標にしない。

### 0.3 制約（本タスク）

- **AI directive files の具体的な変更は禁止**（本タスクの成果物は `docs/.tmp/plan-r3.gpt.md` のみ）。

---

## 1. 命題への結論（確立度と適用強度）

### 1.1 MUST NOT を序盤の独立セクションに集約することは「確立」しているか

本件は、「MUST NOT を序盤にまとめれば遵守が保証される」という単純命題としては確立していない。  
一方で、以下の複合（構造化 + 事後検証）としては、合理的な慣行として支持されると評価する。

- **lost-in-the-middle**（Liu et al. 2023 など）により、長いコンテキストで情報が中間に埋もれる現象が示され、**禁止事項を独立セクションとして早期提示する設計**は合理的に支持される。
- Instruction Hierarchy（Wallace et al. 2024）/ Constitutional AI の知見は、制約の明示・独立・早期配置が遵守に有利であることを支持する。ただし「ワーキングメモリ相当への保持」は合理的推論であり、直接実証の断言は避ける（OpenReview 2025 の限界指摘を踏まえる）。
- **Semantic Gravity Wells（arXiv 2601.08070, 2026）**は、否定制約が **priming（逆活性化）** により失敗しうること（Priming Failure 87.5%）を示し、**MUST NOT を“並べるだけ”で遵守が上がる**という主張に強い反証を与える。

したがって本プランでは、次を結論とする：

- MUST NOT 集中セクションは **明瞭性・運用・検証**を目的とする「構造化」として採用する。
- 遵守保証は **verification（事後検証）** に置く。
- MUST NOT の過剰増殖は priming リスクを増やしうるため、強度は過剰に上げない。

### 1.2 「どこまでの強さで適用するか」

強度は次の4段階で整理する（Weak / Medium / Strong / Strict）。

- **Weak**: SHOULD（例外許容が広い）。
- **Medium**: 規範的 MUST NOT（rule record の `statement` における規範オペレータが MUST NOT のもの）を `prohibitions.items` に集約。説明的 MUST NOT は許容。
- **Strong**: rule record の `statement` に含まれる MUST NOT を広く `prohibitions` に寄せる。
- **Strict**: ファイル全体で `prohibitions` 以外の MUST NOT 文字列を禁じる。

**推奨: Medium を MUST（強制）として適用**する。

- **理由**:
  - `explanatory-must-not-permitted` / `explanatory-must-not-for-clarity` が示す通り、**MUST NOT の語の出現**と **規範的禁止**は区別される。
  - Strong/Strict は、説明文の rule record 昇格や構造肥大を招き、境界が曖昧になりやすい。
  - Semantic Gravity Wells の含意として、MUST NOT の出現・列挙の膨張は priming リスクを増やしうる。

---

## 2. Medium 強度を「検証可能」にする操作的定義

### 2.1 規範オペレータ（deontic operator）

`statement` を左から走査し、「数える」と判定した最初の RFC モーダル（MUST NOT / MUST / SHOULD NOT / SHOULD / MAY）を **規範オペレータ**とする。

### 2.2 「数えない（説明的）」条件

以下のいずれかに該当する MUST NOT は「数えない（説明的）」として扱う。

1. 単引用符または二重引用符で囲まれたトークンとして出現（例: `'MUST NOT'`）。
2. "the phrase MUST NOT" / "phrase MUST NOT" 等、語句としての言及であることが明示されている出現。
3. RFC keywords の列挙として現れている出現（例: `(MUST, MUST NOT, SHOULD, ...)`）。
4. 括弧内での説明として現れている出現（例: `All normative prohibitions (MUST NOT) MUST ...`）。
5. 「e.g.」「for example」等に続く例示の一部として現れている出現。

### 2.3 Medium 強度（MUST）ルール

- `statement` の規範オペレータが **MUST NOT** である rule record は、**`prohibitions.items` に配置しなければならない（MUST）**。
- 規範オペレータが MUST NOT 以外の rule record、および rule record 外フィールド（interpretation, semantics, definitions, verification, behavior, degradation 等）の MUST NOT は、説明的使用として扱い `prohibitions` への移動を要しない。

---

## 3. 現状の meta-circular 非遵守（確定事項）

### 3.1 確定違反: `explanatory-must-not-permitted` の配置

`authoring_obligations` 内の `explanatory-must-not-permitted` は、`statement` において規範オペレータが MUST NOT と判定されうる（例: "MUST NOT be treated" が最初の「数える」モーダル）にもかかわらず `prohibitions.items` に存在しない。

### 3.2 副次的問題: 1ルール2述語（`one-obligation-per-rule`）

同ルールは "is allowed"（許可）と "MUST NOT be treated"（禁止）が同居しており、1ルール1述語の要件と緊張する。  
（形式的に回避解釈の余地があっても、"is allowed" の曖昧性は `no-ambiguous-modals` の精神に反するため、分割が望ましい。）

---

## 4. remediation 方針（最小変更・最大整合）

### 4.1 目標状態（To-Be）

- `prohibitions.items` 以外のすべての rule record で、`statement` の規範オペレータが MUST NOT でない。
- すべての rule record が rule-record スキーマ（id, layer, priority, statement, conditions, exceptions, verification）に適合する。
- `one-obligation-per-rule` が満たされる（複合述語を排除する）。
- YAML が標準パーサで解析可能である。

### 4.2 変更 A: `explanatory-must-not-permitted` を分割

**A-1（新規・規範的禁止）**: `prohibitions.items` の末尾に追加する（規範オペレータ MUST NOT）。

- id: `no-treat-explanatory-must-not-as-prohibition`
- layer: L2
- priority: 92
- statement: "MUST NOT treat descriptive uses of the phrase 'MUST NOT' in interpretation, semantics, definitions, or verification fields as additional enforceable prohibitions."
- conditions: ["creating AI directive file", "editing AI directive file"]
- exceptions: ["none"]
- verification: "No interpretation, semantics, definitions, or verification field treats descriptive MUST NOT as an enforceable prohibition; human or pattern check."

**A-2（既存・分類の義務）**: `authoring_obligations` に残し、`statement` を MUST NOT 主述語を含まない形へ書き換える（規範オペレータ MUST）。

- id: `explanatory-must-not-permitted`
- layer: L2
- priority: 92
- statement: "Descriptive use of the phrase MUST NOT in interpretation, semantics, definitions, or verification text (as opposed to primary normative statement fields) MUST be classified as explanatory; enforcement as a separate prohibition is governed by no-treat-explanatory-must-not-as-prohibition."
- conditions: ["creating AI directive file", "editing AI directive file"]
- exceptions: ["none"]
- verification: "Descriptive uses of MUST NOT in interpretation, semantics, definitions, or verification text are classified as explanatory and cross-reference no-treat-explanatory-must-not-as-prohibition for enforcement."

### 4.3 変更 B: `explanatory-must-not-for-clarity` は維持（確認のみ）

`statement` の主（規範）オペレータが SHOULD であり、MUST NOT は例示・列挙として登場するため、Medium 強度の下では変更不要。  
ただし変更 A の後に整合を確認する。

---

## 5. Phase 2（別タスク）: `prohibitions` セクションの序盤移動

lost-in-the-middle 対策として、YAML ブロック内の `prohibitions` を `interpretation` および `precedence_and_conflict` の直後へ移動する案を **Phase 2** として扱う。

- 位置移動は補助的手段であり、Semantic Gravity Wells の含意から **遵守保証の中心は verification** に置く。
- Phase 1（meta-circular 回復）完了後に、構造変更のコスト・副作用（可読性、参照順）を評価して実施可否を決める。

---

## 6. 受け入れ基準（Phase 1）

- `prohibitions.items` 以外のすべての rule record において、`statement` の規範オペレータが MUST NOT でない。
- YAML が標準パーサで正常に解析できる。
- rule record スキーマ（id, layer, priority, statement, conditions, exceptions, verification）が全ルールで維持されている。
- `explanatory-must-not-permitted` と `no-treat-explanatory-must-not-as-prohibition` の間で意味的矛盾がない。
- `one-obligation-per-rule` が満たされる（A-2 が MUST、A-1 が MUST NOT の単一述語となる）。

---

## 7. 未解決・検討継続事項（別タスク候補）

1. **`definitions.tier-separation` の扱い**: `definitions.tier-separation.description` の "MUST NOT interleave" は、文脈によっては規範的禁止として機能しうる。現状は説明的使用として扱う前提で進めつつ、将来的に `no-interleave-tiers` を `prohibitions.items` に追加し definitions から参照する整理案を候補として残す。
2. **規範オペレータ判定の lint 化**: セクション 2 の判定手続きを機械実行可能な検査へ落とし込み、`verification-machine-checkable` の充足度を高める（別タスク）。
3. **priming リスク緩和の具体化**: MUST NOT の列挙・名指しが逆活性化しうる点（Semantic Gravity Wells）を踏まえ、記述スタイルとしての緩和策（禁止対象の直接名指し最小化、verification の重視）を別タスクとして検討する。
