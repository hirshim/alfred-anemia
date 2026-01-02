#!/bin/bash
# 使用例スクリプト

echo "=== 貧血鑑別スクリプトの使用例 ==="
echo ""

echo "1. 男性、Hb 14.0 g/dL:"
python -m src.main m 14.0
echo ""

echo "2. 女性、Hb 11.0 g/dL:"
python -m src.main f 11.0
echo ""

echo "3. 無効な性別:"
python -m src.main x 14.0
echo ""

echo "4. JSON形式で出力:"
python -m src.main m 13.5 --output /tmp/anemia_result.json
cat /tmp/anemia_result.json
echo ""

echo "5. ヘルプを表示:"
python -m src.main --help
echo ""

echo "6. バージョン情報:"
python -m src.main --version

