# Markdownファイルのレンダリング方法

## Cursor/VS Code内でのプレビュー

### 方法1: 組み込みプレビュー（推奨）

1. **Markdownファイルを開く**（例: `doc/SPEC.md`）
2. **プレビューを開く**:
   - キーボードショートカット: `Cmd+Shift+V` (macOS) / `Ctrl+Shift+V` (Windows/Linux)
   - または、右上のプレビューアイコンをクリック
   - または、コマンドパレット（`Cmd+Shift+P`）で「Markdown: Open Preview」

3. **サイドバイサイド表示**:
   - `Cmd+K V` (macOS) / `Ctrl+K V` (Windows/Linux) で横並び表示

### 方法2: Markdown All in One拡張機能

インストール済みの `yzhang.markdown-all-in-one` を使用:

- **ショートカット**:
  - `Cmd+Shift+V`: プレビュー
  - `Cmd+K V`: サイドバイサイド
  - `Cmd+Shift+S`: ドキュメントをHTMLとして保存

- **機能**:
  - 目次の自動生成
  - 数式のレンダリング
  - テーブルのフォーマット

### 方法3: Markdown Preview Enhanced

インストール済みの `shd101wyy.markdown-preview-enhanced` を使用:

- **コマンドパレット**（`Cmd+Shift+P`）から:
  - 「Markdown Preview Enhanced: Open Preview to the Side」
  - 「Markdown Preview Enhanced: Open Preview」

- **機能**:
  - 数式（MathJax/KaTeX）
  - コード実行
  - プレゼンテーション機能

## コマンドラインでのレンダリング

### 方法1: Python + markdownライブラリ

```bash
# markdownライブラリをインストール
pip install markdown

# HTMLに変換
python -c "import markdown; print(markdown.markdown(open('doc/SPEC.md').read()))" > spec.html

# ブラウザで開く
open spec.html  # macOS
# xdg-open spec.html  # Linux
# start spec.html  # Windows
```

### 方法2: pandoc（推奨）

```bash
# pandocをインストール（Homebrew）
brew install pandoc

# HTMLに変換
pandoc doc/SPEC.md -o doc/SPEC.html --standalone --css=github-markdown.css

# PDFに変換
pandoc doc/SPEC.md -o doc/SPEC.pdf

# ブラウザで開く
open doc/SPEC.html
```

### 方法3: grip（GitHubスタイル）

```bash
# gripをインストール
pip install grip

# ローカルサーバーで表示（GitHubスタイル）
grip doc/SPEC.md

# ブラウザで http://localhost:6419 を開く
```

### 方法4: mdv（ターミナル内で表示）

```bash
# mdvをインストール
pip install mdv

# ターミナルで表示（色付き）
mdv doc/SPEC.md
```

## ブラウザでの表示

### 方法1: 直接開く（基本）

```bash
# HTMLに変換してから開く
pandoc doc/SPEC.md -o doc/SPEC.html --standalone
open doc/SPEC.html
```

### 方法2: GitHub/GitLabで表示

1. リポジトリにプッシュ
2. GitHub/GitLab上でMarkdownファイルを開く
3. 自動的にレンダリングされる

### 方法3: VS Code Live Server

```bash
# Live Server拡張機能をインストール（未インストールの場合）
# その後、HTMLファイルを右クリック → "Open with Live Server"
```

## 便利なスクリプト

### プレビュー用スクリプト

`scripts/preview_md.sh` を作成:

```bash
#!/bin/bash
# MarkdownファイルをHTMLに変換してブラウザで開く

if [ -z "$1" ]; then
    echo "使用方法: ./scripts/preview_md.sh <markdown-file>"
    exit 1
fi

MD_FILE="$1"
HTML_FILE="${MD_FILE%.md}.html"

# pandocで変換
pandoc "$MD_FILE" -o "$HTML_FILE" --standalone --css=github-markdown.css

# ブラウザで開く
open "$HTML_FILE"  # macOS
# xdg-open "$HTML_FILE"  # Linux
```

## 推奨ワークフロー

### 開発中
1. Cursor内で `Cmd+Shift+V` でプレビュー
2. サイドバイサイド表示（`Cmd+K V`）で編集しながら確認

### 共有・配布
1. `pandoc` でHTML/PDFに変換
2. またはGitHubにプッシュして表示

### プレゼンテーション
1. `Markdown Preview Enhanced` のプレゼンテーションモードを使用
2. または `reveal.js` と組み合わせ

## トラブルシューティング

### プレビューが表示されない
- Markdown拡張機能が有効か確認
- ファイルが `.md` 拡張子か確認
- Cursorを再起動

### 日本語が正しく表示されない
- ファイルのエンコーディングがUTF-8か確認
- フォント設定を確認

### 数式が表示されない
- `Markdown Preview Enhanced` を使用
- MathJax/KaTeXの設定を確認

