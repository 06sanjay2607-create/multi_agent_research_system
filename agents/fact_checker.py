def fact_checking_agent(extracted_data):

    facts = extracted_data.get("facts", [])
    sources = extracted_data.get("sources", [])

    verified_facts = []

    for fact in facts:

        verified_facts.append({
            "fact": fact,
            "status": "Based on the available research sources"
        })

    return {
        "verified_facts": verified_facts,
        "sources": sources
    }