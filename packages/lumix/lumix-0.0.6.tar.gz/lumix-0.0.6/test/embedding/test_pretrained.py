import unittest
from lumix.embedding import PretrainedEmbedding


class TestPretrainedEmbedding(unittest.TestCase):
    """"""
    def setUp(self) -> None:
        self.name_or_path = "/home/models/BAAI/bge-small-zh-v1.5"
        self.embedding = PretrainedEmbedding(
            name_or_path=self.name_or_path,
            batch_size=2,
            normalize_embeddings=True,
            verbose=True,
        )

    def test_pretrained_embedding(self):
        """"""
        text = ["你好", "你是谁", "你这里有点好看", "如何打车去南京路", "我想吃西瓜", "今天去做点什么呢"]
        data = self.embedding.embedding(text=text)
        print(data.to_numpy().shape)
