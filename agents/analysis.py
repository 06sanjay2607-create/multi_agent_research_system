from ai_model import ask_ai


def analysis_agent(checked_data):
    facts = checked_data["verified_facts"]

    fact_text = ""

    for item in facts:
        fact_text += item["fact"] + "\n"

    prompt = f"""
You are an Analysis Agent.

Analyze the following research facts:

{fact_text}

Prepare the analysis with these sections:

1. Short Summary
2. Three Important Insights
3. Benefits
4. Limitations
5. Final Conclusion

Use simple and clear English.
Do not invent facts, sources, or statistics.
"""

    ai_analysis = ask_ai(prompt)

    return {
        "total_facts": len(facts),
        "analysis": ai_analysis,
        "sources": checked_data["sources"]
    }