def extraction_agent(research_data):

    information = research_data.get("information", [])
    sources = research_data.get("sources", [])

    document = research_data.get("document")

    if document:

        information = information.copy()

        information.append(
            f"\nDocument: {document['filename']}\n"
            f"{document['text']}"
        )

    facts = []

    for item in information:

        if item and str(item).strip():

            facts.append({
                "fact": str(item).strip()
            })

    return {
        "facts": facts,
        "sources": sources
    }


if __name__ == "__main__":

    sample_data = {
        "information": [
            "Artificial Intelligence helps computers perform human-like tasks."
        ],
        "sources": [
            "Research source"
        ]
    }

    result = extraction_agent(sample_data)

    print("\nExtracted Facts:")
    print(result)