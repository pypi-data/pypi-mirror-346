import unittest
from lumix.llm import OpenAI
from lumix.agent import ToolsAgent, Tools
from lumix.agent.tools import get_weather, random_number


class TestToolsAgent(unittest.TestCase):
    def setUp(self):
        """"""
        self.base_url = "https://open.bigmodel.cn/api/paas/v4"
        self.model = "glm-4-flash"
        self.llm = OpenAI(
            model=self.model, base_url=self.base_url,
            key_name="ZHIPU_API_KEY", verbose=False)
        self.tools = Tools(tools=[random_number])

    def test_tools_agent(self):
        """"""
        agent = ToolsAgent(tools=self.tools, llm=self.llm, verbose=True)
        agent.completion(prompt="你好，请给我一个0-100的随机数")

    def test_tools_agent_sse(self):
        """"""
        agent = ToolsAgent(tools=self.tools, llm=self.llm, verbose=True)
        completion = agent.completion(prompt="你好，请给我一个0-100的随机数", stream=True)
        answer = ""
        for chunk in completion:
            # print(chunk)
            if chunk.choices[0].delta.content:
                answer += chunk.choices[0].delta.content
        print(answer)


class TestLocalToolsAgent(unittest.TestCase):
    """"""
    def setUp(self):
        """"""
        self.base_url = "http://172.16.11.159:8000/"
        self.model = "Qwen2.5-14B-Instruct"
        self.llm = OpenAI(
            model=self.model, base_url=self.base_url,
            api_key="empty", verbose=False)
        self.tools = Tools(tools=[random_number])

    def test_tools_agent(self):
        """"""
        agent = ToolsAgent(tools=self.tools, llm=self.llm, verbose=True)
        agent.completion(prompt="你好，请给我一个0-100的随机数")

    def test_tools_agent_sse(self):
        """"""
        agent = ToolsAgent(tools=self.tools, llm=self.llm, verbose=True)
        completion = agent.completion(prompt="你好，请给我一个0-100的随机数", stream=True)
        answer = ""
        for chunk in completion:
            if chunk.choices[0].delta.content:
                answer += chunk.choices[0].delta.content
        print(answer)
