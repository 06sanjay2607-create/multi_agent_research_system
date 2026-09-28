from ai_model import ask_ai


def extraction_agent(research_data):
    information = research_data["information"]

    prompt = f"""
You are an Information Extraction Agent.

From the following research information, extract the important facts.
Give the facts as a simple numbered list.

Research Information:
{information}
"""

    ai_result = ask_ai(prompt)

    return {
        "facts": [ai_result],
        "sources": research_data["sources"]
    }


if __name__ == "__main__":
    sample_data = {
        "information": [
            "Artificial Intelligence helps computers perform human-like tasks."
        ],
        "sources": ["Local Ollama AI model"]
    }

    result = extraction_agent(sample_data)

    print("\nExtracted Facts:")
    print(result)