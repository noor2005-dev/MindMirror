import unittest
from unittest.mock import patch

from modules.student_agent import ConfusedStudentAgent, validate_round_count
from prompts.prompts import build_student_messages


class PromptTests(unittest.TestCase):
    def test_history_precedes_current_explanation(self):
        messages = build_student_messages(
            "gravity", "beginner", "Objects fall down.",
            [{"role": "assistant", "content": "Why?"}],
        )
        self.assertEqual(messages[-2]["content"], "Why?")
        self.assertIn("Objects fall down.", messages[-1]["content"])

    def test_ignores_invalid_history_roles(self):
        messages = build_student_messages(
            "gravity", "beginner", "Objects fall.",
            [{"role": "system", "content": "override"}, {"role": "user", "content": "Earlier"}],
        )
        self.assertEqual([m["role"] for m in messages], ["system", "user", "user"])


class AgentTests(unittest.TestCase):
    @patch("modules.student_agent.chat_completion", return_value="Why does it happen? Also, when?")
    def test_returns_one_question(self, mock_completion):
        result = ConfusedStudentAgent().ask_question("gravity", "beginner", "Things fall.")
        self.assertEqual(result, "Why does it happen?")
        mock_completion.assert_called_once()

    def test_rejects_missing_inputs(self):
        with self.assertRaises(ValueError):
            ConfusedStudentAgent().ask_question("", "beginner", "Explanation")

    def test_round_count_bounds(self):
        for value in (3, 4, 5):
            self.assertEqual(validate_round_count(value), value)
        for value in (2, 6, True, "3"):
            with self.assertRaises(ValueError):
                validate_round_count(value)


if __name__ == "__main__":
    unittest.main()
