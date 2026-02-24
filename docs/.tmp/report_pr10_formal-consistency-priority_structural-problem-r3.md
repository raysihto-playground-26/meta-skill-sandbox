# PR #10 を契機に顕在化した「形式整合性優先」の構造問題レポート（R3 改訂版）

## 本書の目的

本書は、PR #10 に付随して観測されたレビューコメント（`discussion_r2841492177`）を「きっかけ」として、
`SKILL.md` が `docs/ai-directive-files-policy.md`（以下「ポリシー」）に照らして抱える構造的問題を、
課題認識として共有するためのレポートである。

本 R3 版は、R2 版が依拠していた「inference efficiency first」という私的な設計公理ではなく、
**ポリシーを唯一の根拠として固定**し、そこから問題を演繹する。

---

## 1. ポリシーを根拠として固定

### 1.1 ポリシーの位置付け

`docs/ai-directive-files-policy.md` は本リポジトリにおける **ゴールドポリシー** である。

> "This document is the canonical policy for AI directive files in this repository."
> "If any guidance conflicts, this policy wins."

ポリシーは次の本質的方向性を宣言している：

> "Design toward a system where only the highest-impact instructions are transmitted reliably,
> at minimal cost (minimal context)."

これは **MUST** ではなく設計の向かうべき方向性として示されており、
個別の MUST/SHOULD 規定はそこから導出される。

### 1.2 本件に関連するポリシーの規定

以下は本問題に直接関連するポリシー条項である（強調は引用者）。

#### Conditions and exceptions (MUST)

> "Anti-pattern to avoid: **Do not use `conditions: always`.**"
> "For unconditional rules, omit `conditions` entirely."
> "Only add `conditions` when there is a real trigger that matters."
> "This prevents 'definition bloat' where obvious terms must be defined just
> because they appear as condition values."

#### Definitions policy (MUST)

> "Define only non-obvious terms that materially change interpretation."
> "Do not define words that are universally understood in this context
> (example: do not define 'always', 'generally', 'usually' by default)."

#### Verification and testing (SHOULD)

> "Do not rely on 'final comprehensive rule checking' inside the same LLM call
> as the primary enforcement mechanism."
> "Prefer: Externalize validation ... when the constraint is important and cheaply checkable."

### 1.3 ポリシーの参照ガイド文書（規範的マッピング）

ポリシーは `docs/guides.sub/` 以下の5つのガイドを参照素材として採用している。
本問題に特に関連するのは以下の採用箇所である：

- `ai-directive-files-best-practices.md` — 節 5.1「Conditions as Enumerations」:
  "Conditions MUST be specified as explicit triggers, not prose."
- `llm-instruction-robustness-workaround-audit-manual.md` — 節 2「Post-Hoc Validation」:
  生成後に外部で検証せよ
- `llm-meta-control-instability.md` — 節 4「The Core Insight」:
  "An LLM is a generator, not a governor."
  自己内最終チェックは信頼できない

---

## 2. 観測された事象（きっかけ）

対象コメント: `https://github.com/raysihto-playground-26/meta-skill-sandbox/pull/10#discussion_r2841492177`

コメントの要旨（要約）：

- `interpretation.condition_identifiers` は `conditions` 配列の識別子が `definitions`
  のキーと厳密一致することを MUST で要求している。
- 一方、多くのルールが `conditions: ["always"]` を使用しているが、`definitions` に
  `always` のエントリが存在しない。
- よって `SKILL.md` は自己矛盾（self-violation）している。

このコメント自体の正否よりも重要なのは、**この種の指摘がポリシーに照らして妥当かどうか**である。
以下、ポリシーを根拠として問題を分類する。

補足（パスの実体）: `.agents/skills/` が実体であり、他の `.*/skills/` はシンボリックリンクである。

---

## 3. 問題のレイヤー分類（MUST 違反 / SHOULD 違反の分離）

### 3.1 Layer 1 — MUST 違反（即時修正が必要）

#### P3-M1: `conditions: always` の使用（ポリシー明示的禁止）

| 項目         | 内容                                                                                                                                                                   |
| ------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **違反箇所** | `prohibitions` の `no-prose`、`no-invent` など多数のルール                                                                                                             |
| **違反規定** | ポリシー「Conditions and exceptions (MUST)」: "Do not use `conditions: always`."                                                                                       |
| **影響**     | `always` が `definitions` に存在しないため `condition_identifiers` の MUST 要求と矛盾する                                                                              |
| **根本原因** | `rule-record-schema`（後述 P3-M2）が `conditions` を必須フィールドとして要求するため、<br>無条件ルールにも `conditions` フィールドを記載せざるを得ない構造になっている |

#### P3-M2: `rule-record-schema` が `conditions` を必須フィールドとして要求（ポリシーと矛盾）

| 項目               | 内容                                                                                                                               |
| ------------------ | ---------------------------------------------------------------------------------------------------------------------------------- |
| **違反箇所**       | `authoring_obligations` の `rule-record-schema` ルール                                                                             |
| **現行のルール文** | "having exactly the following fields: id, layer, priority, statement, **conditions**, exceptions, verification"                    |
| **違反規定**       | ポリシー「Conditions and exceptions (MUST)」: "For unconditional rules, omit `conditions` entirely."                               |
| **影響**           | `conditions` を必須とすることで、無条件ルールに `conditions: always` を強制する構造を生む。<br>これが P3-M1 の根本原因となっている |

