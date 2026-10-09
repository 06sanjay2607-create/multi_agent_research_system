
from ai_model import ask_ai


def report_generation_agent(topic, analysis_data):

    analysis = analysis_data.get("analysis", "")

    if not analysis:
        analysis = str(analysis_data)

    prompt = f"""
You are an advanced AI research assistant.

Research Topic: {topic}

Research and Analysis Findings:
{analysis}

Write a detailed, high-quality final research report.

Follow this structure:

# 1. Introduction
Explain the topic and its importance.

# 2. Detailed Explanation
Explain the topic clearly using headings and subheadings.

# 3. Key Findings
Present the important findings in bullet points with explanations.

# 4. Detailed Analysis
Analyze the findings, their meaning, and their implications.

# 5. Real-World Applications
Give relevant practical examples and use cases.

# 6. Benefits
Explain the major advantages in detail.

# 7. Challenges and Limitations
Explain relevant problems and limitations.

# 8. Future Scope
Describe possible future developments where relevant.

# 9. Conclusion
Summarize the main insights clearly.

# 10. Sources
Include source URLs only if they are available in the supplied research data.

IMPORTANT RULES:
- Answer the research topic directly.
- Give detailed explanations, not just short summaries.
- Use clear professional English.
- Use bullet points and examples wherever useful.
- Avoid repeating the same information.
- Never invent facts, statistics, or source URLs.
- If the research data is insufficient, clearly mention the limitation.
- Adjust the report length to the complexity of the topic.
- Return the complete report in Markdown.
"""

    try:
        result = ask_ai(prompt)

        if isinstance(result, str) and result.strip():
            return result.strip()

        return "Unable to generate the final report. Please try again."

    except Exception as error:
        print("Report generation error:", error)
        return (
            f"Unable to generate a detailed report for '{topic}'. "
            "Please check the AI model connection."
        )