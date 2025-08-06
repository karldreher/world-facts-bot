# server.py

from countries.main import COUNTRIES_LOWER, mcp as countries
from scraping.main import get_content, parse_factbook_data

from fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("World Facts Bot")
async def setup():
    """Setup function to initialize the MCP server."""
    await mcp.import_server(countries)


def _get_cia_facts_impl(country: str) -> object:
    if not country:
        return "Please provide a country name."
    try:
        if country.lower() in COUNTRIES_LOWER:
            slug = country.lower().replace(" ", "-")

            # Construct the CIA World Factbook URL
            url = f"https://www.cia.gov/the-world-factbook/countries/{slug}/"
            content = get_content(url)
            facts = parse_factbook_data(content)
            return facts
    except Exception as e:
        return e


@mcp.tool()
def get_cia_facts(country: str) -> object:
    """Get the facts from the CIA World Factbook"""
    return _get_cia_facts_impl(country)


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
def get_country_facts(name: str) -> str:
    """Talk about a country"""
    facts = _get_cia_facts_impl(name)
    return f"Facts about {name}: {facts}"

if __name__ == "__main__":
    mcp.run()
