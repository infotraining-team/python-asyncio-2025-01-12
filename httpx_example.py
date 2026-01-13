import asyncio
import httpx
from bs4 import BeautifulSoup as soup
from urllib.parse import urljoin, urlparse

class Crawler:
    def __init__(self, start_url):
        self.start_url = start_url

    def search_for_links(self, text, current_url):
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

    async def worker(self, url_to_get):
        pass

    async def fetch_website_text(self, url):
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            return response.text

    async def run(self):
        pass

async def main():
    crawler = Crawler("http://books.toscrape.com/")
    await crawler.run()
    print("--Success--")
    ## Use search to search for links, then scrap them
    ## Use Semaphore to limit access
    
asyncio.run(main())