> **注意**: P3-M1 と P3-M2 は直列した因果関係にある。P3-M2 を修正しなければ P3-M1 を根本解決できない。

### 3.2 Layer 2 — SHOULD 違反（設計上の問題）

#### P3-S1: 検証戦略が同一生成パスの最終セルフチェックを一部前提としている

| 項目         | 内容                                                                                                                                                                  |
| ------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **該当箇所** | 複数ルールの `verification` フィールドに "human or pattern check" と記載されているが、<br>runner の分離が明示されていない箇所がある                                   |
| **違反規定** | ポリシー「Verification and testing (SHOULD)」: "Do not rely on 'final comprehensive rule checking'<br>inside the same LLM call as the primary enforcement mechanism." |
| **影響**     | LLM は生成器であり統治者ではない（`llm-meta-control-instability.md` 節 4）。<br>自己チェックに依存した検証は信頼性が低い                                              |
| **優先度**   | SHOULD（MUST ではない）。P3-M1/M2 の修正後に対応を検討する                                                                                                            |

---

## 4. 望ましい解決クラスの先定義

**以下の解決クラスを優先順位順に定義する。**
各クラスはポリシーの「最小コストで最大の遵守安定性」という方向性に沿うよう、
最小変更から順に配置する。

### 解決クラス A（最優先・MUST 違反修正）

**P3-M2 を修正してから P3-M1 を修正する（順序が重要）**

- A-1: `rule-record-schema` の `conditions` フィールドを必須から任意（optional）に変更する。
  これにより「`conditions` を省略できる」構造を保証する。
- A-2: 全ての無条件ルール（`conditions: ["always"]` を持つルール）から
  `conditions` フィールドを削除する。

期待効果:

- `always` が `conditions` 配列から消えるため、`condition_identifiers` との矛盾が解消する
- ポリシーの「Definitions policy」が示す「`always` を定義しない」方針とも整合する
- トークン削減: 削除されるフィールドの分だけコンテキストが軽量化する

### 解決クラス B（A に付随・結果整合）

- B-1: `condition_identifiers` の文言を修正し、「`conditions` フィールドが存在する場合にのみ
  exact-match が適用される」ことを明示する。
  A-2 の実施後は `always` が `conditions` に現れなくなるため、この修正は念のための明示化である。
- B-2: `constraints` フィールドが参照する `'always'` の記述（"Rules with conditions other than
  'always' apply only when..."）を、「`conditions` フィールドが存在しないルールは無条件に適用」
  という表現に置き換える。

### 解決クラス C（推奨・SHOULD 対応）

- C-1: `failure_states_and_degradation` に、検証が外部化（post-hoc validation）を前提とする旨を
  明示する。
  ポリシー「Verification and testing (SHOULD)」および
  `llm-meta-control-instability.md` 節 5.1「Externalize Meta-Control」に準拠する。

---

## 5. R2 版との差異と方針転換の宣言

### 5.1 R2 版の問題

R2 版は以下の前提に基づいていた：

1. `conditions: always` は温存する（変更しない）
2. `inference_reserved_sentinels` というカーブアウト機構を追加し、`always` を definitions 要求から免除する
3. `design_axiom` というポリシーではなく私的な設計公理を SKILL.md に追加する

これらは次の理由で不適切である：

- **前提 1**: ポリシーが明示的に禁止している `conditions: always` を温存することは、
  MUST 違反を恒久化する。
- **前提 2**: カーブアウト機構の追加はトークン増加であり、かつ根本原因（P3-M2）を修正しない。
  ポリシーの「最小コスト」方針に反する。
- **前提 3**: `design_axiom` の内容はポリシーが既に宣言していることと重複する。
  ポリシーが golden policy である以上、SKILL.md で再宣言する必要はない。

### 5.2 R3 版の方針

- **ポリシー準拠を最優先**とし、ポリシーの MUST 規定に違反する箇所を最小変更で修正する。
- `conditions: always` は **削除**する（温存しない）。
- 新たなカーブアウト機構やメタ概念の追加は **行わない**（トークン増加・ポリシー重複を避ける）。
- 解決クラス A → B → C の順で、最小の変更から順に実施する。

---

## 6. 合意すべき課題認識

本書で共有したい課題認識は、ポリシー語彙で次のとおりである。

| 課題 ID     | 種別        | 内容                                                                                                                                        |
| ----------- | ----------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| P3-M2       | MUST 違反   | `rule-record-schema` が `conditions` を必須フィールドとして要求しており、<br>ポリシーの「無条件ルールは `conditions` を省略せよ」と矛盾する |
| P3-M1       | MUST 違反   | `conditions: always` が多数のルールで使用されており、<br>ポリシーが明示的に禁止する anti-pattern に該当する                                 |
| P3-S1       | SHOULD 違反 | 検証戦略の一部が同一生成パスの自己チェックを前提としており、<br>ポリシーが推奨する外部化（post-hoc validation）に沿っていない               |
| R2-方針誤り | 方針        | R2 が提案した sentinel carve-out はポリシー違反を温存し、<br>かつトークン増加を招くため撤回する                                             |

`discussion_r2841492177` は、上記の P3-M1 と P3-M2 が組み合わさって生じた
**ポリシー違反の観察可能な症状**であり、それ自体は正当な観察である。
ただし推奨される解決策（`always` を `definitions` に追加する）はポリシーの
Definitions policy に違反するため採用しない。
正しい解決策は解決クラス A である。
