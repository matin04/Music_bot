from services.ai_service import ask_ai


def generate_tags(song):

    prompt = (
        f"Generate hashtags for {song}"
    )

    return ask_ai(prompt)