# 統合プラン（r2, gpt-5.2）：MUST NOT 集中セクション方針と meta-circular 是正ロードマップ

作成日: 2026-02-23  
作成者: gpt-5.2  
成果物: **本ファイルはプランのみ**（AI directive files への具体的変更は本タスク範囲外）

---

## 0. 前提・制約（本タスク）

- **AI directive files（例：`.agents/skills/**/SKILL.md`）の具体的変更は禁止**（MUST NOT）
- 本タスクで行うことは、既存ドキュメントの検証・統合と、統合プラン文書の追加・push のみ
- `.agents/skills/` が実体で、`.*/skills/` はシンボリックリンク（運用上の正規パスは `.agents/skills/`）

---

## 1. 検証対象（読み込んだもの）

### 1.1 既存ドキュメント

- `docs/.tmp/must-not-section-policy-and-remediation-plan.md`（r1）
- `docs/.tmp/must-not-section-policy-and-remediation-plan-r2.md`（r2。ユーザー記載の “v2” 相当として扱う）
- `docs/.tmp/plan.gpt.md`
- `docs/.tmp/plan.opus.md`
- `docs/.tmp/plan.codex.md`
- `docs/.tmp/plan.composer.md`

### 1.2 事実確認（読み取りのみ）

- `.agents/skills/meta-skill.ai-directive-files-authoring/SKILL.md`
  - `prohibitions:` セクションは既に YAML 内の序盤に存在
  - `authoring_obligations` 内の `explanatory-must-not-permitted` が **`statement` に規範的 MUST NOT を含みうる**（meta-circular 上の核心課題は残存）

---

## 2. 命題への結論（「確立度」と「適用強度」）

### 2.1 「MUST NOT だけを独立セクションで序盤に集約」は“確立”とみなしてよいか

**結論**：単体の万能薬として「確立した定理」と断言するのは強すぎるが、**構造化（独立セクション化）＋事後検証（verification）**の複合パターンとしては、実務上の高信頼ベストプラクティスとして扱うのが最も安全で効果的。

- **支持要素**：
  - 長文コンテキストでの位置依存（lost-in-the-middle）→ 重要制約の“埋没”を避ける設計動機になる
  - 仕様設計（RFC/セキュリティポリシー）→ 禁止を独立条項として明確化する慣行
- **反証・限界（重要）**：
  - 否定制約の **priming（逆活性化）** リスク（例：Semantic Gravity Wells 系の示唆）により、「並べれば守る」にはならない
  - よって **“配置”は補助**であり、遵守の実効性は **verification と lint/runner で担保**する必要がある

### 2.2 どこまで強く適用するのが最も効果的か（推奨）

**推奨**：**Medium を MUST 運用**（= “規範的 prohibition のみを集中”し、説明的 MUST NOT は許容）  
Strong/Strict は、文書肥大・運用コスト増・priming リスク増の割に追加効果が不確実。

---

## 3. 統合ポリシー（採用案）

### 3.1 ポリシー目標（狙い）

- **可視性**：禁止（失敗コストが高い）を一箇所に集め、人間・ツール双方の参照点を作る
- **機械検証性**：曖昧な自然言語解釈（“主述語”判定）を避け、手続き化した判定で lint 可能にする
- **反証耐性**：否定制約の限界を前提に、verification を必須にして「並べただけ」を防ぐ

### 3.2 Medium（MUST運用）の操作的定義（deontic operator 方式）

**用語**：
- **rule record**：`id, layer, priority, statement, conditions, exceptions, verification` を持つレコード
- **規範オペレータ（deontic operator）**：`statement` を左から走査し、**「数える」と判定した最初の** RFC モーダル  
  対象：`MUST NOT`, `MUST`, `SHOULD NOT`, `SHOULD`, `MAY`

**「数えない（説明的）」例**（いずれかに該当すれば、その出現は operator 判定から除外）：
- 引用としての言及：`'MUST NOT'` / `"MUST NOT"`
- “the phrase MUST NOT” のような語句言及が明示されている
- RFC キーワード列挙・例示・括弧内注記（例：`(MUST, MUST NOT, ...)` / `(... (MUST NOT) ...)`）

**Medium の規則（MUST）**：
- `statement` の規範オペレータが **MUST NOT** の rule record は、**必ず `prohibitions.items` に置く**
- 規範オペレータが MUST NOT 以外の rule record は、`prohibitions` への移動を要しない（説明的 MUST NOT を含んでもよい）
- rule record 以外の prose フィールド（interpretation/definitions/verification 等）での MUST NOT は、**説明的用法として許容**（ただし、誤読防止の表現上の工夫は推奨）

