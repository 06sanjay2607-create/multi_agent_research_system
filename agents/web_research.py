import requests
from concurrent.futures import ThreadPoolExecutor, as_completed


def get_wikipedia_summary(title):

    try:

        url = (
            "https://en.wikipedia.org/api/rest_v1/page/summary/"
            + title.replace(" ", "_")
        )

        headers = {
            "User-Agent": "Multi-Agent-Research-System/1.0"
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=8
        )

        if response.status_code == 200:

            data = response.json()

            summary = data.get("extract", "")

            page_url = data.get(
                "content_urls",
                {}
            ).get(
                "desktop",
                {}
            ).get(
                "page",
                ""
            )

            if summary:

                return {
                    "title": title,
                    "summary": summary,
                    "url": page_url
                }

    except Exception as e:

        print("Summary error:", e)

    return None


def web_research_agent(topic):

    print("🔎 Fast Web Research:", topic)

    information = []
    sources = []

    try:

        search_url = "https://en.wikipedia.org/w/api.php"

        headers = {
            "User-Agent": "Multi-Agent-Research-System/1.0"
        }

        # --------------------------------
        # Multiple Relevant Search Queries
        # --------------------------------

        search_queries = [
            topic,
            topic + " applications",
            topic + " benefits",
            topic + " challenges",
            topic + " research"
        ]

        all_titles = []

        # --------------------------------
        # Search Wikipedia
        # --------------------------------

        for query in search_queries:

            params = {
                "action": "query",
                "list": "search",
                "srsearch": query,
                "format": "json",
                "srlimit": 3
            }

            response = requests.get(
                search_url,
                params=params,
                headers=headers,
                timeout=8
            )

            print(
                "Wikipedia Search:",
                query,
                "Status:",
                response.status_code
            )

            if response.status_code == 200:

                data = response.json()

                results = data.get(
                    "query",
                    {}
                ).get(
                    "search",
                    []
                )

                for item in results:

                    title = item.get("title", "")

                    if title and title not in all_titles:

                        all_titles.append(title)

        # --------------------------------
        # Limit Results
        # --------------------------------

        all_titles = all_titles[:10]

        print(
            "📚 Relevant pages found:",
            len(all_titles)
        )

        # --------------------------------
        # Fetch summaries in parallel
        # --------------------------------

        with ThreadPoolExecutor(max_workers=5) as executor:

            tasks = [
                executor.submit(
                    get_wikipedia_summary,
                    title
                )
                for title in all_titles
            ]

            for task in as_completed(tasks):

                result = task.result()

                if result:

                    information.append(
                        result["summary"]
                    )

                    sources.append(
                        result["title"]
                        + " - "
                        + result["url"]
                    )

    except Exception as e:

        print("Web research failed:", e)

    # --------------------------------
    # No Result
    # --------------------------------

    if not information:

        information.append(
            "No reliable web information was found for this topic."
        )

        sources.append(
            "No source available"
        )

    print(
        "✅ Sources found:",
        len(sources)
    )

    return {
        "topic": topic,
        "sources": sources,
        "information": information
    }