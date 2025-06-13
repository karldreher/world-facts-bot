import trafilatura
from requests import get, Response


def get_content(url: str) -> Response:
    # Set headers to mimic a browser request
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }

    # Make the request with timeout
    response = get(url, headers=headers, timeout=10)
    return response


def parse_factbook_data(downloaded_content: Response) -> str | None:
    """Parse CIA World Factbook page and extract key information"""
    content = trafilatura.extract(downloaded_content.text)
    if not content:
        return None
    # This text will usually appear at the start.  We should remove it.
    content = (
        content.replace("Introduction", "")
        .replace(
            "Visit the Definitions and Notes page to view a description of each topic.",
            "",
        )
        .strip()
    )
    return content