### 3.3 MUST NOT 集中セクションの“書き方”ガイド（priming を踏まえた最小限）

- **禁止対象の列挙を増やしすぎない**（Strong/Strict 方向の膨張を避ける）
- **禁止の目的を「望ましい状態」側（肯定形）で補助記述**し、禁止文だけに依存しない
- **verification を必須**にして、禁止が守られていることを（人手・ツールのいずれかで）点検できるようにする

---

## 4. 現状の問題（統合診断）

### 4.1 meta-circular の核心

`.agents/skills/meta-skill.ai-directive-files-authoring/SKILL.md` には、
`prohibitions-dedicated-section`（「規範的 MUST NOT は専用セクションへ」）が存在する一方で、
`authoring_obligations` の `explanatory-must-not-permitted` が `statement` に規範的 MUST NOT を含むため、
**自己準拠（meta-circular）を破っている**。

### 4.2 副次問題（再発しやすい要因）

- **1ルール1述語**に反する疑い（“allowed” + “MUST NOT …” の複合）
- “Medium” の境界が自然言語（主述語）依存だと、運用者・将来の自動検証でブレやすい

---

## 5. 是正ロードマップ（本タスクでは「計画のみ」）

### 5.1 Phase 0（棚卸し・基準固定）

- **P0-1**：`statement` の規範オペレータ判定（3.2）を、repo の“運用基準”として明文化（本ファイルを根拠にする）
- **P0-2**：現行 `SKILL.md` の rule record 一覧を抽出し、`prohibitions.items` 外で規範オペレータが MUST NOT のものを列挙

### 5.2 Phase 1（meta-circular 回復の最小変更）

狙い：**規範的 MUST NOT を `prohibitions.items` に収容**し、`authoring_obligations` 側は分類・定義（MUST）にする。

- **P1-1（分割）**：`explanatory-must-not-permitted` を 2 ルールへ分割
  - **新規 prohibition**：説明的 MUST NOT を “追加の enforceable prohibition として扱う”ことを禁止（規範オペレータ MUST NOT）
  - **既存ルールの再定義**：説明的 MUST NOT は **explanatory に分類される（MUST）**、かつ新規 prohibition を参照（自己矛盾の回避）
- **P1-2（スキーマ充足）**：全 rule record が `exceptions` と `verification` を含むことを確認
- **P1-3（1ルール1述語）**：複合述語が残っていないことを確認

**Phase 1 受け入れ基準（AC）**：
- **AC-1**：`prohibitions.items` 以外の rule record に、規範オペレータ MUST NOT が存在しない
- **AC-2**：YAML パース・構造要件（frontmatter + 単一 fenced YAML 等）を満たす
- **AC-3**：各 rule record がスキーマ（id/layer/priority/statement/conditions/exceptions/verification）を満たす

### 5.3 Phase 2（検証の機械化・再発防止）

狙い：主張を強めるより、**lint/CI による拘束力**で実効性を上げる。

- **P2-1**：`must-not-locality-validation`（名称は例）  
  - `prohibitions.items` 外に “規範オペレータ MUST NOT” が存在しないことを機械検査
- **P2-2**：`one-modal-per-rule-validation`  
  - `statement` 内の規範モーダル混在を検査（`one-obligation-per-rule` の客観化）
- **P2-3**：`deontic-operator-detection` の実装（文字列走査のルールを固定し、レビューで再現可能にする）

### 5.4 Phase 3（文書作法の最適化：priming 対策）

- **P3-1**：禁止の増殖（Strong/Strict 的な拡張）を避けるガイドラインの追加
- **P3-2**：説明的 MUST NOT を使う場合は、可能なら引用（`'MUST NOT'`）や “phrase” での言及を推奨し、lint 判定の誤検知も減らす

---

## 6. この統合プランが解決すること／しないこと

- **解決すること**：
  - 「MUST NOT 集中セクションは“補助的に有効”だが保証ではない」という結論の適正化（r1→r2 の修正点を包含）
  - Medium 強度を “機械判定できる手続き”で定義し、運用ブレを減らす
  - meta-circular の核心（`explanatory-must-not-permitted`）を最小変更で是正する道筋
- **解決しないこと（本タスク範囲外）**：
  - 実際の `.agents/skills/**/SKILL.md` への編集・CI 実装（別タスク）

