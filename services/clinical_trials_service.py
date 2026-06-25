import requests

def search_clinical_trials(drug_name):
    url = "https://clinicaltrials.gov/api/v2/studies"

    params = {
        "query.term": drug_name,
        "pageSize": 5
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        studies = data.get("studies", [])

        results = []

        for study in studies:
            protocol = study.get("protocolSection", {})

            identification = protocol.get("identificationModule", {})
            status = protocol.get("statusModule", {})
            conditions = protocol.get("conditionsModule", {})

            nct_id = identification.get("nctId", "No ID")
            title = identification.get("briefTitle", "No title")
            overall_status = status.get("overallStatus", "Unknown")
            condition_list = conditions.get("conditions", [])

            results.append({
                "nct_id": nct_id,
                "title": title,
                "status": overall_status,
                "conditions": ", ".join(condition_list),
                "url": f"https://clinicaltrials.gov/study/{nct_id}"
            })

        return results

    except Exception as e:
        return [{
            "nct_id": "Error",
            "title": f"ClinicalTrials API error: {e}",
            "status": "Error",
            "conditions": "",
            "url": "#"
        }]