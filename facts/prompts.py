from mcp.server.fastmcp.prompts import base

from server.main import mcp
from .main import COUNTRIES

@mcp.prompt()
def list_countries_prompt() -> list[base.Message]:
    """Prompt for listing available countries"""
    return [
        base.UserMessage("What are the available countries in the CIA World Factbook? Please list them."),
        # TODO: Is COUNTRIES a tool? 
        base.AssistantMessage("Here is the list of countries available in the CIA World Factbook:\n" + "\n".join(COUNTRIES))
    ]



PROMPTS = [list_countries_prompt]
