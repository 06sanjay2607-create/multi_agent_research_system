from agents.web_research import web_research_agent
from agents.extraction import extraction_agent
from agents.fact_checker import fact_checking_agent
from agents.analysis import analysis_agent
from agents.report_generator import report_generation_agent


def run_research(topic, progress_callback=None, document_text=None, document_name=None):

    # =====================================================
    # 1. WEB RESEARCH
    # =====================================================

    print("1. Web Research Agent running...")

    if progress_callback:
        progress_callback(1, "Working")

    research = web_research_agent(topic)
    if document_text:
     research["document"] = {
        "filename": document_name,
        "text": document_text
    }

    if progress_callback:
        progress_callback(1, "Completed")


    # =====================================================
    # 2. INFORMATION EXTRACTION
    # =====================================================

    print("2. Information Extraction Agent running...")

    if progress_callback:
        progress_callback(2, "Working")

    extracted = extraction_agent(research)

    if progress_callback:
        progress_callback(2, "Completed")


    # =====================================================
    # 3. FACT CHECKING
    # =====================================================

    print("3. Fact-Checking Agent running...")

    if progress_callback:
        progress_callback(3, "Working")

    checked = fact_checking_agent(extracted)

    if progress_callback:
        progress_callback(3, "Completed")


    # =====================================================
    # 4. AI ANALYSIS
    # =====================================================

    print("4. Analysis Agent running...")

    if progress_callback:
        progress_callback(4, "Working")

    analyzed = analysis_agent(checked)

    if progress_callback:
        progress_callback(4, "Completed")


    # =====================================================
    # 5. FINAL REPORT
    # =====================================================

    print("5. Report Generation Agent running...")

    if progress_callback:
        progress_callback(5, "Working")

    report = report_generation_agent(
        topic,
        analyzed
    )

    if progress_callback:
        progress_callback(5, "Completed")


    # =====================================================
    # GET DATA
    # =====================================================

    analysis = analyzed.get(
        "analysis",
        ""
    )

    sources = analyzed.get(
        "sources",
        []
    )

    facts = analyzed.get(
        "total_facts",
        0
    )


    # =====================================================
    # DEBUG
    # =====================================================

    print("\n==============================")
    print("RESEARCH COMPLETED")
    print("==============================")

    print("Topic:", topic)

    print("Analysis available:",
          bool(analysis))

    print("Sources found:",
          len(sources))

    print("Sources:")

    for source in sources:
        print("-", source)

    print("==============================\n")


    # =====================================================
    # RETURN EVERYTHING
    # =====================================================

    return {

        "report": report,

        "analysis": analysis,

        "sources": sources,

        "facts": facts

    }