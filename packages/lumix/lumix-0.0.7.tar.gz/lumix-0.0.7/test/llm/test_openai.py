import unittest
from lumix.llm import OpenAI


class TestOpenAI(unittest.TestCase):
    """"""
    def setUp(self) -> None:
        self.base_url = "https://open.bigmodel.cn/api/paas/v4"
        self.model = "glm-4-flash"
        self.llm = OpenAI(
            model=self.model, base_url=self.base_url,
            key_name="ZHIPU_API_KEY", verbose=True)

    def test_openai_completion(self):
        """"""
        completion = self.llm.completion(prompt="你好")
        print(completion.choices[0].message.content)

    def test_openai_sse(self):
        """"""
        completion = self.llm.completion(prompt="你好", stream=True)
        for chunk in completion:
            print(chunk)
            print(chunk.choices[0].delta.content)
