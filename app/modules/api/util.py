"""util.py
================================================
Collection of utilities to use in an application
"""

from typing import Optional
import httpx


def GET_page(url: str, api_key: Optional[str] = None) -> str:
    """Send a GET request to a URL with optional API key authentication.

    Args:
        url: The URL to send the request to
        api_key: Optional API key for authentication

    Returns:
        str: The response content as text

    Raises:
        httpx.HTTPError: If the request fails
    """
    if api_key is None:
        resp = httpx.get(f"{url}")
    else:
        params = {"X-Api-Key": api_key}
        resp = httpx.get(f"{url}", params)

    return resp.text
