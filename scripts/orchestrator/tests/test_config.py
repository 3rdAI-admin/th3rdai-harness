import unittest

from orchestrator import config


class TestRealConfigs(unittest.TestCase):
    def test_agents(self):
        agents = config.load_agents()
        self.assertIn("researcher", agents)
        self.assertEqual(agents["planner"]["model_profile"], "planning")
        self.assertEqual(agents["reviewer"]["default_skill"], "skills/plan/plan-reviewer.md")

    def test_routing(self):
        routes = config.load_routing()
        self.assertIn("task_definition", routes)
        self.assertEqual(routes["task_definition"]["agents"], ["researcher", "planner"])
        self.assertEqual(routes["release"]["stage"], "stages/07-release")

    def test_models(self):
        models = config.load_models()
        self.assertIn("planning", models)
        self.assertEqual(models["planning"]["provider"], "claude")
        self.assertIsInstance(models["planning"]["temperature"], float)

    def test_tools(self):
        tools = config.load_tools()
        self.assertIn("tool_policies", tools)
        self.assertIn("read_only", tools["tool_policies"])
        self.assertEqual(tools["tool_policies"]["read_only"]["requires_approval"], [])
        self.assertIn("git commit", tools["tool_policies"]["command_safe"]["requires_approval"])
        self.assertIsInstance(tools["safety_rules"], list)

    def test_cross_refs_clean(self):
        self.assertEqual(config.cross_ref_problems(), [])


class TestScalarParsing(unittest.TestCase):
    def test_scalar_types(self):
        self.assertIsNone(config.load_yaml_string("k: null")["k"])
        self.assertEqual(config.load_yaml_string("k: 3")["k"], 3)
        self.assertEqual(config.load_yaml_string("k: 0.5")["k"], 0.5)
        self.assertIs(config.load_yaml_string("k: true")["k"], True)
        self.assertIs(config.load_yaml_string("k: false")["k"], False)
        self.assertEqual(config.load_yaml_string("k: []")["k"], [])
        self.assertEqual(config.load_yaml_string("k: 'a: b'")["k"], "a: b")

    def test_string_with_dashes_not_number(self):
        self.assertEqual(config.load_yaml_string("k: 20260528-103000")["k"], "20260528-103000")

    def test_inline_comment_stripped(self):
        self.assertEqual(config.load_yaml_string("k: value  # note")["k"], "value")


class TestStructures(unittest.TestCase):
    def test_nested_mappings(self):
        self.assertEqual(
            config.load_yaml_string("a:\n  b:\n    c: 1\n"),
            {"a": {"b": {"c": 1}}},
        )

    def test_list_of_scalars(self):
        self.assertEqual(
            config.load_yaml_string("xs:\n  - one\n  - two\n")["xs"],
            ["one", "two"],
        )

    def test_list_of_mappings(self):
        text = (
            "issues:\n"
            "  - severity: high\n"
            "    description: boom\n"
            "  - severity: low\n"
            "    description: meh\n"
        )
        doc = config.load_yaml_string(text)
        self.assertEqual(len(doc["issues"]), 2)
        self.assertEqual(doc["issues"][0], {"severity": "high", "description": "boom"})
        self.assertEqual(doc["issues"][1], {"severity": "low", "description": "meh"})


class TestRejectsUnsupported(unittest.TestCase):
    def test_rejects_tab_indent(self):
        with self.assertRaises(config.YAMLSubsetError):
            config.load_yaml_string("a:\n\tb: 1\n")

    def test_rejects_block_scalar(self):
        with self.assertRaises(config.YAMLSubsetError):
            config.load_yaml_string("k: >\n")


if __name__ == "__main__":
    unittest.main()
