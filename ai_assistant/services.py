"""AI assistant response generation (rule-based demo; swap for OpenAI API in production)."""

import random

CODING_RESPONSES = [
    "Great question! Start by breaking the problem into smaller functions. Each function should do one thing well.",
    "Consider using list comprehensions here — they're more Pythonic and often faster for simple transforms.",
    "Your approach is on track. Add error handling with try/except around the I/O operations.",
    "Think about edge cases: empty input, None values, and large datasets. Test those first.",
    "Refactor duplicated logic into a helper function. DRY principle will make debugging easier.",
    "For performance, profile before optimizing. `cProfile` in Python is your friend.",
    "Use type hints — they improve readability and catch bugs early with mypy or Pyright.",
    "This pattern maps well to a generator if you're processing streams of data.",
]

GENERAL_RESPONSES = [
    "I'm Nexus AI, your coding mentor. Ask me about Python, JavaScript, algorithms, or any lesson concept.",
    "Let's debug together. Share your error message and the code snippet that's failing.",
    "Remember: consistent practice beats cramming. Even 30 minutes daily compounds quickly.",
    "Check the course lesson on this topic — it has hands-on exercises that reinforce the concept.",
]


def generate_ai_response(user_message: str, context: str = '') -> str:
    """Generate a contextual AI response. Replace with LLM API call in production."""
    msg = user_message.lower()

    if any(kw in msg for kw in ('error', 'bug', 'fix', 'debug', 'traceback')):
        return (
            "Let's debug step by step:\n\n"
            "1. Read the full error message — the last line usually tells you the type.\n"
            "2. Check line numbers in the traceback.\n"
            "3. Print intermediate values with `print()` or a debugger.\n"
            "4. Isolate the failing function with a minimal test case.\n\n"
            "Paste your traceback and I'll help pinpoint the issue."
        )

    if any(kw in msg for kw in ('python', 'javascript', 'react', 'django', 'function', 'class', 'loop')):
        return random.choice(CODING_RESPONSES)

    if any(kw in msg for kw in ('hello', 'hi', 'hey')):
        return "Hello! I'm your Nexus AI assistant. What are you building today?"

    if context:
        return f"Based on your lesson context ({context[:80]}…): {random.choice(CODING_RESPONSES)}"

    return random.choice(GENERAL_RESPONSES)
