import unittest
import json
import sys
import os

# Add parent directory to path to import anemia_flow
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from anemia_flow import AnemiaWorkflow, FLOWCHART

class TestAnemiaWorkflow(unittest.TestCase):
    def setUp(self):
        self.wf = AnemiaWorkflow()

    def test_root_node_resolution(self):
        """Test that 'root' resolves to the start node 'A'"""
        node = self.wf.get_node("root")
        self.assertIsNotNone(node)
        self.assertEqual(node["type"], "question")
        self.assertIn("貧血", node["text"])

    def test_node_retrieval(self):
        """Test retrieving a specific node"""
        node = self.wf.get_node("C")
        self.assertIsNotNone(node)
        self.assertEqual(node["type"], "result")
        self.assertIn("再生不良性貧血", node["diagnosis"])

    def test_json_output_root(self):
        """Test JSON output for root node"""
        output = self.wf.generate_json_output("root")
        data = json.loads(output)
        self.assertIn("items", data)
        self.assertFalse(data["items"][0]["valid"])
        self.assertTrue(any(item.get("arg") == "C" for item in data["items"]))
        self.assertTrue(any(item.get("arg") == "D" for item in data["items"]))

    def test_json_output_result(self):
        """Test JSON output for a result node"""
        output = self.wf.generate_json_output("C")
        data = json.loads(output)
        self.assertIn("items", data)
        diag_item = next((i for i in data["items"] if i["title"] == "鑑別診断結果:"), None)
        self.assertIsNotNone(diag_item)
        self.assertIn("再生不良性貧血", diag_item["subtitle"])

    def test_invalid_node_returns_error(self):
        """Test that invalid node ID handles gracefully"""
        output = self.wf.generate_json_output("INVALID_ID")
        data = json.loads(output)
        self.assertEqual(data["items"][0]["title"], "Error")


class TestAllNodesReachable(unittest.TestCase):
    """全ノードが有効なJSON出力を生成できることを検証"""

    def setUp(self):
        self.wf = AnemiaWorkflow()

    def test_all_nodes_produce_valid_json(self):
        """全ノードIDが有効なAlfred JSONを返す"""
        for node_id, node_data in FLOWCHART.items():
            if isinstance(node_data, str):
                continue  # alias (e.g. "root")
            with self.subTest(node_id=node_id):
                output = self.wf.generate_json_output(node_id)
                data = json.loads(output)
                self.assertIn("items", data)
                self.assertGreater(len(data["items"]), 0)

    def test_all_question_options_point_to_existing_nodes(self):
        """全questionノードの選択肢が存在するノードを指していることを検証"""
        for node_id, node_data in FLOWCHART.items():
            if isinstance(node_data, str):
                continue
            if node_data["type"] == "question":
                for option in node_data["options"]:
                    with self.subTest(node_id=node_id, option=option["label"]):
                        target = option["next"]
                        self.assertIn(target, FLOWCHART,
                            f"Node '{node_id}' option '{option['label']}' points to non-existent node '{target}'")

    def test_no_duplicate_option_targets(self):
        """同じquestionノード内で全選択肢が異なる遷移先を持つ"""
        for node_id, node_data in FLOWCHART.items():
            if isinstance(node_data, str):
                continue
            if node_data["type"] == "question":
                with self.subTest(node_id=node_id):
                    targets = [opt["next"] for opt in node_data["options"]]
                    self.assertEqual(len(targets), len(set(targets)),
                        f"Node '{node_id}' has duplicate option targets: {targets}")

    def test_all_result_nodes_have_diagnosis(self):
        """全resultノードがdiagnosisリストを持つ"""
        for node_id, node_data in FLOWCHART.items():
            if isinstance(node_data, str):
                continue
            if node_data["type"] == "result":
                with self.subTest(node_id=node_id):
                    self.assertIn("diagnosis", node_data)
                    self.assertGreater(len(node_data["diagnosis"]), 0)


