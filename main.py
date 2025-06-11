# server.py
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("World Facts Bot")


# Add an addition tool
@mcp.tool()
# Todo: object type
def get_cia_facts(country: str) -> object:
    """Get the facts from the CIA World Factbook"""
    # do something with https://www.cia.gov/the-world-factbook/countries/
    return {}


# Add a dynamic country resource
@mcp.resource("country://{name}")
def get_country(name: str) -> str:
    """Get a personalized greeting"""
    facts = get_cia_facts(name)
    return f"Facts about {name}: {facts}"
