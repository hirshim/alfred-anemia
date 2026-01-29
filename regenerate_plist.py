import plistlib
import uuid

# Define UUIDs to ensure they match connections
UID_KEYWORD = "cb14ab1e-cdbc-4589-81e6-a9dd7bc317c5"
UID_SCRIPT_FILTER = "e9b408f1-86d3-4dfe-8898-f82f5d2fc143"
UID_EXTERNAL_TRIGGER = "89e9e3e0-75da-45e9-8635-cd45048de426"
UID_OUTPUT_TRIGGER = "8d5441fb-768d-4a8c-9687-a3925993ba77"

# Readme content
README_TEXT = """# 貧血鑑別診断ワークフロー (Alfred Workflow)

成田美和子先生の「貧血の分類と診断の進め方」 (日内会誌 104:1375-1382, 2015) に基づいた、貧血鑑別診断フローチャートをAlfredから手軽に利用できるワークフローです。
検査結果（MCV、網赤血球数、鉄関連検査など）を入力していくことで、疑われる疾患や次の検査項目を提示します。

## 機能
- **対話的診断**: 質問に答えていくだけで、適切な診断プロセスを辿れます。
- **診断結果の提示**: 最終的な鑑別疾患の候補を表示します。

## 使い方
1. Alfredを開き、キーワード `anemia` を入力。
2. 質問に回答して進めます。
"""

data = {
    "bundleid": "com.hirshim.alfred-anemia",
    "category": "Tools",
    "connections": {
        UID_KEYWORD: [
            {
                "destinationuid": UID_SCRIPT_FILTER,
                "modifiers": 0,
                "modifiersubtext": "",
                "vitoclose": False
            }
        ],
        UID_EXTERNAL_TRIGGER: [
            {
                "destinationuid": UID_SCRIPT_FILTER,
                "modifiers": 0,
                "modifiersubtext": "",
                "vitoclose": False
            }
        ],
        UID_SCRIPT_FILTER: [
            {
                "destinationuid": UID_OUTPUT_TRIGGER,
                "modifiers": 0,
                "modifiersubtext": "",
                "vitoclose": False
            }
        ]
    },
    "createdby": "hirshim",
    "description": "貧血鑑別診断フローチャートに基づいた診断支援ワークフロー",
    "disabled": False,
    "name": "Anemia Diagnosis",
    "objects": [
        {
            "config": {
                "argumenttype": 2,
                "keyword": "anemia",
                "subtext": "診断を開始します",
                "text": "貧血鑑別診断",
                "withspace": False
            },
            "type": "alfred.workflow.input.keyword",
            "uid": UID_KEYWORD,
            "version": 1
        },
        {
            "config": {
                "triggerid": "anemia_trigger"
            },
            "type": "alfred.workflow.trigger.external",
            "uid": UID_EXTERNAL_TRIGGER,
            "version": 1
        },
        {
            "config": {
                "alfredfiltersresults": False,
                "alfredfiltersresultsmatchmode": 0,
                "argumenttype": 1,
                "escaping": 102,
                "keyword": "",
                "queuedelaycustom": 3,
                "queuedelayimmediatelyinitially": True,
                "queuedelaymode": 0,
                "queuemode": 1,
                "runningsubtext": "考え中...",
                "script": '/usr/bin/python3 run_diagnosis.py "{query}"',
                "scriptargtype": 0,
                "scriptfile": "",
                "subtext": "選択肢を選んでください",
                "title": "貧血鑑別診断",
                "withspace": True
            },
            "type": "alfred.workflow.input.scriptfilter",
            "uid": UID_SCRIPT_FILTER,
            "version": 3
        },
        {
            "config": {
                "externaltriggerid": "anemia_trigger",
                "passinputasargument": True,
                "passvariables": True,
                "workflowbundleid": "self"
            },
            "type": "alfred.workflow.output.trigger",
            "uid": UID_OUTPUT_TRIGGER,
            "version": 1
        }
    ],
    "readme": README_TEXT,
    "uidata": {
        UID_KEYWORD: {"xpos": 50, "ypos": 50},
        UID_EXTERNAL_TRIGGER: {"xpos": 50, "ypos": 200},
        UID_SCRIPT_FILTER: {"xpos": 250, "ypos": 200},
        UID_OUTPUT_TRIGGER: {"xpos": 450, "ypos": 200},
    },
    "version": "1.0.0",
    "webaddress": "https://github.com/hirshim/alfred-anemia"
}

with open("info.plist", "wb") as f:
    plistlib.dump(data, f)

print("info.plist regenerated successfully.")
