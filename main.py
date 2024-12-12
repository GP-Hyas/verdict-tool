import asyncio
from api.api import fetch_verdicts
from utils.helper import (
    fetch_filepath,
    fetch_urls,
    fetch_env_vars,
    fetch_header,
    fetch_file,
    fetch_report,
)


async def main():
    filepath = fetch_filepath()

    if filepath is not None:
        print(f"Using file path: {filepath}")

    env_vars = fetch_env_vars()
    key = env_vars["key"]
    client_id = env_vars["client_id"]

    base_url = "https://api.hyas.com"
    url = fetch_urls(base_url).verdict
    header = fetch_header(key)

    domains = fetch_file(filepath)

    print("\n...")
    print("Starting verdict run...")
    data = await fetch_verdicts(url, client_id, domains, header)

    print("...")
    fetch_report(data)


if __name__ == "__main__":
    asyncio.run(main())
