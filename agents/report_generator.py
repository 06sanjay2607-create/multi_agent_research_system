from ai_model import ask_ai


def report_generation_agent(topic, analysis_data):

    analysis = analysis_data.get("analysis", "")
    sources = analysis_data.get("sources", [])

    source_text = "\n".join(
        f"- {source}" for source in sources
    )

    prompt = f"""
You are a professional AI research assistant.

Your job is to create a high-quality, natural research answer
similar to modern AI assistants such as ChatGPT and Gemini.

Research Topic:
{topic}

Research Analysis:
{analysis}

Available Sources:
{source_text}


Write the final answer for the user.

IMPORTANT WRITING STYLE:

- Start with the answer directly.
- Do not use Markdown heading symbols such as # or ##.
- Do not use labels such as "Step 1", "Step 2", etc.
- Do not make the answer look like a school textbook.
- Use a professional and natural writing style.
- Use simple English words.
- Give deep and useful information without unnecessary length.
- Make the answer easy to understand and easy to learn.
- Use short paragraphs.
- Use bold headings only when they genuinely improve readability.
- Mix short paragraphs and useful points naturally.
- Avoid repeating the same information.


CONTENT REQUIREMENTS:

1. Start with a clear direct answer.
   Give enough introduction to understand the topic.

2. Explain the most important points.
   Give 4 to 10 useful points when enough information is available.

3. Each important point should contain:
   - A clear short heading.
   - 1 to 4 easy sentences.
   - Actual explanation, not only a definition.
   - A relevant example or practical detail when useful.

4. Explain how the topic works or is used when relevant.
   Do not add this section if it is not useful for the topic.

5. Explain important benefits when relevant.

6. Explain important challenges or limitations when relevant.

7. End with a clear conclusion.
   The conclusion should summarize the main idea in 2 to 10 lines.
   Do not introduce unrelated new information.

8. Add relevant sources at the end if reliable sources are available.


IMPORTANT ACCURACY RULES:

- Use only information supported by the research provided.
- Do not invent facts.
- Do not invent statistics.
- Do not invent sources.
- Do not make unsupported claims.
- Do not repeat information.
- Do not add unnecessary filler.
- Do not use complicated technical words unless necessary.
- Do not make every topic follow exactly the same structure.
- Choose the structure naturally based on the topic.
- If the research does not contain enough information, clearly say so.


OUTPUT STYLE EXAMPLE:

Artificial Intelligence in Agriculture

Artificial Intelligence (AI) is helping agriculture become more
data-driven and efficient. It can analyze information about soil,
weather, crops, and plant health. This information can help farmers
make better decisions and identify problems earlier.

**Crop Monitoring**

AI can analyze crop images and other farming data to identify
changes in plant health. This can help farmers notice problems
earlier and take suitable action.

**Disease Detection**

AI can identify patterns that may be related to plant diseases.
Early detection can help farmers respond before the problem becomes
more serious.

**Smart Irrigation**

AI can use soil and weather information to support better watering
decisions. This can help reduce unnecessary water usage.

**Benefits**

AI can help improve decision-making, reduce resource waste, and
support more efficient farming practices.

**Challenges**

AI systems may require reliable data, suitable technology, and
people with the skills needed to use them properly.

**Conclusion**

AI can make agriculture smarter and more data-driven. Its value
comes from helping farmers understand useful information and make
better decisions. With proper data and implementation, it can be a
useful technology for modern agriculture.

Sources

List only the reliable sources provided above.
"""


    try:
        report = ask_ai(prompt)

    except Exception as e:
        report = f"Report Generation Error: {str(e)}"

    return report