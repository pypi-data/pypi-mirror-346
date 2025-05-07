import unittest
from lumix.llm import OpenAI
from pydantic import BaseModel, Field
from typing import Optional
from pprint import pprint


class TestOpenAIStruct(unittest.TestCase):
    """"""
    def setUp(self) -> None:
        self.base_url = "https://open.bigmodel.cn/api/paas/v4"
        self.model = "glm-4-flash"
        self.llm = OpenAI(
            model=self.model, base_url=self.base_url,
            key_name="ZHIPU_API_KEY", verbose=True)

    def test_structured_output(self):
        """"""
        class Joke(BaseModel):
            """Joke to tell user."""
            setup: str = Field(description="The setup of the joke")
            punchline: str = Field(description="The punchline to the joke")
            rating: int = Field(description="How funny the joke is, from 1 to 10")
        data = self.llm.structured_output(schema=Joke, prompt="给我讲个简单的笑话")
        pprint(data)

    def test_structured(self):
        """"""
        class ParseDict(BaseModel):
            """结构化输出：为用户解析数据"""
            time: str = Field(description="时间")
            person: str = Field(description="人物")
            content: str = Field(description="内容")
        data = self.llm.structured_output(schema=ParseDict, prompt="结构化输出：小明早晨去商场买了一个苹果")
        pprint(data)

