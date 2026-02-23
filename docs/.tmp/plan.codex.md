# MUST NOT 集中方針: 統合変更プラン（codex案）

作成日: 2026-02-23  
対象:

- `.agents/skills/meta-skill.ai-directive-files-authoring/SKILL.md`
- `.cursor/skills/meta-skill.ai-directive-files-authoring/SKILL.md`  
  ステータス: 実装前プラン（本書は方針定義のみ）

---

## 0. このプランの目的

本プランは、AI directive files における `MUST NOT` の扱いを、**meta-circular に整合しつつ機械検証可能な形へ改善**するための統合方針を定義する。  
あわせて、ユーザー提示の草案（以下「現考案」）の妥当点と課題を明示し、採用可能な修正案に収束させる。

---

## 1. 現考案の評価（妥当点）

現考案には、以下の妥当な要素がある。

1. `MUST NOT` 集中セクションを重視する方向性は正しい。
2. 強度レベル（Weak/Medium/Strong/Strict）を分ける設計は実務的。
3. `explanatory-must-not-permitted` の自己矛盾（配置と複合述語）を特定している点は正確。
4. Tier ベースで実施・検証を分離する工程設計は有効。

---

## 2. 現考案の課題（不一致・要修正点）

### 2.1 根拠強度の表現が強すぎる

- `lost-in-the-middle` は有力な実証知見だが、そこから「MUST NOT 専用セクションが唯一最適」とまでは直接実証されていない。
- Constitutional AI についても、禁止事項の配置順序最適化を直接示す根拠としては限定的。

**修正方針**:  
「確立された定理」ではなく、**強い実務ベストプラクティス**として記述する。

### 2.2 「主述語が MUST NOT」判定は機械検証に不向き

- 現考案の Medium 定義は自然言語判定（主述語認識）を含み、実装者間でぶれやすい。
- `verification-machine-checkable` との整合が弱い。

**修正方針**:  
判定基準を構文的に固定する（例: 正規表現・フィールド規約）。

### 2.3 A-2（分割後ルール）の規範性が弱くなる恐れ

- 「分類記述」のみで規範モーダルを外すと、`authoring_obligations` の enforceable rule として曖昧になりうる。

**修正方針**:  
ルールとして残すなら検証可能な規範文へ再定義する。  
定義文に降格するなら、規範セクション外へ移す。

### 2.4 対象が `.agents` 側に偏っている

- 現実には `.cursor/.../SKILL.md` も存在し、片系のみ更新すると再不整合化する。

**修正方針**:  
**2ファイル同時更新を必須**とする（または片側を生成元化）。

### 2.5 「説明文で MUST NOT を積極利用」方針の副作用

- 説明文での `MUST NOT` を推奨すると、集中セクションの可視性メリットを相殺しやすい。

**修正方針**:  
説明文での `MUST NOT` は「必要時のみ許容（SHOULD NOT 常用）」へ寄せる。

---

## 3. 本プランの最終方針（採用判断）

### 3.1 適用強度

**採用: Medium を強制運用化した “Medium+”**

- 規範禁止（enforceable prohibition）は `prohibitions.items` に集約（MUST）。
- rule record 外の説明文における語句としての `MUST NOT` は、例外的に許容可。
- ただし、説明文での `MUST NOT` は可読性改善が明確な場合に限定（SHOULD）。

### 3.2 運用上の確立度表現

- 「研究上の絶対最適」ではなく、  
  **LLM の位置依存特性 + 仕様設計上の明瞭性 + 検証容易性に基づく高信頼の設計慣行**として定義する。

---

## 4. 目標状態（To-Be）

1. **meta-circular 完全遵守**  
   authoring スキル自身が `prohibitions-dedicated-section` を自分に適用して満たす。

2. **機械検証可能**  
   「どれが prohibition か」を構文ルールで判定できる。

3. **再発防止**  
   `.agents` と `.cursor` の二重管理で差分が出ない運用を持つ。

---

