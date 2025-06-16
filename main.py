# server.py
from facts.main import COUNTRIES_LOWER as COUNTRIES
from server.main import mcp
from scraping.main import get_content, parse_factbook_data
from facts.prompts import PROMPTS  # noqa: F401


@mcp.tool()
def get_cia_facts(country: str) -> object:
    # Todo: return type
    """Get the facts from the CIA World Factbook"""
    if not country:
        return "Please provide a country name."
    try:
        if country.lower() in COUNTRIES:
            slug = country.lower().replace(" ", "-")

            # Construct the CIA World Factbook URL
            url = f"https://www.cia.gov/the-world-factbook/countries/{slug}/"
            content = get_content(url)
            facts = parse_factbook_data(content)
            return facts
    except Exception as e:
        return e


# Add a dynamic country resource
@mcp.resource("country://{name}")
def get_country(name: str) -> str:
    """Check that a country exists"""
    if name.lower() in COUNTRIES:
        return f"{name} is a valid country."
    else:
        return "Not a valid country."


# Add a dynamic country facts resource
@mcp.resource("country://{name}/facts")
def get_country_facts(name: str) -> str:
    """Talk about a country"""
    facts = get_cia_facts(name)
    return f"Facts about {name}: {facts}"
