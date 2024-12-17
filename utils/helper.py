import sys
import pandas as pd
from pathlib import Path
from typing import List, Dict, Any
from utils.logger_config import logger
from api.hyas_api import APIClient


async def fetch_domain_verdict(client: APIClient, domain: str) -> Dict[str, Any]:
    """
    Fetch the verdict fro a given domain using the API client.

    Args:
        client (APIClient): The API client instance.
        domain (str): The domain to query.

    Returns:
        Dict[str, str]: A dictionary containing the domain and its verdict
    """
    try:
        response = await client.verdict(domain)
        verdict = response.get("verdict_status", "error")

        logger.info(f"Processed: {domain} - Verdict: {verdict}")
        return {"domain": domain, "verdict": verdict}

    except Exception as e:
        logger.error(f"Error processing {domain}: {e}")
        return {"domain": domain, "verdict": "error"}


def get_filepath() -> str:
    """
    Prompt the user for a valid file path.

    Returns:
        str: The validated file path as a string.

    Raises:
        SystemExit: Exits if the user fails to provide a valid path after retries.
    """
    retries = 3
    while retries > 0:
        filepath = input("\nEnter the file path to your txt or csv: ").strip()
        path = Path(filepath).expanduser().resolve()

        if path.exists():
            if path.suffix.lower() in [".txt", ".csv"]:
                logger.info("File path is valid.")
                return str(path)
            else:
                logger.warning("Invalid file type. Expected txt or csv.")
        else:
            logger.warning("Path does not exist.")

        retries -= 1
        logger.warning(f"Retries left: {retries}. Please try again.")
        if retries == 0:
            logger.error("Exceeded maximum retries. Exiting...")
            sys.exit(1)


def read_file(filepath: str) -> List[str]:
    """
    Read lines from a file, ensuring no duplicates or empty lines.

    Args:
        filepath (str): The path to the input file.

    Returns:
        List[str]: A list of unique non-empty lines.

    Raises:
        SystemExit: Exits if the file cannot be read or is empty.
    """
    try:
        path = Path(filepath)
        if path.stat().st_size == 0:
            logger.error("Error: The input file is empty.")
            sys.exit(1)

        with path.open("r", encoding="utf-8") as file:
            lines = {line.strip() for line in file if line.strip()}

        if not lines:
            logger.error("Error: The input file contains no valid entries.")
            sys.exit(1)

        logger.info(f"Successfully read {len(lines)} unique lines from file.")
        return list(lines)

    except Exception as e:
        logger.exception(f"An error occurred while reading the file: {e}")
        sys.exit(1)


def _display_summary(results: List[Dict[str, Any]]) -> None:
    """
    Generate a summary of report results to the screen.

    Args:
        results (List[Dict[str, Any]]): List of processed domain results.
    """
    print("\nSummary Report:")
    verdict_counts = {"allow": 0, "block": 0, "suspicious": 0, "none": 0, "error": 0}

    for item in results:
        # Use the correct key 'Verdict' with case normalization
        verdict = item.get("Verdict", "error").strip().lower()
        if verdict in verdict_counts:
            verdict_counts[verdict] += 1
        else:
            logger.warning(f"Unexpected verdict encountered: {verdict}")
            verdict_counts["error"] += 1

    print(f"\n{'Verdict':<12} | {'Count':<5}")
    print("-" * 20)
    for verdict, count in verdict_counts.items():
        print(f"{verdict.capitalize():<12} | {count:<5}")
    print("\nReport saved successfully. Have a nice day!\n")


def generate_report(data: Dict[str, List[Dict[str, str]]]) -> None:
    """
    Generate a CSV report from fetched data and print a summary.

    Args:
        data (Dict[str, List[Dict[str, str]]]): The fetched domain data.
    """
    logger.info("Generating CSV report.")
    report_data = []

    for item in data.get("answer", []):
        domain = item.get("domain", "unknown")
        verdict = item.get("verdict", "none").lower()
        report_data.append({"Domain": domain, "Verdict": verdict})

    # Create DataFrame
    df = pd.DataFrame(report_data)

    # Save report to the user's Downloads folder
    downloads_folder = Path.home() / "Downloads"
    csv_filename = downloads_folder / "verdict_report.csv"

    try:
        df.to_csv(csv_filename, columns=["Domain", "Verdict"], index=False)
        logger.info(f"CSV report created successfully: {csv_filename}")
    except Exception as e:
        logger.exception(f"Failed to save the report: {e}")
        sys.exit(1)

    # Print the summary
    _display_summary(report_data)  # Pass processed list directly
