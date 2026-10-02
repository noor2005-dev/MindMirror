# MindMirror
AI-powered learning tool based on the Feynman Technique.

## Member 2: Groq Confused Student Agent

The agent asks one short, beginner-level follow-up question about the learner's latest explanation.

### Setup
1. Create and activate a Python virtual environment.
2. Install dependencies: `pip install -r requirements.txt`.
3. Set `GROQ_API_KEY` in your environment, or add it to Streamlit secrets. Never commit API keys.
4. Optional: set `GROQ_MODEL` to override the default model (`llama-3.3-70b-versatile`).

### Use
```python
from modules.student_agent import ConfusedStudentAgent, validate_round_count

agent = ConfusedStudentAgent()
question = agent.ask_question(
    topic="Gravity",
    level="beginner",
    explanation="Gravity is a force that attracts objects with mass.",
    history=[],
)
rounds = validate_round_count(3)  # supported range: 3–5
```

### Test
Run the unit tests without making a live API request:
```bash
python -m unittest discover -s tests -v
```
