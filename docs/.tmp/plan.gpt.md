## MUST NOT 集中セクション方針および authoring スキル修正計画（GPT案）

- **作成日**: 2026-02-23
- **対象（実体）**: `.agents/skills/meta-skill.ai-directive-files-authoring/SKILL.md`
- **補足**: `.cursor/skills` 等の他の `.*/skills` は実体 `.agents/skills` を指すシンボリックリンクであり、修正は実体側に行う。
- **ステータス**: プラン（未実装）

---

## 0. 目的と非目的

### 0.1 目的

- **目的A**: 「MUST NOT（禁止）」の解釈・運用を **単一ソース化**し、衝突時に禁止が優先されることを **決定的**にする。
- **目的B**: authoring スキル（本ファイル）が、自身の規則を自身でも満たす **meta-circular** 状態を回復する。
- **目的C**: 「MUST NOT を集中セクションに置く」強制（Medium強度）を、曖昧さを最小化して **検証可能**にする。

### 0.2 非目的

- LLM の注意特性に関する学術的主張（個別論文の正確な引用・検証）を、本プランの受け入れ条件にしない。
- 全ディレクティブファイル全体への横展開は、本プランでは必須にしない（別タスク化）。

---

## 1. 「現考案」（提示草案）との整合・不一致・課題

### 1.1 整合している点（妥当）

- **骨格（Medium強度）**: 「規範的禁止（MUST NOT）を `prohibitions` に集約し、説明的用法は許容する」は合理的。
- **meta-circular の診断**: `explanatory-must-not-permitted` の配置と複合述語（1ルール2述語）の問題提起は妥当。
- **Strict を避ける判断**: 構造肥大・追加効果の逓減を考慮して Medium を採るのは実務的。

### 1.2 不一致・課題（修正推奨）

- **課題A: 「確立されている」という断言が強い**
  - lost-in-the-middle 等から「早期配置が有利」は合理的に示唆される一方、AI directive files における「MUST NOT 集中セクション」が“常識・規範として確立”とまで断言するには、根拠の検証・引用の正確性・適用範囲の限定が不足しやすい。
  - 本リポジトリの実効性は、研究の断言より **runner/リンタで機械的に強制・検証できる設計**に依存するため、主張は「合理的・有効な設計パターン」程度に抑え、強制力は実装（検証）で担保するのが安全。

- **課題B: Medium の境界（「主述語」）が非決定的**
  - 「主述語」「参照・列挙・例示」の判定は人間には理解可能だが、機械検証には不向きになりやすい。
  - authoring スキル自身が掲げる「検証可能」「機械チェック可能」と緊張しうるため、Medium強度を採るなら **判定手続き（決定規則）**を明文化する必要がある。

- **課題C: “早期配置が効く”主張と、`prohibitions` の位置が整合しにくい**
  - 現状の authoring スキルでは `prohibitions` が YAML ブロックの中ほどにある。
  - 早期配置の利益を最大化するなら `interpretation` の直後に置くのが一貫するが、これは構造変更であり、本プランでは **別タスク（任意）**として扱う。
  - その場合、「最大化は今はしない」旨を方針文書のトーンに反映するのが整合的。

---

## 2. 目標状態（受け入れ基準）

### 2.1 meta-circular（自己準拠）受け入れ基準

- **AC-1**: `prohibitions.items` 以外の rule record について、`statement` の規範オペレータ（後述）が `MUST NOT` であるレコードが存在しない。
- **AC-2**: `one-obligation-per-rule` を満たす（複数の規範述語を同一 `statement` に混在させない）。
- **AC-3**: YAML パースが標準パーサで成功し、既存の「構造検証」「no-prose 検証」を満たす。

### 2.2 Medium強度（集約）の受け入れ基準

- **AC-4**: 「規範的禁止」の判定手続きが文書化され、その手続きに基づき `prohibitions.items` が規範的禁止の単一ソースとなっている。
- **AC-5**: 「説明的 MUST NOT」は許容されるが、それが規範禁止として誤解釈されないための扱い（分類・無効化ルール）が決定的に定義されている。

---

## 3. Medium強度を「検証可能」にするための定義（提案）

### 3.1 用語

- **rule record**: `id, layer, priority, statement, conditions, exceptions, verification` を持つレコード。
- **規範オペレータ（deontic operator）**: `statement` に現れる RFC モーダルのうち、**判定対象として数える最初のもの**。
- **判定対象として数える RFC モーダル**: `MUST NOT`, `MUST`, `SHOULD NOT`, `SHOULD`, `MAY`。

### 3.2 規範オペレータ決定手続き（案）

`statement` を左から走査して、以下の規則で「数える/数えない」を決め、最初に数えたモーダルを規範オペレータとする。

