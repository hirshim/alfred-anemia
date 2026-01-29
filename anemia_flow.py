import json
import sys

# Define the flowchart data structure
FLOWCHART = {
    # start
    "root": "A",
    
    # Nodes
    "A": {
        "text": "貧血の鑑別診断を開始します。\nまずは白血球・血小板の減少はありますか？",
        "type": "question",
        "options": [
            {"label": "あり（白血球/血小板減少）", "next": "C"},
            {"label": "なし", "next": "D"}
        ]
    },
    
    # Branch: Pancytopenia (C)
    "C": {
        "text": "骨髄検査が必要な疾患の可能性があります。\n以下の疾患が疑われます。",
        "type": "result",
        "diagnosis": [
            "再生不良性貧血",
            "骨髄異形成症候群",
            "骨髄線維症",
            "巨赤芽球性貧血",
            "白血病",
            "肝疾患・脾機能亢進症"
        ]
    },

    # Branch: No Pancytopenia (D) -> Reticulocytes
    "D": {
        "text": "網赤血球絶対数の増加はありますか？",
        "type": "question",
        "options": [
            {"label": "あり（増加）", "next": "E"},
            {"label": "なし", "next": "H"}
        ]
    },
    
    # Branch: Reticulocytes High (E) -> Hemolysis
    "E": {
        "text": "溶血所見（間接ビリルビン↑, LDH↑, ハプトグロビン↓, ヘモジデリン尿）はありますか？",
        "type": "question",
        "options": [
            {"label": "あり", "next": "F"},
            {"label": "なし", "next": "G"}
        ]
    },
    "F": {
        "text": "溶血の原因の検索を行ってください。",
        "type": "result",
        "diagnosis": ["溶血性貧血疑い"]
    },
    "G": {
        "text": "出血源の検索を行ってください。",
        "type": "result",
        "diagnosis": ["出血性貧血疑い"]
    },

    # Branch: Reticulocytes Normal/Low (H) -> MCV
    "H": {
        "text": "MCV（平均赤血球容積）の値は？",
        "type": "question",
        "options": [
            {"label": "MCV ≧ 101 (大球性)", "next": "I"},
            {"label": "MCV 81-100 (正球性)", "next": "J"},
            {"label": "MCV ≦ 80 (小球性)", "next": "K"}
        ]
    },

    # --- Macrocytic (I) ---
    "I": {
        "text": "大球性貧血 (MCV ≧ 101) です。\n網赤血球の増加はありますか？",
        "type": "question",
        "options": [
            {"label": "あり", "next": "L2"},
            {"label": "なし", "next": "L4"}
        ]
    },
    "L2": {
        "text": "溶血あるいは出血が疑われます。\n詳しい検査を行ってください。",
        "type": "result",
        "diagnosis": ["溶血性貧血", "出血性貧血"]
    },
    "L4": {
        "text": "VitB12 あるいは葉酸の低下はありますか？",
        "type": "question",
        "options": [
            {"label": "あり", "next": "L5"},
            {"label": "なし", "next": "L11"}
        ]
    },
    "L5": {
        "text": "巨赤芽球性貧血が疑われます。\n可能であれば骨髄における巨赤芽球増加を確認してください。\n欠乏しているのはどちらですか？",
        "type": "question",
        "options": [
            {"label": "VitB12欠乏", "next": "L8"},
            {"label": "葉酸欠乏", "next": "L10"}
        ]
    },
    "L8": {
        "text": "VitB12欠乏による以下の疾患が疑われます。",
        "type": "result",
        "diagnosis": [
            "悪性貧血", "胃切除後貧血", "回腸疾患", "吸収不良症候群", "腸内細菌叢異常"
        ],
        "note": "抗内因子抗体、抗胃壁抗体、胃内視鏡などの検査を検討してください。"
    },
    "L10": {
        "text": "葉酸欠乏による以下の原因が疑われます。",
        "type": "result",
        "diagnosis": [
            "偏食", "薬剤起因性", "妊娠による葉酸需要増大"
        ]
    },
    "L11": {
        "text": "非巨赤芽球性貧血です。\n以下の疾患は否定できますか？\n（アルコール中毒、肝疾患、甲状腺機能低下症、薬剤、赤芽球癆）",
        "type": "question",
        "options": [
            {"label": "否定できない（疑いあり）", "next": "L13"},
            {"label": "すべて否定できる", "next": "L14"}
        ]
    },
    "L13": {
        "text": "詳細な鑑別を行ってください。",
        "type": "result",
        "diagnosis": [
            "アルコール中毒", "肝疾患", "甲状腺機能低下症", "薬剤性貧血", "赤芽球癆"
        ]
    },
    "L14": {
        "text": "骨髄異形成症候群の疑いがあります。\n骨髄検査を検討してください。",
        "type": "result",
        "diagnosis": ["骨髄異形成症候群 (MDS)"]
    },

    # --- Normocytic (J) ---
    "J": {
        "text": "正球性貧血 (MCV 81-100) です。\n網赤血球数は？",
        "type": "question",
        "options": [
            {"label": "増加", "next": "N2"},
            {"label": "低下〜正常", "next": "N9"}
        ]
    },
    "N2": {
        "text": "以下の項目に該当しますか？\n・貧血や黄疸の家族歴・既往歴\n・赤血球形態異常や封入体の存在\n・間接ビリルビン増加, LDH増加",
        "type": "question",
        "options": [
            {"label": "該当項目あり", "next": "N3"},
            {"label": "該当項目なし", "next": "N8"}
        ]
    },
    "N3": {
        "text": "Coombs試験の結果は？",
        "type": "question",
        "options": [
            {"label": "陽性", "next": "N4"},
            {"label": "陰性", "next": "N5"}
        ]
    },
    "N4": {
        "text": "自己免疫性などの関与が疑われます。",
        "type": "result",
        "diagnosis": ["溶血性貧血", "自己免疫性溶血性貧血"]
    },
    "N5": {
        "text": "CD55, CD59陰性赤血球、Ham試験陽性、NAP低下などの所見はありますか？",
        "type": "question",
        "options": [
            {"label": "あり", "next": "N6"},
            {"label": "なし", "next": "N7"}
        ]
    },
    "N6": {
        "text": "PNHが疑われます。",
        "type": "result",
        "diagnosis": ["発作性夜間血色素尿症 (PNH)"]
    },
    "N7": {
        "text": "その他の溶血性貧血の可能性があります。",
        "type": "result",
        "diagnosis": ["その他の溶血性貧血"]
    },
    "N8": {
        "text": "出血による貧血が疑われます。",
        "type": "result",
        "diagnosis": ["出血性貧血"]
    },
    "N9": {
        "text": "汎血球減少はありますか？",
        "type": "question",
        "options": [
            {"label": "あり", "next": "N18"},
            {"label": "なし", "next": "N10"}
        ]
    },
    "N10": {
        "text": "血清鉄・エリスロポエチン(EPO)の状態は？",
        "type": "question",
        "options": [
            {"label": "EPO低値", "next": "N11"},
            {"label": "EPO正常〜高値 (フェリチンなど確認)", "next": "N12"},
            {"label": "その他 (生化学検査など)", "next": "N14"},
             {"label": "赤芽球癆疑い", "next": "N16"}
        ]
    },
    "N11": {
        "text": "腎性貧血が考えられます。",
        "type": "result",
        "diagnosis": ["腎性貧血"]
    },
    "N12": {
        "text": "フェリチン, TIBC, CRP, RDWなどを確認してください。",
        "type": "result",
        "diagnosis": ["慢性炎症に伴う貧血 (ACD)", "鉄欠乏状態の初期"]
    },
    "N14": {
        "text": "一般生化学検査、甲状腺ホルモン、脾腫の有無を確認してください。",
        "type": "result",
        "diagnosis": ["脾機能亢進症", "内分泌疾患", "悪性腫瘍"]
    },
    "N16": {
        "text": "赤芽球癆が疑われます。骨髄検査を検討してください。",
        "type": "result",
        "diagnosis": ["赤芽球癆"]
    },
    "N18": {
        "text": "汎血球減少があります。骨髄検査が必要です。",
        "type": "result",
        "diagnosis": [
            "再生不良性貧血",
            "骨髄線維症",
            "多発性骨髄腫",
            "骨髄異形成症候群",
            "白血病",
            "血球貪食症候群"
        ]
    },
    
    # --- Microcytic (K) ---
    "K": {
        "text": "小球性貧血 (MCV ≦ 80) です。\n網赤血球数は？",
        "type": "question",
        "options": [
            {"label": "増加", "next": "S2"},
            {"label": "低下〜正常", "next": "S5"}
        ]
    },
    "S2": {
        "text": "赤血球形態異常, 間接ビリルビン↑, LDH↑, ハプトグロビン↓ などの所見はありますか？",
        "type": "question",
        "options": [
            {"label": "あり", "next": "S3"},
            {"label": "なし", "next": "S5"} # Fallback or specific node? Flowchart implies checks. Assume if no hemolysis signs, check iron.
        ]
    },
    "S3": {
        "text": "サラセミアや異常ヘモグロビン症の疑いがあります。\nヘモグロビン分析を検討してください。",
        "type": "result",
        "diagnosis": ["サラセミア", "異常ヘモグロビン症"]
    },
    "S5": {
        "text": "血清鉄・TIBC・フェリチンの値を確認してください。",
        "type": "question",
        "options": [
            {"label": "Fe↓, TIBC↑, Ferritin↓", "next": "S6"},
            {"label": "Fe↓, TIBC正常-↓, Ferritin正常-↑", "next": "S7"},
            {"label": "Fe正常-↑, TIBC正常-↓, Ferritin正常-↑", "next": "S9"}
        ]
    },
    "S6": {
        "text": "鉄欠乏性貧血の所見です。",
        "type": "result",
        "diagnosis": ["鉄欠乏性貧血 (IDA)"]
    },
    "S7": {
        "text": "CRP増加など、炎症性疾患を疑わせる所見はありますか？",
        "type": "question",
        "options": [
            {"label": "あり", "next": "S8"},
            {"label": "なし (詳細精査へ)", "next": "S8"} # Simplified for now as flowchart merges here essentially
        ]
    },
    "S8": {
        "text": "慢性炎症に伴う貧血(ACD)などが考えられます。",
        "type": "result",
        "diagnosis": ["慢性炎症に伴う貧血 (ACD)"]
    },
    "S9": {
        "text": "TIBCの著明低下はありますか？",
        "type": "question",
        "options": [
            {"label": "TIBC著明低下あり", "next": "S10"},
            {"label": "なし (骨髄鉄染色へ)", "next": "S11"}
        ]
    },
    "S10": {
        "text": "無トランスフェリン血症が疑われます。",
        "type": "result",
        "diagnosis": ["無トランスフェリン血症"]
    },
    "S11": {
        "text": "骨髄鉄染色で環状鉄芽球の増加が見られますか？",
        "type": "question",
        "options": [
            {"label": "はい", "next": "S12"},
            {"label": "いいえ (その他)", "next": "S_OTHER"} # Added explicit end
        ]
    },
    "S12": {
        "text": "鉄芽球性貧血が考えられます。",
        "type": "result",
        "diagnosis": ["鉄芽球性貧血"]
    },
    "S_OTHER": {
        "text": "分類困難な小球性貧血です。専門医へのコンサルトを推奨します。",
        "type": "result",
        "diagnosis": ["詳細不明 (要精査)"]
    }
}

