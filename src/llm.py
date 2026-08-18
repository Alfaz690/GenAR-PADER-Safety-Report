import os
from dotenv import load_dotenv

load_dotenv()


def get_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is missing. Copy .env.example to .env and add your API key."
        )
    try:
        from openai import OpenAI
    except ImportError as exc:
        raise RuntimeError("The OpenAI package is not installed. Use offline mode or install requirements.txt.") from exc
    return OpenAI(api_key=api_key)


def generate_text(user_prompt: str) -> str:
    client = get_client()
    model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

    response = client.chat.completions.create(
        model=model,
        temperature=0.1,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a careful regulatory safety-report writing assistant. "
                    "Follow the supplied evidence exactly. "
                    "Never invent unsupported facts."
                ),
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
    )

    return response.choices[0].message.content.strip()
