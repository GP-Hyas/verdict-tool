import os
import sys
import readline
import pandas as pd
from dotenv import load_dotenv
from collections import namedtuple
from pathlib import Path


def fetch_env_vars() -> dict[str, str]:
    env_path = Path(__file__).resolve().parent.parent / ".env"

    if not env_path.exists():
        print(f"Error: .env file not found at {env_path}")
        sys.exit(1)

    load_dotenv(dotenv_path=env_path)

    api_key = os.getenv("APIKEY")
    client_id = os.getenv("CLIENTID")

    if not api_key or not client_id:
        print("Error: Missing APIKEY or CLIENTID in the environment variables.")
        sys.exit(1)

    return {"key": api_key, "client_id": client_id}


def complete_path(text, state):
    path = Path(text).expanduser()
    directory = path.parent if path.parent.exists() else Path(".")
    basename = path.name

    matches = [
        str(match) for match in directory.iterdir() if match.name.startswith(basename)
    ]

    return matches[state] if state < len(matches) else None


def fetch_urls(base_url: str):
    Urls = namedtuple("Urls", ["verdict"])
    return Urls(verdict=base_url + "/decision/verdict")


def fetch_header(key: str) -> dict[str, str]:
    if not key:
        print("Error: API key is missing.")
        sys.exit(1)
    return {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-API-Key": key,
    }


def fetch_filepath() -> str:
    readline.set_completer(complete_path)
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


def fetch_file(filepath: str) -> list[str]:
    try:
        with open(filepath, "r") as file:
            lines = [line.strip() for line in file if line.strip()]

        if not lines:
            print("Error: The input file empty.")
            sys.exit(1)

        return list(set(lines))
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        sys.exit(1)


def fetch_report(data: dict[str, list]) -> None:
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
