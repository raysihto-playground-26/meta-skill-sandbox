# Gap Analysis: P1 (Conflict Resolution Ambiguity) and P2 (Condition Identifier Vocabulary)

Target file: `.agents/skills/meta-skill.ai-directive-files-authoring/SKILL.md`

## Background

PR #10 に対するレビューにおいて、仕様の内部整合性に関する複数の指摘が行われた。
本レポートでは、そのうち重要度の高い 2 件の root cause について、現状 (As-Is)、
あるべき姿 (To-Be)、および両者のギャップ (Gap) を整理する。

## P1: Conflict Resolution Ambiguity — 仕様の根幹メカニズムが不定

### As-Is (現状)

`interpretation.priority` と `precedence_and_conflict.conflict_policy.MUST_vs_MUST` が
論理的に矛盾しており、同一 layer 内で priority が異なる 2 つの MUST ルールが衝突した場合の
挙動が不定である。

**箇所 1** — `interpretation.priority` (L24):

```yaml
priority: "Each rule has layer (L0–L4) and priority (numeric); L0 has highest
  precedence, and within the same layer, higher priority number wins. See
  precedence_and_conflict for details."
```

この記述は「同一 layer 内では数値 priority が高い方が勝つ」と明言している。

**箇所 2** — `precedence_and_conflict.conflict_policy.MUST_vs_MUST` (L30):

```yaml
MUST_vs_MUST: "Halt or request clarification; MUST NOT silently choose one."
```

この記述は MUST 同士の衝突に対して無条件に halt を要求している。

**矛盾の具体例**:

同一 layer (L2) 内でルール A (priority: 98) とルール B (priority: 95) が衝突した場合:

- `interpretation.priority` に従えば → ルール A が勝つ (priority 98 > 95)
- `MUST_vs_MUST` に従えば → halt または clarification を要求

runner はどちらの指示に従うべきか判断できない。

### レビューコメントからの引用

> `interpretation.priority` says conflicts are resolved by layer and numeric priority
> (higher priority wins within a layer), but `precedence_and_conflict.conflict_policy.MUST_vs_MUST`
> says to halt/request clarification for MUST-vs-MUST. As written, this is internally inconsistent
> for two MUST rules with different priorities in the same layer. Consider specifying that halting
> only applies when layer+priority are equal (or otherwise define exactly when priority resolves
> vs when to halt).
>
> — Copilot review on `.agents/skills/meta-skill.ai-directive-files-authoring/SKILL.md` L30

### To-Be (あるべき姿)

priority 解決と conflict policy の適用条件が明確に分離され、runner が決定論的に
衝突を解決できる状態。具体的には:

1. **layer が異なる場合**: layer の precedence order で解決 (L0 > L1 > ... > L4)
2. **layer が同一で priority が異なる場合**: 数値 priority で解決 (高い方が勝つ)
3. **layer も priority も同一の場合**: conflict policy を適用 (MUST vs MUST → halt)

### Gap

| 観点                               | As-Is                                    | To-Be                                            |
| ---------------------------------- | ---------------------------------------- | ------------------------------------------------ |
| `MUST_vs_MUST` の適用条件          | 無条件 ("Halt or request clarification") | layer と priority で解決不能な場合のみ           |
| `interpretation.priority` との関係 | 言及なし (矛盾が放置)                    | priority が conflict policy に優先することを明示 |
| runner の挙動                      | 不定 (2 つの指示が矛盾)                  | 決定論的に解決可能                               |

## P2: Condition Identifier Vocabulary — 仕様の自己違反 (MUST 要件)

### As-Is (現状)

`interpretation.compound_conditions` が condition 識別子の定義を MUST で要求しているが、
ファイル自身がその要求を満たしていない。問題は 2 つの層に分かれる。

#### 問題 A: 未定義の識別子

`compound_conditions` (L22):

```yaml
compound_conditions: "A condition entry may be a single trigger identifier or a
  compound of the form 'A and B' (literal space, and, space), meaning both A and B
  apply; such identifiers MUST be defined in this file or in definitions."
```

しかし、ファイル全体で広く使用されている以下の識別子は `definitions` に存在しない:

| 識別子                                                | 使用箇所 (例)                         | definitions に定義                                    |
| ----------------------------------------------------- | ------------------------------------- | ----------------------------------------------------- |
| `creating AI directive file`                          | 大多数のルールの conditions           | **なし**                                              |
| `editing AI directive file`                           | 大多数のルールの conditions           | **なし**                                              |
| `scope high-stakes`                                   | tier-separation ルール群の conditions | **なし** (注: `scope-high-stakes` は定義あり)         |
| `scope multi-constraint`                              | tier-separation ルール群の conditions | **なし** (注: `scope-multi-constraint` は定義あり)    |
| `scope long-form reasoning`                           | tier-separation ルール群の conditions | **なし** (注: `scope-long-form-reasoning` は定義あり) |
| `creating AI directive file that contains YAML block` | yaml-include-\* ルール群の conditions | **なし**                                              |
| `editing AI directive file that contains YAML block`  | yaml-include-\* ルール群の conditions | **なし**                                              |

