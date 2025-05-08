import unittest
from lumix.embedding import OpenAIEmbedding


class TestOpenAIEmbedding(unittest.TestCase):
    """"""
    def setUp(self):
        self.base_url = "http://172.16.11.159:8000"

    def test_embedding(self):
        embedding = OpenAIEmbedding(base_url=self.base_url, api_key="EMPTY", model="bge-m3")
        data = embedding.embedding(["你好"])
        print(data.to_numpy().shape)
