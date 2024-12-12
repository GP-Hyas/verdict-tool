from dotenv import load_dotenv
from collections import namedtuple
from pathlib import Path
import os
import sys
import pandas as pd


def fetch_env_vars() -> dict[str, str]:
    load_dotenv()
    return {
        "key": os.getenv("APIKEY"),
        "client_id": os.getenv("CLIENTID"),
    }


def fetch_urls(base_url: str):
    Urls = namedtuple("Urls", ["verdict"])
    return Urls(verdict=base_url + "/decision/verdict")


def fetch_header(key: str) -> dict[str, str]:
    return {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-API-Key": key,
    }


def fetch_payload(clientId: str, domain: str) -> dict[str, any]:
    return {"clientId": clientId, "domain": domain}


def fetch_filepath() -> str:
    while True:
        filepath = input("Enter the file path to your txt or csv: ").strip()

        if os.path.exists(filepath):
            _, ext = os.path.splitext(filepath)
            if ext.lower() in ["txt", "csv"]:
                print("File path is valid.")
                return filepath
            else:
                print("Invalid file type. Expected txt or csv.")
        else:
            user_choice = (
                input(
                    "Path does not exist. Enter 'q' to quit or any other key to try again: "
                )
                .strip()
                .lower()
            )
            if user_choice == "q":
                print("Exiting...")
                sys.exit(1)
            else:
                continue


def fetch_file(filepath: str) -> tuple[str]:
    try:
        with open(filepath, "r") as file:
            lines = [line.strip() for line in file]

        dedup_lines = tuple(set(lines))
        return dedup_lines

    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)


def fetch_report(data: dict[str, list]) -> None:
    report_data = []
    for item in data.get("answer", []):
        report_data.append(
            {
                "domain": item.get("domain"),
                "verdict": item.get("verdict"),
            }
        )

    df = pd.DataFrame(report_data)

    downloads_folder = Path.home() / "Downloads"
    csv_filename = downloads_folder / "verdict_report.csv"

    df.to_csv(csv_filename, columns=["Domain", "Verdict"], index=False)
    print(f"CSV created successfully: {csv_filename}")
