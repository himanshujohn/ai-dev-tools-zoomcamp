from fastmcp import FastMCP
import requests

mcp = FastMCP("Demo 🚀")

@mcp.tool
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.tool
def download_page_markdown(url: str) -> str:
    """Download the content of any web page as markdown using Jina Reader (r.jina.ai)."""
    proxy_url = f"https://r.jina.ai/{url}"
    response = requests.get(proxy_url)
    response.raise_for_status()
    return response.text


@mcp.tool
def count_word_data(url: str) -> int:
    """Count how many times the word 'data' appears on the given web page using Jina Reader (r.jina.ai)."""
    proxy_url = f"https://r.jina.ai/{url}"
    response = requests.get(proxy_url)
    response.raise_for_status()
    content = response.text.lower()
    return content.count("data")

if __name__ == "__main__":
    mcp.run()