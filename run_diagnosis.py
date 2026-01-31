"""
Alfredワークフローのエントリーポイントとなるスクリプト。
引数として現在のノードIDを受け取り、次のステップ（質問または結果）をJSON形式で標準出力します。
"""
import json
import sys
from anemia_flow import AnemiaWorkflow

def main():
    node_id = "root"

    if len(sys.argv) > 1 and sys.argv[1].strip():
        node_id = sys.argv[1].strip()

    try:
        wf = AnemiaWorkflow()
        output = wf.generate_json_output(node_id)
        print(output)
    except Exception as e:
        error_output = json.dumps({
            "items": [{"title": "エラーが発生しました", "subtitle": str(e), "valid": False}]
        }, ensure_ascii=False)
        print(error_output)

if __name__ == "__main__":
    main()