class TestPathTraversal(unittest.TestCase):
    """主要な診断パスの走破テスト"""

    def setUp(self):
        self.wf = AnemiaWorkflow()

    def _follow_path(self, choices):
        """選択肢のインデックスリストに従ってパスを辿り、最終ノードを返す"""
        node_id = "root"
        for choice_idx in choices:
            node = self.wf.get_node(node_id)
            self.assertIsNotNone(node, f"Node '{node_id}' not found")
            self.assertEqual(node["type"], "question", f"Expected question at '{node_id}'")
            node_id = node["options"][choice_idx]["next"]
        return node_id, self.wf.get_node(node_id)

    def test_path_pancytopenia(self):
        """root→C: 白血球/血小板減少あり → 骨髄検査が必要"""
        node_id, node = self._follow_path([0])  # あり
        self.assertEqual(node["type"], "result")
        self.assertIn("再生不良性貧血", node["diagnosis"])

    def test_path_hemolysis(self):
        """root→D→E→F: 網赤血球増加→溶血所見あり"""
        node_id, node = self._follow_path([1, 0, 0])  # なし→あり→あり
        self.assertEqual(node["type"], "result")
        self.assertEqual(node_id, "F")

    def test_path_iron_deficiency(self):
        """root→D→H→K→S5→S6: 小球性→鉄欠乏性貧血"""
        node_id, node = self._follow_path([1, 1, 2, 1, 0])  # なし→なし→MCV≦80→低下正常→Fe↓
        self.assertEqual(node["type"], "result")
        self.assertIn("鉄欠乏性貧血 (IDA)", node["diagnosis"])

    def test_path_vitb12_deficiency(self):
        """root→D→H→I→L4→L5→L8: 大球性→VitB12欠乏"""
        node_id, node = self._follow_path([1, 1, 0, 1, 0, 0])
        self.assertEqual(node["type"], "result")
        self.assertIn("悪性貧血", node["diagnosis"])

    def test_path_renal_anemia(self):
        """root→D→H→J→N9→N10→N11: 正球性→EPO低値→腎性貧血"""
        node_id, node = self._follow_path([1, 1, 1, 1, 1, 0])
        self.assertEqual(node["type"], "result")
        self.assertIn("腎性貧血", node["diagnosis"])

    def test_path_s7_no_inflammation(self):
        """S7「なし」が独自の結果ノードに遷移する"""
        node_id, node = self._follow_path([1, 1, 2, 1, 1, 1])
        self.assertEqual(node_id, "S7_OTHER")
        self.assertEqual(node["type"], "result")


class TestEdgeCases(unittest.TestCase):
    """エッジケースのテスト"""

    def setUp(self):
        self.wf = AnemiaWorkflow()

    def test_get_node_returns_none_for_missing(self):
        node = self.wf.get_node("NONEXISTENT")
        self.assertIsNone(node)

    def test_get_node_handles_circular_alias(self):
        """循環エイリアスで無限ループしないことを検証"""
        original = self.wf.flowchart.copy()
        self.wf.flowchart["loop_a"] = "loop_b"
        self.wf.flowchart["loop_b"] = "loop_a"
        try:
            node = self.wf.get_node("loop_a")
            self.assertIsNone(node)
        finally:
            self.wf.flowchart = original

    def test_note_field_in_output(self):
        """noteフィールドが備考として出力される"""
        output = self.wf.generate_json_output("L8")
        data = json.loads(output)
        note_item = next((i for i in data["items"] if i["title"] == "備考"), None)
        self.assertIsNotNone(note_item)
        self.assertIn("抗内因子抗体", note_item["subtitle"])

    def test_result_has_restart_option(self):
        """resultノードに「最初に戻る」オプションがある"""
        output = self.wf.generate_json_output("C")
        data = json.loads(output)
        restart = next((i for i in data["items"] if i.get("arg") == "root"), None)
        self.assertIsNotNone(restart)
        self.assertEqual(restart["title"], "最初に戻る")

    def test_json_output_contains_japanese(self):
        """JSON出力に日本語が正しく含まれる（ensure_ascii=False）"""
        output = self.wf.generate_json_output("root")
        self.assertIn("貧血", output)
        self.assertNotIn("\\u", output)


if __name__ == '__main__':
    unittest.main()