## 5. 変更設計（実装時の具体方針）

### 5.1 ルール設計の正規化

- prohibition 判定を自然言語解釈に頼らず、次で扱う:
  - `prohibitions.items[]` に存在する rule record は prohibition とみなす。
  - それ以外のセクションは prohibition を定義してはならない。

- 可能であれば追加で次を導入:
  - `statement_modal` 等の明示フィールド（`MUST`, `MUST_NOT`, `SHOULD`, ...）
  - これにより `statement` の曖昧判定を回避する。

### 5.2 `explanatory-must-not-permitted` の再構成

現考案Aの方向性（分割）は採用可能。ただし以下で明確化する。

1. **禁止側ルール（prohibitions へ）**
   - id 例: `no-treat-explanatory-must-not-as-prohibition`
   - 目的: 説明的 `MUST NOT` を追加禁止規範として誤読しないことを禁止する。

2. **説明側ルール（authoring or interpretation へ）**
   - 規範ルールとして残すなら、検証可能な単一モーダルで記述する。
   - もしくは rule record ではなく `interpretation` に定義として移す。

3. **1ルール1述語の徹底**
   - 「allowed + MUST NOT」の複合文は禁止。
   - 必ず単一の enforceable predicate に分解する。

### 5.3 セクション配置

- `prohibitions` は YAML ブロック前半（少なくとも `authoring_obligations` より前）に置く。
- 大規模再配置は別タスク化してもよいが、最終的には「早期可視化」を目標とする。

### 5.4 検証メソッド追加（推奨）

`verification.methods` に次を追加する。

- `must-not-locality-validation`
  - 目的: prohibition が `prohibitions.items` の外に出ていないことを確認。
- `one-modal-per-rule-validation`
  - 目的: 1ルール1モーダルを検査（複合述語の禁止）。
- `mirror-sync-validation`（運用ルールでも可）
  - 目的: `.agents` と `.cursor` の対象ファイル同一性を確認。

---

## 6. 実施手順（Tier）

### Tier 0: 事前棚卸し

1. 2対象ファイルの rule record 一覧を抽出。
2. `statement` とセクション所属を対応表化。
3. 現在の meta-circular 非遵守点を確定。

### Tier 1: ルール修正

1. `explanatory-must-not-permitted` の分割または再配置を実施。
2. prohibition ルールを `prohibitions.items` に集約。
3. 1ルール1述語違反を解消。

### Tier 2: 検証強化

1. `must-not-locality-validation` 追加。
2. 必要に応じて `one-modal-per-rule-validation` 追加。
3. YAML parse / structure / no-prose 検証を実行。

### Tier 3: 同期運用

1. `.agents` と `.cursor` を同時更新。
2. 差分が同一方針に従っていることを確認。
3. 将来的には片側自動生成の採否を判断。

---

## 7. 受け入れ基準（Acceptance Criteria）

1. `prohibitions.items` 以外に、enforceable prohibition が存在しない。
2. `one-obligation-per-rule` を満たす（複合モーダルなし）。
3. YAML が標準パーサで成功する。
4. `rule-record-schema`（id/layer/priority/statement/conditions/exceptions/verification）を全 rule record が満たす。
5. `.agents` と `.cursor` の対象ファイルが同方針で同期されている。

---

## 8. リスクと未解決事項

1. **Strict 適用の費用対効果**
   - 説明文から `MUST NOT` を完全排除する利益は限定的で、構造コストが高い可能性。

2. **主述語判定依存の残存リスク**
   - 構文規約化しない限り、再び解釈差が生じる。

3. **セクション前方移動の副作用**
   - 参照順序・可読性への影響を別途確認する必要がある。

---

## 9. 実装時の原則（短縮版）

1. 規範禁止は `prohibitions` に一本化。
2. 1ルール1述語。
3. 人間解釈ではなく機械検証できる基準を優先。
4. `.agents` と `.cursor` を同時に扱う。
5. 根拠表現は「強い慣行」とし、過剰な断定を避ける。
