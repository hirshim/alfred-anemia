#!/bin/bash
# MarkdownファイルをHTMLに変換してブラウザで開く

if [ -z "$1" ]; then
    echo "使用方法: ./scripts/preview_md.sh <markdown-file>"
    echo "例: ./scripts/preview_md.sh doc/SPEC.md"
    exit 1
fi

MD_FILE="$1"

if [ ! -f "$MD_FILE" ]; then
    echo "エラー: ファイルが見つかりません: $MD_FILE"
    exit 1
fi

HTML_FILE="${MD_FILE%.md}.html"

# pandocがインストールされているか確認
if ! command -v pandoc &> /dev/null; then
    echo "エラー: pandocがインストールされていません"
    echo "インストール方法: brew install pandoc"
    exit 1
fi

# HTMLに変換
echo "変換中: $MD_FILE -> $HTML_FILE"
pandoc "$MD_FILE" -o "$HTML_FILE" --standalone --toc --css=https://cdn.jsdelivr.net/gh/sindresorhus/github-markdown-css@4/github-markdown.min.css

# ブラウザで開く
if [[ "$OSTYPE" == "darwin"* ]]; then
    open "$HTML_FILE"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    xdg-open "$HTML_FILE"
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    start "$HTML_FILE"
else
    echo "HTMLファイルが作成されました: $HTML_FILE"
fi

