# alfred-anemia

貧血鑑別スクリプト - 性別とヘモグロビン値から貧血の基準値を表示するPythonスクリプト

Python 3.13+ プロジェクト

## ドキュメント

- **[仕様書 (SPEC.md)](doc/SPEC.md)** - 機能仕様、要件定義
- **[設計ドキュメント (design_doc.md)](doc/design_doc.md)** - アーキテクチャ、設計方針
- **[使用方法 (instructions.md)](doc/instructions.md)** - 使い方、トラブルシューティング
- **[Markdownプレビュー方法](doc/MARKDOWN_PREVIEW.md)** - Markdownファイルのレンダリング方法

### Markdownファイルのプレビュー

Cursor/VS Code内でMarkdownファイルを開き、以下のショートカットでプレビューできます:

- **`Cmd+Shift+V`** (macOS) / **`Ctrl+Shift+V`** (Windows/Linux) - プレビューを開く
- **`Cmd+K V`** (macOS) / **`Ctrl+K V`** (Windows/Linux) - サイドバイサイド表示

詳細は [MARKDOWN_PREVIEW.md](doc/MARKDOWN_PREVIEW.md) を参照してください。

## クイックスタート

### 基本的な使用方法

```bash
# 仮想環境をアクティベート
source .venv/bin/activate

# 男性、Hb 14.0 g/dL の場合
python -m src.main m 14.0

# 女性、Hb 11.0 g/dL の場合
python -m src.main f 11.0

# JSON形式で出力
python -m src.main m 13.5 --output result.json
```

### コマンドラインオプション

```bash
# ヘルプを表示
python -m src.main --help

# バージョン情報を表示
python -m src.main --version

# 入力ファイルから読み込み
python -m src.main --input input.json

# 出力ファイルに保存
python -m src.main m 14.0 --output result.txt
```

## セットアップ

### 1. 仮想環境の作成とアクティベート

```bash
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
# または
.venv\Scripts\activate  # Windows
```

### 2. 開発用パッケージのインストール

```bash
pip install --upgrade pip setuptools wheel
pip install -e ".[dev]"
```

または個別にインストール:

```bash
pip install ruff mypy pytest pytest-cov
```

## 開発ツール

### コード品質チェック

```bash
# Ruff（リンター・フォーマッター）
ruff check .          # チェック
ruff format .         # フォーマット
ruff check --fix .    # 自動修正

# MyPy（型チェック）
mypy src/

# すべてのチェックを実行
ruff check . && ruff format --check . && mypy src/
```

### テスト実行

```bash
# すべてのテストを実行
pytest

# 詳細な出力で実行
pytest -v

# カバレッジ付きで実行
pytest --cov=src --cov-report=term-missing

# 特定のテストファイルを実行
pytest tests/test_main.py
```

## プロジェクト構造

```
alfred-anemia/
├── .venv/              # 仮想環境（.gitignoreに含まれています）
├── .vscode/            # VS Code/Cursor設定
│   └── settings.json
├── doc/                # ドキュメント
│   ├── SPEC.md         # 仕様書
│   ├── design_doc.md    # 設計ドキュメント
│   └── instructions.md  # 使用方法
├── src/                # ソースコード
│   └── main.py
├── tests/              # テストコード
│   ├── __init__.py
│   └── test_main.py
├── pyproject.toml      # プロジェクト設定
└── README.md
```

## 開発環境

このプロジェクトは以下のツールで最適化されています:

- **Ruff**: 高速なPythonリンター・フォーマッター
- **MyPy**: 静的型チェッカー
- **Pytest**: テストフレームワーク
- **pytest-cov**: コードカバレッジ測定

### Cursor拡張機能

以下の拡張機能が推奨されています:

- `ms-python.python` - Python言語サポート
- `charliermarsh.ruff` - Ruff統合
- `ms-python.mypy-type-checker` - MyPy統合
- `ms-python.debugpy` - デバッガー
- `anysphere.cursorpyright` - 型推論

## ライセンス

（ライセンス情報を追加してください）

