from scraipe.async_classes import IAsyncScraper
from scraipe import ScrapeResult
from aiohttp import ClientSession
import asyncio
from collections import namedtuple
ArticleData = namedtuple("ArticleData", ["id","title","description","text"])
import re
from scraipe.defaults import TextScraper

class CertUaScraper(IAsyncScraper):
    """
    Scrapes article content from https://cert.gov.ua using its API.
    
    Compatible with target API on 4/7/2025.
    """
    
    def __init__(self, headers: dict = None):
        """
        Initializes the CertUaScraper with optional headers.
        """
        self.headers = headers if headers else {
            'User-Agent': TextScraper.DEFAULT_USER_AGENT
        }
    
    def get_expected_link_format(self):
        return r"https://cert.gov.ua/article/\d+"

    async def get_article_data(self, article_id: int) -> ArticleData:
        url = f"https://cert.gov.ua/api/articles/byId?id={article_id}&lang=uk"
        headers = {'Cache-Control': 'no-cache', 'Pragma': 'no-cache'}
        async with ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                content = await response.read()
        import xml.etree.ElementTree as ET
        root = ET.fromstring(content)
        data = {
            'id': root.find('id').text if root.find('id') is not None else None,
            'title': root.find('title').text if root.find('title') is not None else None,
            'description': root.find('description').text if root.find('description') is not None else None,
            'text': root.find('text').text if root.find('text') is not None else None
        }
        
        return ArticleData(**data)
    
    async def async_scrape(self, link:str) -> ScrapeResult:
        """
        Scrapes the content of a given URL or article ID.
        The URL should be in the format: https://cert.gov.ua/article/6282069.
        The article ID can also be provided directly as a numeric string.
        """
        # Can accept either an article ID or a URL
        if link.isnumeric():
            article_id = int(link)
        else:
            # Extract article ID from the URL
            match = re.search(r'/article/(\d+)', link)
            if match:
                article_id = int(match.group(1))
            else:
                return ScrapeResult.fail(link,"Invalid URL or article ID")
        
        try:
            article_data = await self.get_article_data(article_id)
        except Exception as e:
            return ScrapeResult.fail(f"Failed to get article data: {e}")
        else:
            content:str = article_data.text                
            metadata = article_data._asdict()
            del metadata["text"]
            if content is None:
                return ScrapeResult.fail(link, "Failed to retrieve content")
            return ScrapeResult.succeed(link, content, metadata=metadata)            
