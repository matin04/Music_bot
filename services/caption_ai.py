from services.ai_service import ask_ai


def generate_caption(song):

    prompt = (
        f"Create Instagram caption for {song}"
    )

    return ask_ai(prompt)