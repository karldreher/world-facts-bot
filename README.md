# Deprecation Notice!  
I cannot say this better than CIA said themselves.  I feel this might be best with an archive link...

https://web.archive.org/web/20260402003608/https://www.cia.gov/stories/story/spotlighting-the-world-factbook-as-we-bid-a-fond-farewell/

> One of CIA’s oldest and most recognizable intelligence publications, The World Factbook, has sunset. The World Factbook served the Intelligence Community and the general public as a longstanding, one-stop basic reference about countries and communities around the globe. 
> ...
> The World Factbook appealed to researchers, news organizations, teachers, students, and international travelers. 

This speaks volumes.  🤷

# world-facts-bot

An MCP server that provides CIA World Factbook data for countries worldwide.

## Prerequisites

- Python 3.12+
- [UV](https://docs.astral.sh/uv/getting-started/installation/)

## Setup

```bash
uv sync
```

## Running

### MCP dev mode (interactive inspector)

```bash
uv run mcp dev main.py
```

### Stdio transport (for MCP client config)

```bash
uv run python main.py
```

### MCP client configuration

Add this to your MCP client config (e.g. `claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "world-facts-bot": {
      "command": "uv",
      "args": ["run", "python", "main.py"],
      "cwd": "/path/to/world-facts-bot"
    }
  }
}
```

## Development

### Run tests

```bash
uv run pytest
```

### Lint and format

```bash
uv run ruff check .
uv run ruff format .
```

### Add a dependency

```bash
uv add <package>           # runtime dependency
uv add --dev <package>     # dev-only dependency
```

After adding dependencies, the lockfile is updated automatically. Commit both `pyproject.toml` and `uv.lock`.

## Available tools

| Tool | Description |
|---|---|
| `list_countries` | Returns all 258 countries/territories available in the CIA World Factbook |
| `get_cia_facts` | Fetches and returns the full CIA World Factbook entry for a given country |

## Caching

Fetched country facts are cached in memory for the lifetime of the server process. Restarting the server clears the cache.
