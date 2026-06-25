import requests

def search_side_effects(drug_name):
    url = "https://api.fda.gov/drug/label.json"

    params = {
        "search": f'openfda.brand_name:"{drug_name}" OR openfda.generic_name:"{drug_name}"',
        "limit": 3
    }

    try:
        response = requests.get(url, params=params, timeout=10)

        if response.status_code != 200:
            return [{
                "drug": drug_name,
                "source": "openFDA",
                "side_effects": f"No side effects found or API error. Status code: {response.status_code}"
            }]

        data = response.json()
        results = []

        for item in data.get("results", []):
            openfda = item.get("openfda", {})
            brand_names = openfda.get("brand_name", [])
            generic_names = openfda.get("generic_name", [])

            adverse_reactions = item.get("adverse_reactions", [])
            warnings = item.get("warnings", [])

            text = " ".join(adverse_reactions[:2]) if adverse_reactions else "No adverse reactions section found."
            warning_text = " ".join(warnings[:1]) if warnings else ""

            if len(text) > 800:
                text = text[:800] + "..."

            if len(warning_text) > 400:
                warning_text = warning_text[:400] + "..."

            results.append({
                "drug": ", ".join(brand_names) if brand_names else drug_name,
                "generic": ", ".join(generic_names),
                "source": "openFDA Drug Label",
                "side_effects": text,
                "warnings": warning_text
            })

        return results

    except Exception as e:
        return [{
            "drug": drug_name,
            "source": "openFDA",
            "side_effects": f"Error while searching side effects: {e}"
        }]