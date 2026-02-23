# MUST NOT 集中セクション方針と meta-circular 改善の統合プラン（r2 / codex）

作成日: 2026-02-23  
対象: AI directive files（主対象は `.agents/skills/meta-skill.ai-directive-files-authoring/SKILL.md`）  
ステータス: 実装前プラン（本書は方針・手順定義のみ）

---

## 0. 前提・制約

- 本タスクでは **AI directive files の具体的変更は実施しない**（MUST NOT）。
- 実体ディレクトリは `.agents/skills/`。`.cursor/skills/` など他の `.*/skills/` はシンボリックリンク。
- 目標は、次回の実装タスクで迷いなく適用できる **統合方針** を確定すること。

---

## 1. 検証対象と入力資料

### 1.1 検証した資料

- `docs/.tmp/must-not-section-policy-and-remediation-plan.md`
- `docs/.tmp/must-not-section-policy-and-remediation-plan-r2.md`
- `docs/.tmp/plan.gpt.md`
- `docs/.tmp/plan.codex.md`
- `docs/.tmp/plan.composer.md`
- `docs/.tmp/plan.opus.md`

### 1.2 指定ファイル名との対応

指定された `docs/.tmp/must-not-section-policy-and-remediation-plan-v2.md` は現時点で確認できなかった。  
そのため、内容的に後継・同系統と判断できる `...-plan-r2.md` と `...-plan.md` を併読し、統合判断を行った。

---

## 2. 統合結論（最重要）

### 2.1 「MUST NOT 集中セクション」は確立されているか

**結論**: 「絶対定理」とまでは言えないが、実務上は高信頼で採用すべき設計慣行。  
ただし効果の本体は「配置のみ」ではなく、**構造化 + 事後検証（verification）** の組み合わせにある。

理由（統合）:

1. lost-in-the-middle 系の知見は「前方配置・独立提示」の有効性を支持する。
2. 仕様設計（RFC 的規範記述）では禁止の独立セクション化が明瞭性を高める。
3. 一方で否定命令には逆活性化（priming）リスクがあり、MUST NOT を増やすだけでは保証にならない。

### 2.2 どの強度で適用するべきか

**採用方針: Medium+（MUST 運用）**

- 規範的禁止（rule record の `statement` における規範オペレータが `MUST NOT`）は、必ず `prohibitions.items` に置く。
- 説明的 MUST NOT（例示・語句言及・rule record 外 prose）は許容する。
- ただし説明的 MUST NOT は、誤解釈を避けるため分類と検証をセットにする。

**Strong/Strict を採らない理由**:

- ファイル肥大化・可読性低下・保守コスト増大に対して追加効果が限定的。
- MUST NOT の過剰露出は逆活性化リスクを増やしうる。

---

## 3. 目標状態（To-Be）

### 3.1 到達目標

1. **Meta-circular 完全遵守**  
   authoring スキルが自分自身に対しても `prohibitions-dedicated-section` 等を満たす。

2. **境界判定の決定性**  
   「規範的 MUST NOT」と「説明的 MUST NOT」を、人依存でなく再現可能に判定できる。

3. **機械検証可能性**  
   少なくともパターン検査で違反を検知できる（将来的 lint 化を含む）。

### 3.2 成功基準（Acceptance Criteria）

- AC-1: `prohibitions.items` 以外に、規範オペレータ `MUST NOT` の rule record がない。
- AC-2: `one-obligation-per-rule` を満たす（1 rule = 1 enforceable predicate）。
- AC-3: 全 rule record が完全スキーマ（id/layer/priority/statement/conditions/exceptions/verification）を満たす。
- AC-4: YAML/構造検証が成功する。
- AC-5: 説明的 MUST NOT の扱いが規則化され、誤って禁止ルール化されない。

---

## 4. 適用ポリシー（Medium+）の操作的定義

### 4.1 規範オペレータ判定

