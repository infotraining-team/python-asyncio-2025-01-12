import asyncio
import httpx
from bs4 import BeautifulSoup as soup
from urllib.parse import urljoin, urlparse

async def fetch_website_text(url):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.text

async def main():
    text = await fetch_website_text("http://books.toscrape.com/")
    print("--Success--")
    ## Use search to search for links, then scrap them
    ## Use Semaphore to limit access
    print(text)

def search_for_links(text, current_url):
    s = soup(text, 'html.parser')
    links = []
    for anchor in soup.find_all('a', href=True):
        href = anchor['href']
        # Convert relative URLs (e.g., /about) to absolute URLs
        full_url = urljoin(current_url, href)
        parsed_url = urlparse(full_url)

        # Filter: Only keep HTTP/HTTPS links on the same domain
        if parsed_url.scheme in ('http', 'https') and parsed_url.netloc == self.base_domain:
            # Remove fragments (#section) to avoid duplicate crawling
            clean_url = full_url.split('#')[0]
            links.add(clean_url)

    return links

asyncio.run(main())