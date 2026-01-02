# 使用方法 (Instructions)

## クイックスタート

### 基本的な使用方法

```bash
# 仮想環境をアクティベート
source .venv/bin/activate

# スクリプトを実行
python -m src.main
```

## 詳細な使用方法

### コマンドラインオプション

```bash
# ヘルプを表示
python -m src.main --help

# バージョン情報を表示
python -m src.main --version

# 入力ファイルを指定
python -m src.main --input data.txt

# 出力ファイルを指定
python -m src.main --input data.txt --output result.txt
```

### 設定ファイルの使用

```bash
# 設定ファイルを指定
python -m src.main --config config.json
```

### 環境変数の使用

```bash
# 環境変数を設定
export ALFRED_ANEMIA_CONFIG_PATH=/path/to/config.json
python -m src.main
```

## 使用例

### 例1: 基本的な実行

```bash
python -m src.main
```

### 例2: ファイル処理

```bash
python -m src.main --input input.txt --output output.txt
```

### 例3: バッチ処理

```bash
for file in *.txt; do
    python -m src.main --input "$file" --output "processed_$file"
done
```

## トラブルシューティング

### よくある問題

#### 問題1: モジュールが見つからない

**解決方法**:
```bash
# 仮想環境がアクティベートされているか確認
which python  # .venv/bin/python を指しているか確認

# プロジェクトルートから実行
cd /path/to/alfred-anemia
python -m src.main
```

#### 問題2: パーミッションエラー

**解決方法**:
```bash
# 実行権限を確認
chmod +x src/main.py  # 必要に応じて
```

#### 問題3: 依存関係エラー

**解決方法**:
```bash
# 依存関係を再インストール
pip install -e ".[dev]"
```

## 高度な使用方法

### デバッグモード

```bash
# デバッグログを有効化
python -m src.main --debug
```

### 詳細ログ

```bash
# 詳細なログ出力
python -m src.main --verbose
```

## 統合

### CI/CDでの使用

```yaml
# GitHub Actions の例
- name: Run script
  run: |
    source .venv/bin/activate
    python -m src.main --input data.txt
```

### 他のスクリプトからの呼び出し

```python
from src.main import main

if __name__ == "__main__":
    main()
```