class AnemiaWorkflow:
    """
    貧血鑑別診断のロジックを管理するクラス。
    
    mermaidフローチャートの構造（定義されたJSONノード構造）および
    成田美和子「貧血の分類と診断の進め方」日内会誌 104:1375-1382, 2015
    に基づき、次の質問や診断結果を提示します。
    """
    def __init__(self):
        """
        ワークフロー初期化。
        FLOWCHART定数を読み込みます。
        """
        self.flowchart = FLOWCHART

    def get_node(self, node_id):
        """
        指定されたIDのノードを取得します。
        文字列によるエイリアス（リダイレクト）も解決します。
        
        Args:
            node_id (str): ノードID (例: "root", "A", "C")
            
        Returns:
            dict or None: ノード情報の辞書。存在しない場合はNone。
        """
        node = self.flowchart.get(node_id)
        # Handle alias/redirection (e.g., "root" -> "A")
        while isinstance(node, str):
            node = self.flowchart.get(node)
        return node

    def generate_json_output(self, node_id):
        """
        Alfred Script Filter用のJSON出力を生成します。
        
        Args:
            node_id (str): 現在のステップを示すノードID
            
        Returns:
            str: Alfredが解釈可能なJSON文字列
        """
        node = self.get_node(node_id)
        if not node:
            return json.dumps({"items": [{"title": "Error", "subtitle": "Node not found"}]})

        items = []
        
        # Display the question/text as the first item (unselectable/info)
        items.append({
            "title": node["text"].split("\n")[0],
            "subtitle": "\n".join(node["text"].split("\n")[1:]) if "\n" in node["text"] else "",
            "valid": False,
            "icon": {"path": "icon.png"} # Assuming icon exists or default
        })

        if node["type"] == "question":
            for option in node["options"]:
                items.append({
                    "title": option["label"],
                    "subtitle": "選択して次へ",
                    "arg": option["next"],
                    "valid": True,
                    "autocomplete": option["label"]
                })
        elif node["type"] == "result":
            diagnosis_list = ", ".join(node.get("diagnosis", []))
            items.append({
                "title": "鑑別診断結果:",
                "subtitle": diagnosis_list,
                "valid": False
            })
            if "note" in node:
                items.append({
                    "title": "備考",
                    "subtitle": node["note"],
                    "valid": False
                })
            # Option to restart
            items.append({
                "title": "最初に戻る",
                "arg": "root",
                "valid": True
            })

        return json.dumps({"items": items}, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    # Simple test execution
    wf = AnemiaWorkflow()
    print(wf.generate_json_output("root"))
