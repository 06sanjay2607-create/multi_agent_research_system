from agents.web_research import web_research_agent
from agents.extraction import extraction_agent
from agents.fact_checker import fact_checking_agent
from agents.analysis import analysis_agent
from agents.report_generator import report_generation_agent


def run_research(topic, progress_callback=None):

    print("1. Web Research Agent running...")

    if progress_callback:
        progress_callback(1, "Working")

    research = web_research_agent(topic)

    if progress_callback:
        progress_callback(1, "Completed")


    print("2. Information Extraction Agent running...")

    if progress_callback:
        progress_callback(2, "Working")

    extracted = extraction_agent(research)

    if progress_callback:
        progress_callback(2, "Completed")


    print("3. Fact-Checking Agent running...")

    if progress_callback:
        progress_callback(3, "Working")

    checked = fact_checking_agent(extracted)

    if progress_callback:
        progress_callback(3, "Completed")


    print("4. Analysis Agent running...")

    if progress_callback:
        progress_callback(4, "Working")

    analyzed = analysis_agent(checked)

    if progress_callback:
        progress_callback(4, "Completed")


    print("5. Report Generation Agent running...")

    if progress_callback:
        progress_callback(5, "Working")

    report = report_generation_agent(topic, analyzed)

    if progress_callback:
        progress_callback(5, "Completed")


    return report