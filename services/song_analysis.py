from services.ai_service import ask_ai


def analyze_song(song):

    prompt = (
        f"Analyze meaning of song {song}"
    )

    return ask_ai(prompt)