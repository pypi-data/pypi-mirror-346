import unittest
import numpy as np
from lumix.embedding import PretrainedEmbedding


class TestMixin(unittest.TestCase):
    """"""

    def setUp(self) -> None:
        self.name_or_path = "/home/models/BAAI/bge-small-zh-v1.5"
        self.embedding = PretrainedEmbedding(
            name_or_path=self.name_or_path,
            batch_size=2,
            normalize_embeddings=True,
            verbose=True,
        )

    def test_similarity_matrix(self):
        """"""
        text = ["你好", "你是谁", "你这里有点好看", "如何打车去南京路", "我想吃西瓜", "今天去做点什么呢"]
        cosine_matrix = self.embedding.similarity_matrix(source=text, target=text)
        print(cosine_matrix.shape)

    def test_similarity_matrix_topn(self):
        """"""
        source = ["你好", "hello"]
        target = ["你好", "你是谁", "here"]
        matched = self.embedding.filter(source=source, target=target, top_n=1, threshold=0.6)
        print(matched)

    def test_top_n_idx(self):
        """"""
        target = [
            "谁更容易避免损失，谁的责任更大，谁更需要主动采取措施防止问题发声",
            "在这个事件中，女子的行为绝对责任占大头",
            "首先，网约车迟到并不是小概率事件，偶尔发生是可预判的",
            "而且网约车是无法知道乘客去机场剩余多少时间值机，也不知道你坐飞机去做什么",
            "换句话说，网约车的责任和平时迟到八分钟没有区别",
        ]
        query = ["谁的责任占大头？", "网约车是否知道乘客去机场剩余多少时间值机？"]
        match = self.embedding.filter(
            source=query,
            target=target,
            top_n=2,
        )
        print(match)
