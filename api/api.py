import aiohttp
import asyncio


async def fetch_verdict(
    session: aiohttp.ClientSession,
    url: str,
    client_id: str,
    domain: str,
    header: dict[str, str],
) -> dict[str, str]:
    payload = {"clientId": client_id, "domain": domain}
    try:
        async with session.post(url, json=payload, headers=header) as response:
            response.raise_for_status()
            data = await response.json()
            verdict = data.get("verdict_status")
            print(f"Success: {domain} - Verdict: {verdict}")
            return {"domain": domain, "verdict": verdict} if verdict else None
    except aiohttp.ClientError as e:
        print(f"Error: {domain} - {e}")
    except asyncio.TimeoutError:
        print(f"Timeout: {domain}")
    return None


async def fetch_verdicts(
    url: str, client_id: str, domains: list[str], header: dict[str, str]
) -> dict[str, list]:
    results = {"answer": []}
    total_domains = len(domains)

    async with aiohttp.ClientSession() as session:
        tasks = []
        for i, domain in enumerate(domains, start=1):
            print(f"[{i}/{total_domains}] Processing: {domain}")
            tasks.append(fetch_verdict(session, url, client_id, domain, header))

        response = await asyncio.gather(*tasks)

        results["answer"] = [response for response in response if response]
        return results