`statement` を左から走査し、最初に「規範として数える」RFC モーダル  
（`MUST NOT`, `MUST`, `SHOULD NOT`, `SHOULD`, `MAY`）を規範オペレータとする。

### 4.2 「数えない（説明的）」出現

以下は説明的用法として扱う:

- 引用符内トークン（例: `'MUST NOT'`）
- 「the phrase MUST NOT」のような語句言及
- RFC キーワード列挙
- 括弧内の補足説明
- 明確な例示文脈（e.g., for example）

### 4.3 強制ルール

- 規範オペレータが `MUST NOT` の rule record は `prohibitions.items` に配置（MUST）。
- それ以外の MUST NOT 出現は説明的扱い可能（ただし誤解釈防止の注記・検証を推奨）。

---

## 5. remediation 方針（実装タスク向け）

### 5.1 優先修正（核心）

`explanatory-must-not-permitted` の meta-circular 問題を解消する。

- 方針A: 「説明的 MUST NOT を禁止として扱ってはならない」を `prohibitions.items` 側の独立ルールに分離。
- 方針B: `authoring_obligations` 側の `explanatory-must-not-permitted` は、分類/解釈ルールとして単一述語化。
- 方針C: 新規・既存ともに `exceptions` と `verification` を省略しない（完全スキーマ維持）。

### 5.2 境界の明示

- `interpretation`, `semantics`, `verification` に加え、必要なら `definitions` の扱いを明文化。
- rule record 外 prose の MUST NOT は「説明的」として残しつつ、関連 prohibition への参照で誤読を防ぐ。

### 5.3 追加改善（別フェーズ）

- `prohibitions` セクションの YAML 内前方移動（大きめの構造変更）。
- 規範オペレータ判定の lint 化。
- 説明的 MUST NOT の常用抑制ガイド（必要時のみ使用）。

---

## 6. 実施フェーズ（次回の実装順）

### Phase 0: 棚卸し

- 全 rule record とセクション所属を一覧化。
- `statement` の規範オペレータを判定し、違反候補を確定。

### Phase 1: 最小変更で meta-circular 回復

- 核心違反を分割・再配置して AC-1/AC-2 を達成。
- ルールレコードの完全スキーマを満たす。

### Phase 2: 検証強化

- YAML/構造/ローカリティ検証を実行。
- `MUST NOT locality` と `one-modal-per-rule` の半自動チェックを導入。

### Phase 3: 構造最適化（任意）

- `prohibitions` の前方配置、冗長ルール統合、lint 固定化を段階適用。

---

## 7. リスクと対策

| リスク | 影響 | 対策 |
|---|---|---|
| MUST NOT の過剰列挙による逆活性化 | 禁止違反率の上昇 | 配置最適化だけに依存せず verification を必須化 |
| Medium 判定の曖昧運用 | 運用者間の判定ブレ | 規範オペレータ判定手続きの明文化 + lint 化 |
| 説明文 MUST NOT の誤読 | 禁止ルールの重複・衝突 | 分類ルールと cross-reference を義務化 |
| 大規模並べ替えの副作用 | 差分拡大・レビュー負荷 | Phase 分離（まず核心修正、配置最適化は後段） |

---

## 8. 今回の提案の採択事項（決定版）

1. 「MUST NOT 集中セクション」は **高信頼の設計慣行として採択**する。  
   ただし、効果は **構造化 + 事後検証** の複合で成立するものとして扱う。

2. 適用強度は **Medium+（MUST 運用）** を採択する。  
   Strong/Strict は現段階では採用しない。

3. remediation の第一優先は  
   `explanatory-must-not-permitted` の分割と完全スキーマ整備に置く。

4. 実装は段階適用（Phase 0-3）で進め、**まず meta-circular 回復を完了**する。

---

## 9. 本プランの非目的（明示）

- 本書は方針文書であり、AI directive files の即時編集は行わない。
- 研究論文の厳密再現実験を本プランの成立条件にはしない。
- リポジトリ全体への一括横展開は、次タスクとして分離する。

