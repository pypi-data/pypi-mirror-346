import os
import requests
from typing import List, Dict, Optional


__all__ = [
    "BingSearch",
]


class BingSearch:
    """"""
    api_key: Optional[str] = None
    base_url: Optional[str] = "https://api.bing.microsoft.com/v7.0/search"

    def __init__(
            self,
            api_key: Optional[str] = None,
            key_name: Optional[str] = "BING_SEARCH_KEY",
    ):
        """"""
        self.set_api_key(api_key, key_name)

    def __call__(self, query: str, n_pages: Optional[int] = 1, *args, **kwargs):
        """"""
        web_pages = self.search_query(query=query, n_pages=n_pages)
        return web_pages

    def set_api_key(self, api_key: Optional[str] = None, key_name: Optional[str] = None):
        """"""
        if api_key is not None:
            self.api_key = api_key
        elif key_name is not None:
            self.api_key = os.getenv(key_name)

    def search_query(self, query: str, n_pages: Optional[int] = 1) -> List[Dict]:
        """"""
        headers = {"Ocp-Apim-Subscription-Key": self.api_key}
        params = {"q": query, "textDecorations": True, "textFormat": "HTML", 'setLang': 'zh-hans', 'mkt': 'zh-CN'}
        response = requests.get(self.base_url, headers=headers, params=params)
        response.raise_for_status()
        search_results = response.json()
        web_pages = search_results['webPages']['value'][:n_pages]
        return web_pages
