import os
import io
import requests
from PIL import Image
from typing import Annotated, Optional, Literal, List, Dict, Callable
from lumix.utils.utils import assemble_url
from lumix.utils.logger import LoggerMixin
from lumix.types.documents import SearchedImage
from .config.baidu import BAIDU_IMAGE_HEADERS


__all__ = [
    "BaiduImageSearch",
    "baidu_image_search"
]


class BaiduImageSearch(LoggerMixin):
    """"""
    base_url: str = "https://image.baidu.com/search/acjson"
    headers: Dict = BAIDU_IMAGE_HEADERS

    def __init__(
            self,
            api_key: Optional[str] = None,
            key_name: Optional[str] = "BAIDU_SEARCH",
            quality: Literal["high", "low"] = "low",
            logger: Optional[Callable] = None,
            verbose: Optional[bool] = False,
    ):
        """百度图片搜索工具

        Args:
            api_key: 百度图片搜索的API Key
            key_name: API Key的配置文件键名
            quality: 图片质量，可选"high"或"low"，默认"low"
            logger: 日志记录器
            verbose: 是否打印详细信息

        Examples:
            ```python
            import matplotlib.pyplot as plt
            from lumix.agent.tools import BaiduImageSearch

            baidu = BaiduImageSearch(verbose=True)
            images = baidu.search(query="cat")

            for i, image in enumerate(images):
                plt.imshow(image.image)
                plt.axis('off')
                plt.show()
            ```
        """
        self.quality = quality
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
        """
        Args:
            query:
            page:

        Returns:

        """
        return {
            "tn": "resultjson_com",
            "ipn": "rj",
            "ct": "201326592",
            "fp": "result",
            "word": query,
            "queryWord": query,
            "ie": "utf-8",
            "oe": "utf-8",
            "pn": str(int(page * 10)),
            "rn": "30",
            "gsm": "3c",
        }

    def fetch_images(self, metadata: List[Dict]) -> List[SearchedImage]:
        """"""
        images = []
        metadata = [item for item in metadata if item]
        for _metadata in metadata:
            if self.quality == "low":
                image_url = _metadata.get("image_url")
            elif self.quality == "high":
                image_url = _metadata.get("object_url")
            else:
                raise ValueError("Please set quality to 'low' or 'high'")

            try:
                response = requests.get(image_url, headers=self.headers)
                image = Image.open(io.BytesIO(response.content))
                images.append(SearchedImage(image=image, metadata=_metadata))
            except Exception as e:
                self.warning(msg=f"[{__class__.__name__}] Error fetching image from {image_url}: {str(e)}")

        self.info(msg=f"[{__class__.__name__}] Fetched {len(images)} / {len(metadata)} images")
        return images

    def fetch_metadata(self, data: Optional[Dict] = None) -> Dict:
        """"""
        mark = any([
            data is None,
            data.get("thumbURL") is None,
            data.get("replaceUrl") is None,
            data.get("fromPageTitle") is None,
        ])
        if mark:
            return dict()
        else:
            origin_url = data.get("replaceUrl")[0]
            return {
                "image_url": data.get("thumbURL"),
                "object_url": origin_url.get("ObjURL"),
                "from_url": origin_url.get("FromURL"),
                "from_title": data.get("fromPageTitle")
            }

    def search(self, query: str) -> List[SearchedImage]:
        """"""
        params = self.make_params(query)
        url = assemble_url(self.base_url, params)
        response = requests.get(url, headers=self.headers)
        metadata = list(map(self.fetch_metadata, response.json().get("data")))
        return self.fetch_images(metadata)


def baidu_image_search(
        query: Annotated[str, "The query to search for", True],
) -> List[Image.Image]:
    """ Search for a query on Baidu and return the results as a string.

    Args:
        query: The query to search for

    Returns:
        A string containing the search results

    Examples:
        ```python
        images = baidu_image_search("cat")
        ```
    """
    baidu = BaiduImageSearch(verbose=True)
    images = baidu.search(query=query)
    images = [image.image for image in images]
    return images
