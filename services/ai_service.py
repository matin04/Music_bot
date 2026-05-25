from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv(
        "OPENAI_API_KEY"
    )
)


def ask_ai(prompt: str):

    response = client.chat.completions.create(
        model="gpt-4.1-mini",

        messages=[
            {
                "role": "system",
                "content": (
                    "You are a music assistant"
                )
            },

            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content