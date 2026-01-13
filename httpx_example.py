import asyncio
import httpx
from bs4 import BeautifulSoup as soup
from urllib.parse import urljoin, urlparse
from collections import deque

class Crawler:
    def __init__(self, start_url, max_pages=100, max_concurrency=10):
        self.max_pages = max_pages
        self.sem = asyncio.Semaphore(max_concurrency)
        self.start_url = start_url
        self.to_visit = deque()
        self.lock = asyncio.Lock()
        self.visited = set()
        self.base_domain = urlparse(start_url).netloc

    def search_for_links(self, text, current_url):
        s = soup(text, 'html.parser')
        links = []
        for anchor in s.find_all('a', href=True):
            href = anchor['href']
            # Convert relative URLs (e.g., /about) to absolute URLs
            full_url = urljoin(current_url, href)
            parsed_url = urlparse(full_url)

            # Filter: Only keep HTTP/HTTPS links on the same domain
            if parsed_url.scheme in ('http', 'https') and parsed_url.netloc == self.base_domain:
                # Remove fragments (#section) to avoid duplicate crawling
                clean_url = full_url.split('#')[0]
                links.append(clean_url)
        return links

    async def runner(self):
        while True:
            if len(self.visited) >= self.max_pages:
                return
            async with self.sem:
                while True:
                    async with self.lock:
                        if self.to_visit:
                            new_url = self.to_visit.popleft()
                            break
                    await asyncio.sleep(0.1)
                await self.worker(new_url)


    async def worker(self, url_to_get):
        print(f"Crawling {url_to_get}")
        self.visited.add(url_to_get)
        html = await self.fetch_website_text(url_to_get)
        if html:
            links = self.search_for_links(html, url_to_get)
            for link in links:
                async with self.lock:
                    if link not in self.visited and link not in self.to_visit:
                        self.to_visit.append(link)


    async def fetch_website_text(self, url):
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            return response.text

    async def run(self):
        self.to_visit.append(self.start_url)
        workers = [asyncio.create_task(self.runner()) for _ in range(50)]
        await asyncio.gather(*workers)

async def main():
    crawler = Crawler("http://books.toscrape.com/")
    await crawler.run()
    print("--Success--")
    ## Use search to search for links, then scrap them
    ## Use Semaphore to limit access

asyncio.run(main())