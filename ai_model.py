from groq import Groq
import os
import time

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def ask_ai(prompt):

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_tokens=700
        )

        return response.choices[0].message.content

    except Exception as e:

        error_text = str(e)

        if "429" in error_text or "rate_limit_exceeded" in error_text:
            return (
                "AI LIMIT REACHED. "
                "Groq daily token limit is currently exhausted. "
                "Please try again after the limit resets."
            )

        return f"AI Error: {error_text}"