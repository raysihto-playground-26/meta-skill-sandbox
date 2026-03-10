# リポジトリサマリー

> **プロンプト（原文）:** このリポジトリーの summary を一時ファイルとして作成してください。

---

## リポジトリ概要

**リポジトリ名:** `raysihto-playground-26/meta-skill-sandbox`

AI エージェント向けディレクティブファイル（スキル）の開発・実験を行うサンドボックスリポジトリです。
複数の AI エージェントが共通のスキル定義を参照しながら一貫した振る舞いを実現する仕組みを探求しています。

---

## ディレクトリ構成

| パス                                             | 役割                                                  |
| ------------------------------------------------ | ----------------------------------------------------- |
| `.agents/docs/`                                  | AI ディレクティブファイルに関するポリシー文書（正典） |
| `.agents/skills/`                                | AI エージェント共通スキル定義                         |
| `.agent/skills/`                                 | 汎用エージェント向けスキル定義                        |
| `.github/skills/`                                | GitHub Copilot 向けスキル定義                         |
| `.github/workflows/`                             | GitHub Actions CI ワークフロー                        |
| `.claude/`、`.cursor/`、`.gemini/`、`.opencode/` | 各 AI ツール固有の設定ディレクトリ                    |
| `docs/.tmp/`                                     | 一時ファイルの格納場所（tmp-file-rules に基づく）     |

---

## 主要スキル

### `skill-alchemy`

AI ディレクティブファイルの **形式・オーサリングプロトコル**を規定するメタスキルです。

- **適用対象:** `.*/skills/*/*.md` に該当するすべての AI ディレクティブファイル
- **核心ルール:**
  - ファイルは「YAML フロントマター ＋ 単一 YAML コードブロック」の構造のみ許可（散文不可）
  - `interpretation` セクションで閉世界仮定・優先度・競合ポリシーを宣言する
  - すべてのルールに数値 `priority` を付与（`priority_direction: higher_wins`）
  - 無条件ルールは `conditions` フィールドを省略する（`conditions: always` 禁止）

### `tmp-file-rules`

一時ファイルの **命名規則・保存場所**を規定するスキルです。

- **適用対象:** `docs/.tmp/**/*`
- **核心ルール:**
  - パス形式: `docs/.tmp/YYYYMM/YYYYMMDDhhmmJST-<kebab-case-summary>.ext`（JST 基準）
  - 元のプロンプトをファイル先頭に記録する
  - 言語指定がない場合はプロンプトと同言語で記述する

---

## ポリシードキュメント

`.agents/docs/ai-directive-files-policy.md` が **AI ディレクティブファイルに関する正典ポリシー**です。
主な設計思想：

- **制約密度優先:** コンテキストを肥大化させず、高インパクトな制約を確実に伝達する
- **LLM は候補生成器:** 完全なコンプライアンスではなく、構造・優先度・外部検証で信頼性を確保する
- **Class 1 ハード制約を最優先:** 省略すると予測可能な失敗を引き起こす制約は絶対に保持する

補助リファレンス（`docs/ai-directive-files-policy.d/` 配下）：

- `ai-directive-files-best-practices.md`
- `deterministic-yaml-instruction-design.md`
- `llm-instruction-robustness-workaround-audit-manual.md`
- `llm-meta-control-instability.md`
- `tier-separation-iterative-processing.md`

---

## 技術スタック

| 項目                 | 内容                                   |
| -------------------- | -------------------------------------- |
| パッケージマネージャ | pnpm 10.x                              |
| Node.js バージョン   | 24.x                                   |
| フォーマッター       | Prettier（`printWidth: 120`）          |
| CI                   | GitHub Actions（フォーマットチェック） |
| 依存関係自動更新     | Dependabot（weekly、npm + Actions）    |

### 主要スクリプト

```bash
pnpm run check:format   # フォーマットチェック
pnpm run fix:format     # フォーマット自動修正
pnpm run all            # 修正 → チェック一括実行
```

---

## CI ワークフロー

`.github/workflows/integration-readiness.yml` — PR および手動実行時に起動。

1. リポジトリチェックアウト
2. pnpm セットアップ（corepack 経由）
3. 依存関係インストール（`--frozen-lockfile`）
4. Prettier フォーマットチェック
