"""Confused Student Agent: asks one beginner question per explanation round."""
from services.llm import chat_completion
from prompts.prompts import build_student_messages

class ConfusedStudentAgent:
    """Generate focused follow-up questions for a Feynman learning session."""
    def __init__(self, model: str | None = None):
        self.model = model

    def ask_question(self, topic: str, level: str, explanation: str,
                     history: list[dict[str, str]] | None = None) -> str:
        if not topic.strip():
            raise ValueError("Topic is required.")
        if not level.strip():
            raise ValueError("Learner level is required.")
        if not explanation.strip():
            raise ValueError("Explanation is required.")
        question = chat_completion(
            build_student_messages(topic, level, explanation, history),
            temperature=0.7, max_tokens=120, model=self.model,
        ).strip().splitlines()[0].strip()
        if "?" in question:
            question = question[:question.find("?") + 1]
        if not question.endswith("?"):
            question = question.rstrip(".! ") + "?"
        return question

def generate_student_question(topic: str, level: str, explanation: str,
                              history: list[dict[str, str]] | None = None) -> str:
    """Convenience function for callers that do not need an agent instance."""
    return ConfusedStudentAgent().ask_question(topic, level, explanation, history)

def validate_round_count(rounds: int) -> int:
    """Validate the PRD's supported 3–5 question rounds."""
    if isinstance(rounds, bool) or not isinstance(rounds, int) or not 3 <= rounds <= 5:
        raise ValueError("Round count must be an integer from 3 to 5.")
    return rounds
