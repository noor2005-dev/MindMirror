"""Prompt templates for MindMirror's Feynman-style student agent."""
STUDENT_SYSTEM_PROMPT = """You are a curious beginner student learning a topic from the user.
Act genuinely confused where the explanation leaves a gap. Do not teach, grade, or
summarize. Ask exactly ONE short, clear, beginner-level follow-up question per turn.
Refer to the explanation and probe one specific unclear idea, missing step, assumption,
or example. Avoid trick questions and jargon. Do not ask multiple questions.
Return only the question."""

def build_student_messages(topic: str, level: str, explanation: str,
                           history: list[dict[str, str]] | None = None) -> list[dict[str, str]]:
    messages = [{"role": "system", "content": STUDENT_SYSTEM_PROMPT},
                {"role": "user", "content": (
                    f"Topic: {topic}\nLearner level: {level}\n"
                    "Ask one useful beginner question about this explanation:\n" + explanation
                )}]
    for item in (history or [])[-8:]:
        role, content = item.get("role"), item.get("content", "")
        if role in {"user", "assistant"} and content:
            messages.append({"role": role, "content": content})
    return messages
