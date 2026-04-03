# server.py

import asyncio

import cache
from countries.main import COUNTRIES_LOWER, mcp as countries
from scraping.main import get_content, parse_factbook_data

from fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("World Facts Bot")
mcp.mount(countries)


async def _get_cia_facts_impl(country: str) -> str:
    if not country:
        return "Please provide a country name."
    if country.lower() not in COUNTRIES_LOWER:
        return f"{country!r} is not a recognized country."
    try:
        slug = country.lower().replace(" ", "-")
        cached = await asyncio.to_thread(cache.get, slug)
        if cached:
            return cached
        # Construct the CIA World Factbook URL
        url = f"https://www.cia.gov/the-world-factbook/countries/{slug}/"
        content = await asyncio.to_thread(get_content, url)
        facts = parse_factbook_data(content)
        if facts:
            await asyncio.to_thread(cache.put, slug, facts)
        return facts or "No facts found."
    except Exception as e:
        return str(e)


@mcp.tool()
async def get_cia_facts(country: str) -> str:
    """Get the facts from the CIA World Factbook"""
    return await _get_cia_facts_impl(country)


# Add a dynamic country resource
@mcp.resource("country://{name}")
def get_country(name: str) -> str:
    """Check that a country exists"""
    if name.lower() in COUNTRIES_LOWER:
        return f"{name} is a valid country."
    else:
        return "Not a valid country."


# Add a dynamic country facts resource
@mcp.resource("country://{name}/facts")
async def get_country_facts(name: str) -> str:
    """Talk about a country"""
    facts = await _get_cia_facts_impl(name)
    return f"Facts about {name}: {facts}"

if __name__ == "__main__":
    mcp.run()
