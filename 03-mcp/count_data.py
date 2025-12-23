import requests

def download_page_markdown(url: str) -> str:
    """Download the content of any web page as markdown using Jina Reader (r.jina.ai)."""
    proxy_url = f"https://r.jina.ai/{url}"
    response = requests.get(proxy_url)
    response.raise_for_status()
    return response.text

if __name__ == "__main__":
    url = "https://datatalks.club"
    content = download_page_markdown(url)
    count = content.lower().count("data")
    print(f'The word "data" appears {count} times on {url}.')
