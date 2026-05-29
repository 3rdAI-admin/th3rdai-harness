import unittest

from scripts.orchestrator import config, gates


def _all_approval_phrases():
    policies = config.load_tools().get("tool_policies", {})
    phrases = []
    for policy in policies.values():
        if isinstance(policy, dict):
            phrases.extend(policy.get("requires_approval", []) or [])
    return phrases


class TestRequiresApproval(unittest.TestCase):
    def test_every_real_phrase_flags(self):
        phrases = _all_approval_phrases()
        self.assertGreater(len(phrases), 0, "expected some requires_approval phrases")
        for phrase in phrases:
            with self.subTest(phrase=phrase):
                self.assertTrue(
                    gates.requires_approval(phrase),
                    f"phrase should require approval: {phrase!r}",
                )

    def test_case_insensitive_and_whitespace(self):
        self.assertTrue(gates.requires_approval("GIT   Commit"))

    def test_containment_either_direction(self):
        # action is a substring of a phrase ("git commit" appears verbatim,
        # but also a shorter action contained by a phrase should flag)
        self.assertTrue(gates.requires_approval("staging"))  # in "git staging"
        # phrase is a substring of the action
        self.assertTrue(gates.requires_approval("please git commit now"))

    def test_clearly_allowed_actions_not_gated(self):
        self.assertFalse(gates.requires_approval("read files"))
        self.assertFalse(gates.requires_approval("search workspace"))

    def test_empty_action(self):
        self.assertFalse(gates.requires_approval(""))

    def test_policies_override(self):
        custom = {"p": {"requires_approval": ["launch missiles"]}}
        self.assertTrue(gates.requires_approval("launch missiles", custom))
        self.assertFalse(gates.requires_approval("git commit", custom))


class TestGatedActions(unittest.TestCase):
    def test_subset_order_preserved(self):
        actions = ["read files", "git commit", "search workspace"]
        self.assertEqual(gates.gated_actions(actions), ["git commit"])

    def test_dedupe(self):
        actions = ["git commit", "git commit", "read files"]
        self.assertEqual(gates.gated_actions(actions), ["git commit"])

    def test_none_gated(self):
        self.assertEqual(gates.gated_actions(["read files", "search workspace"]), [])


class TestConfirm(unittest.TestCase):
    def test_empty_returns_true(self):
        self.assertTrue(gates.confirm([]))

    def test_no_gated_returns_true_without_prompting(self):
        def boom(*_):
            raise AssertionError("prompt_fn should not be called when nothing is gated")

        self.assertTrue(gates.confirm(["read files"], prompt_fn=boom))

    def test_assume_yes(self):
        messages = []
        self.assertTrue(
            gates.confirm(["git commit"], assume_yes=True, out=messages.append)
        )
        self.assertTrue(any("git commit" in m for m in messages))

    def test_reply_no(self):
        self.assertFalse(gates.confirm(["git commit"], prompt_fn=lambda *_: "n"))

    def test_reply_yes(self):
        self.assertTrue(gates.confirm(["git commit"], prompt_fn=lambda *_: "yes"))

    def test_reply_y_variants(self):
        self.assertTrue(gates.confirm(["git commit"], prompt_fn=lambda *_: "  Y  "))
        self.assertTrue(gates.confirm(["git commit"], prompt_fn=lambda *_: "YES"))

    def test_prompt_called_once(self):
        calls = []

        def once(msg):
            calls.append(msg)
            return "y"

        gates.confirm(["git commit", "installing dependencies"], prompt_fn=once)
        self.assertEqual(len(calls), 1)


class TestProtectedWrites(unittest.TestCase):
    def test_filters_protected(self):
        paths = [
            "agents/x.md",
            "runs/y.md",
            "configs/z.yaml",
            "scripts/orchestrator/q.py",
            "output/n.md",
        ]
        self.assertEqual(
            gates.protected_writes(paths),
            ["agents/x.md", "configs/z.yaml", "scripts/orchestrator/q.py"],
        )

    def test_leading_dot_slash_normalized(self):
        self.assertEqual(
            gates.protected_writes(["./agents/a.md", "./runs/b.md"]),
            ["./agents/a.md"],
        )

    def test_custom_prefixes(self):
        self.assertEqual(
            gates.protected_writes(["secrets/x", "runs/y"], prefixes=("secrets/",)),
            ["secrets/x"],
        )


if __name__ == "__main__":
    unittest.main()
