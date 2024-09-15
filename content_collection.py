from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_community.document_transformers import Html2TextTransformer
from langchain_core.documents import Document
import os
import pandas as pd
from serpapi import GoogleSearch
from typing import List

# Different Data manipulation involving
# scraping data from external sources and converting a document object
class ChromiumLoader(AsyncChromiumLoader):
    async def load(self):
        # Fetch data from urls and store in a list
        raw_text = [await self.ascrape_playwright(url) for url in self.urls]
        
        # Return document obbject from raw text
        return [Document(page_content=text) for text in raw_text]
    

async def get_html_content_from_urls(
    df: pd.DataFrame,
    number_of_urls: int=3,
    url_column: str="link") -> List[Document]:
    
    urls = df[url_column].values[:number_of_urls].tolist()
    
    if isinstance(urls, str):
        urls = [urls]
    
    urls = [url for url in urls if url != ""]
    
    urls = list(set(urls))
    
    if len(urls) == 0:
        raise ValueError("No URLs Found!")

    loader = ChromiumLoader(urls)
    docs = await loader.load()
    return docs

def extract_text_from_webpages(documents: List[Document]):
    html2text = Html2TextTransformer()
    return html2text.transform_documents(documents)

async def collect_serp_data_and_extract_text_from_webpages(
    topic: str) -> List[Document]:
    
    search = GoogleSearch(
        {
            "q": topic,
            "location": "Austin,Texas",
            "api_key": os.environ["SERPAPI_API_KEY"],
        }
    )
    # Get the results:
    result = search.get_dict()

    # Put the results in a Pandas DataFrame:
    serp_results = pd.DataFrame(result["organic_results"])

    # Extract the html content from the URLs:
    html_documents = await get_html_content_from_urls(serp_results)

    # Extract the text from the URLs:
    text_documents = extract_text_from_webpages(html_documents)

    return text_documents