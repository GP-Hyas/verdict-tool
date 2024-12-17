import asyncio
from tqdm import tqdm
from asyncio import TaskGroup
from api.hyas_api import APIClient
from utils.logger_config import logger
from utils.helper import (
    get_filepath,
    fetch_domain_verdict,
    read_file,
    generate_report,
)


async def process_domains(domains, base_url):
    """
    Process a list of domains to fetch verdicts asynchronously.

    Args:
        domains (List[str]): List of domains to process.
        base_url (str): The base URL for the API.

    Returns:
        List[Dict[str, str]]: A list of domain verdict results.
    """
    results = []
    progress = tqdm(
        total=len(domains), desc="Processing domains", position=0, dynamic_ncols=True
    )

    async def fetch_and_store_result(client, domain):
        """Fetch verdict and append result, then update the progress bar."""
        result = await fetch_domain_verdict(client, domain)
        results.append(result)
        progress.update(1)  # Update progress bar for each completed task

    try:
        async with APIClient(base_url) as client:
            async with TaskGroup() as tg:
                for domain in domains:
                    tg.create_task(fetch_and_store_result(client, domain))
    except Exception as e:
        logger.exception(f"An error occurred during domain processing: {e}")
    finally:
        progress.close()  # Ensure progress bar is closed properly

    return results


async def main():
    """
    Main function to orchestrate the domain verdict tool
    """
    try:
        filepath = get_filepath()
        logger.info(f"Using file path: {filepath}")

        domains = read_file(filepath)
        total_domains = len(domains)
        logger.info(f"Loaded {total_domains} domains for processing.")

        base_url = "https://api.hyas.com"

        print("\nStarting verdict run...")
        results = await process_domains(domains, base_url)

        print("\nGenerating report...")
        generate_report({"answer": results})
        logger.info("Processing complete. Report generated successfully.")

    except KeyboardInterrupt:
        logger.warning("Process interrupted by user.")
    except Exception as e:
        logger.exception(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logger.critical(f"Critical error during execution: {e}")
