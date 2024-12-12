import requests
from utils.helper import fetch_payload


def fetch_verdicts(
    url: str, client_id: str, header: str, domains: tuple[str]
) -> dict[str, list]:
    results = {"answer": []}

    for domain in domains:
        payload = fetch_payload(client_id, domain)

        try:
            response = requests.post(url=url, json=payload, headers=header)
            response.raise_for_status()

            data = response.json()
            verdict = data.get("verdict_status")

            if domain and verdict:
                results["answer"].append({"domain": domain, "verdict": verdict})
        except requests.RequestException as e:
            print(f"HTTP error occurred for {domain}: {e}")
        except ValueError as e:
            print(f"Failed to parse JSON response for {domain}: {e}")
        except Exception as e:
            print(f"An unexpected error occurred for {domain}: {e}")
    return results