#### 問題 B: トークン形式の不一致

tier-separation ルール群の conditions で使われる識別子がスペース区切りであるのに対し、
`definitions` のキーはハイフン区切りになっている。YAML 文字列として異なる値であり、
機械的な照合が失敗する。

conditions での使用 (例: `tier-separation-when-applicable` L448):

```yaml
conditions: ["creating AI directive file and scope high-stakes", "editing AI directive file and scope high-stakes", ...]
```

definitions での定義 (L66-71):

```yaml
scope-high-stakes:
  description: "Context or output where errors have serious consequences ..."
scope-multi-constraint:
  description: "Context where many rules or constraints must be satisfied together."
scope-long-form-reasoning:
  description: "Context involving extended analysis, multi-step reasoning, ..."
```

`"scope high-stakes"` (スペース) ≠ `scope-high-stakes` (ハイフン)。

### レビューコメントからの引用

**識別子未定義について**:

> `interpretation.compound_conditions` requires compound identifiers like "A and B" to
> reference identifiers that are defined in this file, but later `conditions` entries use
> terms like "creating AI directive file" / "scope high-stakes" that are not defined under
> `definitions` (and `scope-high-stakes` uses a different tokenization). Add explicit
> trigger/condition identifiers under `definitions` (or a dedicated `triggers:` section) and
> use them consistently in `conditions`, or relax this requirement.
>
> — Copilot review on `.agents/skills/meta-skill.ai-directive-files-authoring/SKILL.md` L22

**トークン形式不一致について**:

> The `tier-separation-*` rules' `conditions` include compounds like
> "creating AI directive file and scope high-stakes", but the referenced tokens aren't
> defined consistently: `definitions` uses keys like `scope-high-stakes` while the condition
> uses "scope high-stakes". Given `interpretation.compound_conditions` requires identifiers
> to be defined, please standardize the identifier vocabulary (e.g., use exact defined
> identifiers, or define aliases) so these conditions can be validated and evaluated
> deterministically.
>
> — Copilot review on `.agents/skills/meta-skill.ai-directive-files-authoring/SKILL.md` L450

> The `compound_conditions` interpretation requires identifiers in compound conditions to be
> "defined in this file or in definitions." The tier-separation rules use space-separated
> identifiers (`scope high-stakes`, `scope multi-constraint`, `scope long-form reasoning`) in
> their `conditions` arrays, but the `definitions` section defines these with hyphens
> (`scope-high-stakes`, `scope-multi-constraint`, `scope-long-form-reasoning`). These are
> distinct YAML strings, so a runner or linter resolving compound condition parts against
> definitions would fail to find a match for all four tier-separation rules.
>
> — cursor[bot] (Bugbot) review on `.agents/skills/meta-skill.ai-directive-files-authoring/SKILL.md` L450

### To-Be (あるべき姿)

`compound_conditions` の MUST 要求が満たされ、全ての condition 識別子が
定義済み・照合可能な状態。具体的には:

1. ファイル内で conditions に使用される全識別子が `definitions` (またはそれに相当するセクション) に定義されている
2. conditions 内のトークンと definitions のキーが同一の正規形で一致する
3. runner/linter が conditions を definitions に対して機械的に検証できる

### Gap

| 観点                               | As-Is                                                    | To-Be                                                          |
| ---------------------------------- | -------------------------------------------------------- | -------------------------------------------------------------- |
| trigger 識別子の定義               | "creating/editing AI directive file" 等が未定義          | 全識別子が definitions (または triggers セクション) に定義済み |
| scope 識別子のトークン形式         | conditions: スペース区切り / definitions: ハイフン区切り | 統一された正規形                                               |
| `compound_conditions` の MUST 準拠 | **自己違反**                                             | 準拠                                                           |
| 機械的検証可能性                   | 照合不能                                                 | definitions に対する照合が可能                                 |

## Summary

| ID  | 問題                                        | 重要度   | As-Is                    | To-Be                    |
| --- | ------------------------------------------- | -------- | ------------------------ | ------------------------ |
| P1  | priority 解決と conflict policy の矛盾      | Critical | 衝突解決が不定           | 決定論的に解決可能       |
| P2  | condition 識別子の語彙不在 + トークン不一致 | High     | MUST 自己違反 + 照合不能 | 全識別子が定義・照合可能 |
