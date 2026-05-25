from services.ai_service import ask_ai


def recommend_music(song_name):

    prompt = (
        f"Recommend 10 songs similar to {song_name}"
    )

    return ask_ai(prompt)