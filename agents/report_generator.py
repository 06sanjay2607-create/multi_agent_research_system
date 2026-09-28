from ai_model import ask_ai


def report_generation_agent(topic, analysis_data):

    analysis = analysis_data["analysis"]
    sources = analysis_data.get("sources", [])

    source_text = "\n".join(f"- {source}" for source in sources)

    prompt = f"""
You are a helpful AI research assistant.

Research Topic:
{topic}

Research Analysis:
{analysis}

Available Sources:
{source_text}

Create a simple and easy-to-understand answer.

Use this format:

# {topic}

## What is it?
Explain in 2-4 simple sentences.

## How does it work?
Explain using simple numbered steps.

## Key Points
Give 4-6 important points.

## Benefits
Give simple bullet points.

## Limitations
Give simple bullet points.

## Conclusion
Give a short conclusion.

## Sources
List only the sources provided above.

Rules:
- Use simple English.
- Keep sentences short.
- Avoid unnecessary technical words.
- Do not repeat information.
- Do not invent facts.
- Do not invent statistics.
- Do not invent sources.
- Use only the research information provided.
- Make the answer easy to read.
"""

    report = ask_ai(prompt)

    return report