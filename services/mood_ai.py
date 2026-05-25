from services.ai_service import ask_ai


def detect_mood(text):

    prompt = (
        f"What mood is this song:\n{text}"
    )

    return ask_ai(prompt)