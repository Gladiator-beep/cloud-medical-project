from config import Config

def clean_text(text, max_length=450):
    if not text:
        return "No summary available."

    text = text.replace("\n", " ").strip()

    if len(text) > max_length:
        text = text[:max_length] + "..."

    return text


def search_diagnosis_info(diagnosis):
    if not Config.TAVILY_API_KEY or Config.TAVILY_API_KEY == "PUT_YOUR_TAVILY_KEY_HERE":
        return [
            {
                "title": "Demo Search Result",
                "summary": f"Demo mode: example reliable medical information about diagnosis: {diagnosis}",
                "url": "#"
            }
        ]

    try:
        from tavily import TavilyClient

        client = TavilyClient(api_key=Config.TAVILY_API_KEY)

        response = client.search(
            query=f"{diagnosis} diagnosis treatment reliable medical source Mayo Clinic MedlinePlus NIH",
            max_results=3,
            search_depth="basic"
        )

        cleaned_results = []

        for item in response.get("results", []):
            cleaned_results.append({
                "title": item.get("title", "No title"),
                "summary": clean_text(item.get("content", "")),
                "url": item.get("url", "#")
            })

        return cleaned_results

    except Exception as e:
        return [
            {
                "title": "Search Error",
                "summary": f"Error while searching Tavily: {e}",
                "url": "#"
            }
        ]