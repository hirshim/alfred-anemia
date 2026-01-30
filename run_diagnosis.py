#!/usr/bin/env python3
"""
Alfredワークフローのエントリーポイント。
引数として検査値（スペース区切り）を受け取り、
診断フローに基づいた結果をJSON形式で出力します。
"""
import sys
from anemia_flow import main

if __name__ == "__main__":
    main()
