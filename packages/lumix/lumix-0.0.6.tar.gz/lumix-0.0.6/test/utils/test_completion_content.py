import unittest
from lumix.agent.tools.search import baidu_search
from lumix.utils.string import drop_multi_mark
from lumix.utils.completion import TransCompletionContent


class TestCompletionContent(unittest.TestCase):
    def test_trans_completion_content(self):
        """"""
        trans_content = TransCompletionContent(
            role="assistant", content="Hello World", model="chat", finish_reason="stop")
        completion = trans_content.completion()
        print(completion)

    def test_trans_chunk_content(self):
        """"""
        trans_content = TransCompletionContent(
            role="assistant", content="Hello World", model="chat", finish_reason="stop")
        chunk = trans_content.completion_chunk()
        print(chunk)

    def test_ali_chunk(self):
        """"""
        trans_content = TransCompletionContent(
            role="assistant", content="Hello World", model="chat", finish_reason=None)
        chunk = trans_content.ali_chunk(delta=True)
        print(chunk)


class TestUtils(unittest.TestCase):
    """"""
    def test_drop_mark(self):
        """"""
        text = "欲知更加准确的天气预报需随时关注短期天气预报和最新预报信息更新。\n\n\n\n\n\n\n\n\n今天\n03/21\n\n\n\n\n晴\n\n26/12℃\n\n\n\n\n\n\n\n\n\n西南风4-5级\n西南风3-4级\n\n\n\n\n\n\n\n\n\n\n详情\n\n\n\n\n\n\n\n\n\n\n\n周六\n03/22\n\n\n\n\n晴\n\n26/14℃\n\n\n\n\n\n\n\n\n\n西南风3-4级\n西南风3-4级\n\n\n\n\n\n\n\n\n\n\n详情\n\n\n\n\n\n\n\n\n\n\n\n周日\n03/23\n\n\n\n\n多云\n\n28/14℃\n\n\n\n\n\n\n\n\n\n西南风4-5级\n西风3-4级\n\n\n\n\n\n\n\n\n\n\n详情\n\n\n\n\n\n\n\n\n\n\n\n周一\n03/24\n\n\n\n\n晴\n\n29/1"
        data = drop_multi_mark(text)
        print(data)
