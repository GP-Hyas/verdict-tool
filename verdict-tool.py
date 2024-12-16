import asyncio
from api.hyas_api import APIClient
from utils.helper import (
    get_filepath,
    fetch_domain_verdict,
    read_file,
    generate_report,
)


async def main():
    filepath = get_filepath()

    if filepath is not None:
        print(f"Using file path: {filepath}")

    domains = read_file(filepath)

    base_url = "https://api.hyas.com"

    print("\n...")
    print("Starting verdict run...")
    results = {"answer": []}
    total_domains = len(domains)

    async with APIClient(base_url) as client:
        for i, domain in enumerate(domains, start=1):
            print(f"[{i}/{total_domains}] Processing: {domain}")
            result = await fetch_domain_verdict(client, domain)
            results["answer"].append(result)

    print("\n...")
    generate_report(results)


if __name__ == "__main__":
    asyncio.run(main())
