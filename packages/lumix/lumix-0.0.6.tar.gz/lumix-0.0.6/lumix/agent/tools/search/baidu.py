import os
import time
import base64
import random
import chardet
import hashlib
import requests
from bs4 import BeautifulSoup, Tag
from typing import Annotated, Optional, List, Dict, Callable

from lumix.utils.utils import assemble_url
from lumix.utils.logger import LoggerMixin
from lumix.utils.string import drop_multi_mark
from lumix.types.documents import DocumentPage
from .config.baidu import BAIDU_HEADERS, NORMAL_HEADERS


__all__ = [
    "BaiduSearch",
    "baidu_search"
]


class BaiduSearch(LoggerMixin):
    """"""
    base_url: str = "https://www.baidu.com/s"
    headers: Dict = BAIDU_HEADERS

    def __init__(
            self,
            api_key: Optional[str] = None,
            key_name: Optional[str] = "BAIDU_SEARCH",
            logger: Optional[Callable] = None,
            verbose: Optional[bool] = False,
    ):
        """百度搜索工具

        Args:
            api_key:
            key_name:
            logger:
            verbose:
        """
        self.logger = logger
        self.verbose = verbose
        self.set_api_key(api_key, key_name)

    def __call__(self, *args, **kwargs):
        """"""

    def set_api_key(self, api_key: Optional[str] = None, key_name: Optional[str] = None):
        """"""
        if api_key is not None:
            self.headers["Cookie"] = api_key
        elif key_name is not None and os.getenv(key_name):
            self.headers["Cookie"] = os.getenv(key_name)
        else:
            raise ValueError("Please set api_key or key_name")

    def make_params(self, query: str, page: int = 0) -> dict:
        """"""
        random_str = f"{time.time()}{random.random()}".encode()
        rsv_pq = hashlib.md5(random_str).hexdigest()

        timestamp = int(time.time() * 1000)
        random_part = base64.b64encode(
            hashlib.sha1(str(random.random()).encode()).digest()
        ).decode()[:8]

        return {
            "ie": "utf-8",
            "tn": "baidu",
            "wd": query,
            "base_query": query,
            "oq": query,
            "pn": str(int(page * 10)),
            "rsv_pq": rsv_pq,
            "rsv_t": f"{timestamp}{random_part}",
        }

    def parse_metadata(self, div: Tag):
        """"""
        url = div.find(name="a").get("href")
        title = div.find(name="a").text
        span = div.select('span[class^="content-right_"]')
        abstract = span[0].text if len(span) > 0 else ""
        return {"url": url, "title": title, "abstract": abstract}

    def parse_html(self, soup: BeautifulSoup) -> List[Dict]:
        """"""
        div_c_container = soup.select('div[class="c-container"]')
        metadata = list(map(self.parse_metadata, div_c_container))
        return metadata

    def web_content(self, url) -> str:
        """"""
        try:
            response = requests.get(url, headers=NORMAL_HEADERS)
            detected = chardet.detect(response.content)
            soup = BeautifulSoup(response.content, from_encoding=detected['encoding'], features="html.parser")
            return soup.text
        except Exception as e:
            self.warning(msg=f"[{__class__.__name__}] URL: {url}, Error: {str(e)}")
            return ""

    def search(self, query: str, pages: Optional[int] = 10) -> List[DocumentPage]:
        """"""
        metadata = []
        page = 0
        while len(metadata) <= pages:
            params = self.make_params(query, page=page)
            url = assemble_url(self.base_url, params)
            response = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(response.text, features="html.parser")
            _metadata = self.parse_html(soup)
            metadata.extend(_metadata)
            page += 1
            if len(_metadata) == 0:
                break
        metadata = metadata[:pages]
        self.info(msg=f"[{__class__.__name__}] Find {len(metadata)} pages")
        web_data = []
        for item in metadata:
            page_content = self.web_content(item.get("url"))
            web_data.append(DocumentPage(page_content, metadata=item))
        return web_data


def baidu_search(
        query: Annotated[str, "The query to search for", True],
        pages: Annotated[Optional[int], "Number of pages to search, and you can", False] = 5,
) -> str:
    """ Search for a query on Baidu and return the results as a string.

    Args:
        query: The query to search for
        pages:
            Number of pages to search, You can search multiple pages at the
            same time to ensure the information is accurate. The default is 10 pages.

    Returns:
        A string containing the search results
    """
    baidu = BaiduSearch(verbose=True)
    page_data = baidu.search(query=query, pages=pages)
    for page in page_data:
        page.page_content = drop_multi_mark(text=page.page_content)
    content = str([page.model_dump() for page in page_data])
    return content
