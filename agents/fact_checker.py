from ai_model import ask_ai


def fact_checking_agent(extracted_data):
    verified_facts = []

    for fact in extracted_data["facts"]:
        prompt = f"""
You are a fact-checking agent.

Check the following research information carefully:

{fact}

Give the result in this format:

Status: Likely True / Needs Verification
Reason: Explain briefly in simple English.
Source Check: Mention whether a reliable source is available.

Do not invent sources or statistics.
"""

        result = ask_ai(prompt)

        verified_facts.append({
            "fact": fact,
            "status": result
        })

    return {
        "verified_facts": verified_facts,
        "sources": extracted_data["sources"]
    }