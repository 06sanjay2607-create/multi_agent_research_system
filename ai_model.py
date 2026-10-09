
from groq import Groq
import os

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError(
        "GROQ_API_KEY is missing. Please configure your API key."
    )

client = Groq(api_key=api_key)


def ask_ai(prompt):

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "system",
                    "content": """
You are a helpful, detailed AI assistant.

Instructions:
- Answer the user's actual question directly.
- Explain complex topics step by step.
- Use headings, subheadings, and bullet points.
- Include relevant examples and practical applications.
- Explain important points instead of listing them briefly.
- Include advantages, limitations, and analysis when relevant.
- Provide a conclusion for detailed research questions.
- Use simple, professional English.
- Avoid unnecessary repetition.
- Never invent facts, statistics, or sources.
- Adjust answer length to the complexity of the question.
- For research questions, generate a comprehensive report.
"""
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.4,
            max_tokens=4000
        )

        answer = response.choices[0].message.content

        if answer and answer.strip():
            return answer.strip()

        return "The AI model returned an empty response. Please try again."

    except Exception as e:

        error_text = str(e)
        print("AI Model Error:", error_text)

        if "429" in error_text or "rate_limit_exceeded" in error_text:
            return (
                "Groq rate limit reached. "
                "Please wait until your usage limit resets."
            )

        return (
            "Unable to generate the answer. "
            "Please check the AI model connection and server logs."
        )