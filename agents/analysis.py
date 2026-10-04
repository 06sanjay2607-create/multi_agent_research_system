from ai_model import ask_ai


def analysis_agent(checked_data):

    facts = checked_data.get("verified_facts", [])

    sources = checked_data.get("sources", [])

    fact_text = ""

    for index, item in enumerate(facts, start=1):

        fact_text += f"""
Fact {index}:
{item.get("fact", "")}

Verification:
{item.get("status", "")}

"""


    prompt = f"""
You are an expert AI Research Analysis Agent.

Analyze the verified research information below.

RESEARCH INFORMATION:
{fact_text}

AVAILABLE SOURCES:
{sources}


Create a professional research analysis.

Use EXACTLY these sections:

EXECUTIVE SUMMARY
Write a short 3-4 sentence summary of the research.

KEY INSIGHTS
Give 4 important insights.
Number them from 1 to 4.

BENEFITS
Give 4 important benefits.
Use bullet points.

LIMITATIONS
Give 3 important limitations.
Use bullet points.

IMPORTANT FINDINGS
Give the most important findings from the available research.

FINAL INSIGHT
Give a short and clear conclusion based only on the provided research.


IMPORTANT RULES:

- Use only the information provided.
- Do not invent facts.
- Do not invent statistics.
- Do not invent sources.
- Do not make unsupported claims.
- Keep the language simple and professional.
- Avoid unnecessary technical words.
- Do not repeat the same information.
- Clearly separate facts from conclusions.
"""


    try:

        ai_analysis = ask_ai(prompt)

    except Exception as e:

        ai_analysis = f"AI Analysis Error: {str(e)}"


    return {
        "total_facts": len(facts),
        "analysis": ai_analysis,
        "sources": sources
    }