import requests
import os
from dotenv import load_dotenv

load_dotenv()


def recognize_music(audio_path):
    token = os.getenv("AUDD_TOKEN")

    with open(audio_path, "rb") as f:
        response = requests.post(
            "https://api.audd.io/",
            data={
                "api_token": token,
                "return": "apple_music,spotify"
            },
            files={
                "file": f
            }
        )

    return response.json()