- **数えない（説明的）**:
  - 単引用符または二重引用符で囲まれたトークンとしての出現（例: `'MUST NOT'`）。
  - 「phrase MUST NOT」「the phrase MUST NOT」等、**語句としての言及**であることが明示されている出現。
  - 「RFC keywords の列挙」「例示」コンテキストで、明確に「キーワード一覧」として現れている出現（例: `RFC-style normative keywords (MUST, MUST NOT, ...)`）。

- **数える（規範）**:
  - 上記「数えない」に該当しない `MUST NOT` 等の出現。

### 3.3 Medium強度の規則（案）

- `prohibitions.items` に置くべきもの:
  - 規範オペレータが **`MUST NOT`** の rule record。
- `prohibitions.items` に置く必要がないもの:
  - 規範オペレータが `MUST NOT` 以外の rule record で、`statement` 内の `MUST NOT` が「数えない（説明的）」として現れているだけのもの。
- rule record 以外（interpretation / definitions / verification の文字列等）:
  - 本プランの Medium強度では **説明的用法を許容**する（ただし、規範として解釈しないことを明示する）。

> 注: ここでの主眼は「集約の強制」を機械判定可能にすることであり、LLM への心理的効果（早期配置）を最大化することは必須要件にしない。

---

## 4. 現状（authoring スキル）の問題点（確定事項）

### 4.1 meta-circular 違反（確定）

- `authoring_obligations` 内の `explanatory-must-not-permitted` は `statement` に規範的 `MUST NOT` を含みうるのに `prohibitions` に存在しない。
- 同レコードは「allowed（許容）」と「MUST NOT be treated（禁止）」が同居し、`one-obligation-per-rule` の趣旨に反する。

### 4.2 “Strict” を採らない限りは違反としない点（現方針）

以下のような rule record 外文字列（interpretation 等）の `MUST NOT` は、Mediumでは許容対象とする（ただし誤解釈防止策は必要）。

---

## 5. 変更方針（最小変更・最大整合）

### 5.1 方針概要

- **方針1**: `explanatory-must-not-permitted` を「1ルール1述語」に分解し、規範的禁止は `prohibitions.items` に移す。
- **方針2**: 「説明的 MUST NOT は規範禁止ではない」という扱いは、`statement` を **定義文（分類文）**へ落として `MUST NOT` を規範的に使わない形にする。
- **方針3**: Medium強度の判定手続きを、authoring スキル内の `verification` もしくは解釈セマンティクスとして明示し、将来 lint 可能にする。

### 5.2 具体変更案（設計）

#### 変更A: `explanatory-must-not-permitted` を分割

- **A-1（新規・禁止）**: `prohibitions.items` に追加
  - **id**: `no-treat-explanatory-must-not-as-prohibition`
  - **statement**: 解釈・セマンティクス・検証フィールドにおける説明的な `MUST NOT` を、追加の規範的禁止として扱うことを禁じる（規範オペレータは `MUST NOT`）。
  - **verification**: 少なくとも人手でのチェック手順を定義し、将来的な lint 化を可能にする。

- **A-2（既存・定義へ書き換え）**: `authoring_obligations` に残す（規範オペレータは `MUST` または定義文）
  - **id**: `explanatory-must-not-permitted`（名称維持）
  - **statement**: 「説明的 MUST NOT」の分類定義（例: “Descriptive mentions of the token ‘MUST NOT’ … are non-normative.”）にし、規範的 `MUST NOT` を含めない。

#### 変更B: `explanatory-must-not-for-clarity` は維持（要整合確認）

- `statement` の主オペレータが `SHOULD` であり、`MUST NOT` は例示・列挙のため、Medium定義と整合する限り変更不要。

#### 変更C（任意）: `prohibitions.items` の配置順

- 新規禁止（A-1）を `prohibitions.items` の末尾に追加する。
- 重要度・参照頻度を考慮して順序を変える場合は、別プランとして扱う。

---

## 6. 検証計画（実装後）

### 6.1 機械的検証（最低限）

- YAML パース（frontmatter と fenced YAML ブロック双方）
- 構造検証（frontmatter + 単一 fenced YAML + それ以外は空白のみ）

### 6.2 規範検証（人手 + 将来 lint）

- `prohibitions.items` 以外の rule record に、規範オペレータ `MUST NOT` がないことを確認
- `one-obligation-per-rule`（複数モーダル混在）の検査
- Medium強度の「数える/数えない」規則に照らして、説明的用法が誤分類されないことを確認

---

## 7. 未解決事項（別タスク候補）

### 7.1 `prohibitions` セクションの位置（lost-in-the-middle 対策の最大化）

- 早期配置効果を最大化するなら `interpretation` 直後への移動が一貫する。
- ただし構造変更・差分肥大の懸念があるため、まずは meta-circular の回復（変更A）を優先し、位置移動は別タスクとする。

### 7.2 リポジトリ横断適用

- 本リポジトリの他スキルファイル（実体は `.agents/skills`）が増えた場合、同じ Medium強度（判定手続き込み）を適用するか、authoring スキルへの参照（id/link）に統一するかを決める。
