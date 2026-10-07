import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).parents[1]


class ConfigTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = json.loads((ROOT / ".opencode/opencode.json").read_text(encoding="utf-8"))
        cls.model = cls.config["provider"]["argolink"]["models"]["gpt-6-sol"]

    def test_responses_provider_shape(self):
        provider = self.config["provider"]["argolink"]
        self.assertEqual(provider["npm"], "@ai-sdk/openai")
        self.assertEqual(provider["options"]["baseURL"], "https://argolink.io/v1")
        self.assertEqual(provider["options"]["apiKey"], "{env:OPENAI_API_KEY}")
        self.assertEqual(self.config["model"], "argolink/gpt-6-sol")

    def test_reasoning_limits_cost_and_variants(self):
        self.assertEqual(self.model["reasoning_options"][0]["values"], ["low", "medium", "high", "xhigh", "max"])
        self.assertEqual(self.model["limit"], {"context": 1050000, "output": 128000})
        self.assertEqual(self.model["cost"]["cache"], {"read": 0.06, "write": 0.75})
        self.assertEqual(set(self.model["variants"]), set(self.model["reasoning_options"][0]["values"]))

    def test_workflow_and_hygiene(self):
        plan = (ROOT / "examples/workflows.yaml").read_text(encoding="utf-8")
        self.assertIn("argolink/gpt-6-sol", plan)
        self.assertIn("write_requires_clean_branch: true", plan)
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertNotIn("sk-", text.lower())
        self.assertNotIn("api." + "argolink.io", text)
        self.assertNotIn("@ai-sdk/openai-compatible` targets", text[text.find("## Current"):text.find("## Setup")])


if __name__ == "__main__":
    unittest.main()
