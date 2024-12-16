import sys
import readline
import pandas as pd
from pathlib import Path
from api.hyas_api import APIClient
from typing import List, Dict, Any


def _autocomplete_path(text: str, state: int) -> str:
    path = Path(text).expanduser()
    directory = path.parent if path.parent.exists() else Path(".")
    basename = path.name

    matches = [
        str(match) for match in directory.iterdir() if match.name.startswith(basename)
    ]

    return matches[state] if state < len(matches) else None


async def fetch_domain_verdict(client: APIClient, domain: str) -> Dict[str, Any]:
    try:
        response = await client.verdict(domain)
        verdict = response.get("verdict_status", "error")
        print(f"Success: {domain} - Verdict: {verdict}")
        return {"domain": domain, "verdict": verdict}
    except Exception as e:
        print(f"Error processing {domain}: {e}")
        return {"domain": domain, "verdict": "error"}


def get_filepath() -> str:
    readline.set_completer(_autocomplete_path)
    readline.parse_and_bind("tab: complete")

    retries = 3
    while retries > 0:
        filepath = input("\nEnter the file path to your txt or csv: ").strip()
        path = Path(filepath).expanduser().resolve()

        if path.exists():
            if path.suffix.lower() in [".txt", ".csv"]:
                print("File path is valid.")
                return str(path)
            else:
                print("Invalid file type. Expected txt or csv.")
        else:
            print("Path does not exist.")

        retries -= 1
        if retries > 0:
            print(f"Retries left: {retries}. Please try again.")
        else:
            print("Exceeded maximum retries. Exiting...")
            sys.exit(1)


def read_file(filepath: str) -> List[str]:
    try:
        with open(filepath, "r") as file:
            lines = {line.strip() for line in file if line.strip()}

        if not lines:
            print("Error: The input file empty.")
            sys.exit(1)

        return list(lines)
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        sys.exit(1)


def generate_report(data: Dict[str, List[Dict[str, str]]]) -> None:
    print("\nGenerating CSV report...")
    report_data = []
    summary_counts = {"allow": 0, "block": 0, "none": 0}

    for item in data.get("answer", []):
        domain = item.get("domain")
        verdict = item.get("verdict")
        report_data.append({"Domain": domain, "Verdict": verdict})
        if verdict in summary_counts:
            summary_counts[verdict] += 1

    df = pd.DataFrame(report_data)

    downloads_folder = Path.home() / "Downloads"
    csv_filename = downloads_folder / "verdict_report.csv"

    df.to_csv(csv_filename, columns=["Domain", "Verdict"], index=False)
    print(f"CSV created successfully: {csv_filename}")

    print("\nSummary:")
    for verdict, count in summary_counts.items():
        print(f"{verdict.capitalize()}: {count} domains")
    print("\nHave a nice day!")
