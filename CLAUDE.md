# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## プロジェクト概要

貧血の鑑別診断を対話的に行うAlfred Workflow。成田美和子の分類（日内会誌 104:1375-1382, 2015）に基づく決定木フローチャート。Alfred で `anemia` と入力し、診断質問に答えて鑑別診断に到達する。

- **作者**: hirshim
- **Bundle ID**: `com.hirshim.alfred-anemia`

## コマンド

```bash
# テスト実行
python3 -m unittest discover tests

# 単一テスト実行
python3 -m unittest tests.test_anemia_flow.TestAnemiaFlow.test_root_node_resolution

# スクリプト直接実行（動作確認用）
python3 run_diagnosis.py           # ルートノード（デフォルト）
python3 run_diagnosis.py "C"       # 特定ノード指定

# .alfredworkflow パッケージビルド（CIではタグpush時に自動実行）
zip -r AnemiaDiagnosis.alfredworkflow . -x '.git/*' '.github/*' 'tests/*' '*.md' '.DS_Store'
```

外部依存なし — Python標準ライブラリ（`json`, `sys`）のみ使用。

## アーキテクチャ

**実行フロー**: Alfred キーワード (`anemia`) → Script Filter → `run_diagnosis.py "{query}"` → `AnemiaWorkflow.generate_json_output(node_id)` → Alfred JSON → ユーザーが選択肢を選択 → external trigger で次の node_id を渡す → 繰り返し。

- `anemia_flow.py`: コアロジック。`FLOWCHART` 辞書（30+ノード）と `AnemiaWorkflow` クラス。各ノードは `"question"`（選択肢付き、次ノードへの参照あり）または `"result"`（診断名リスト）。ノード "root" は "A" のエイリアス。
- `run_diagnosis.py`: Alfred から呼ばれるエントリーポイント。`sys.argv[1]` から node_id を取得し、デフォルトは "root"、Alfred互換JSONを出力。
- `info.plist`: Script Filter、キーワードトリガー、再帰ナビゲーション用 external trigger を含むAlfred Workflow設定。

## Alfred Script Filter 設定

**info.plist の重要設定**（参考: `~/git/alfred-diabetic-nephropathy/CLAUDE.md`）:

| キー | 値 | 説明 |
|------|-----|------|
| `scriptargtype` | `0` | argv モード — `{query}` は必ずダブルクォートで囲む |
| `argumenttype` | `1` | Argument Optional |
| `escaping` | `0` 推奨 | 高い値（例: 102）は引数渡しを妨げる可能性あり |
| Script | `/usr/bin/python3 run_diagnosis.py "{query}"` | `"{query}"` のダブルクォートは必須 |

ワークフロー更新時は、Alfred Preferences で既存ワークフローを削除してから再インストールすること（キャッシュが残る場合がある）。

## リリースプロセス

Git タグ push（`v*`）で `.github/workflows/release.yml` が実行され、`.alfredworkflow` zip をビルドし `softprops/action-gh-release@v1` で GitHub Release を作成。バージョン文字列は `info.plist` 内に記載。
