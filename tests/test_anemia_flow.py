import unittest
import json
import sys
import os

# Add parent directory to path to import anemia_flow
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from anemia_flow import AnemiaWorkflow

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
        # Check first item is the text
        self.assertFalse(data["items"][0]["valid"])
        # Check options exist
        self.assertTrue(any(item.get("arg") == "C" for item in data["items"]))
        self.assertTrue(any(item.get("arg") == "D" for item in data["items"]))

    def test_json_output_result(self):
        """Test JSON output for a result node"""
        output = self.wf.generate_json_output("C")
        data = json.loads(output)
        self.assertIn("items", data)
        # Check for diagnosis results
        diag_item = next((i for i in data["items"] if i["title"] == "鑑別診断結果:"), None)
        self.assertIsNotNone(diag_item)
        self.assertIn("再生不良性貧血", diag_item["subtitle"])

    def test_invalid_node_returns_error(self):
        """Test that invalid node ID handles gracefully"""
        output = self.wf.generate_json_output("INVALID_ID")
        data = json.loads(output)
        self.assertEqual(data["items"][0]["title"], "Error")

if __name__ == '__main__':
    unittest.main()
