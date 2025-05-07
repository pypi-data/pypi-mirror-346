from typing import List, Dict, Union, Callable, Optional, Iterable
from lumix.llm import TypeLLM
from lumix.types.messages import TypeMessage, ToolMessage
from lumix.types.openai.sync import ChatCompletion
from lumix.types.openai.sse import Stream, ChatCompletionChunk
from lumix.utils import LoggerMixin

from contextlib import asynccontextmanager
from fastmcp import Client
from fastmcp.client.transports import SSETransport, PythonStdioTransport, FastMCPTransport


__all__ = [
    "ChatWithMCPClient"
]


class ChatWithMCPClient(LoggerMixin):
    """Chat with MCP Client"""

    def __init__(
            self,
            llm: Optional[TypeLLM],
            transport: Union[str, SSETransport, PythonStdioTransport, FastMCPTransport],
            max_calls: Optional[int] = 10,
            logger: Optional[Callable] = None,
            verbose: Optional[bool] = False,
            **kwargs,
    ):
        self.llm = llm
        self.transport = transport
        self.max_calls = max_calls
        self.logger = logger
        self.verbose = verbose
        self.kwargs = kwargs
        self.tools = []
        self.openai_tools = []

    async def initialize(self):
        """Async initialization to load tools"""
        self.tools = await self.list_tools()
        self.openai_tools = self.make_openai_tools()

    def make_openai_tools(self) -> List[Dict]:
        """"""
        if not self.tools:
            raise ValueError("Tools not initialized. Call await initialize() first.")
        tools = [
            {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.inputSchema,
                }
            } for tool in self.tools
        ]
        return tools

    @asynccontextmanager
    async def make_mcp_client(
            self,
            transport: Union[str, SSETransport, PythonStdioTransport, FastMCPTransport]
    ) -> Iterable[Client]:
        async with Client(transport) as client:
            yield client

    async def list_tools(self) -> List:
        """"""
        async with self.make_mcp_client(self.transport) as client:
            return await client.list_tools()

    async def completion(
            self,
            prompt: Optional[str] = None,
            messages: Optional[Union[List[TypeMessage], List[Dict]]] = None,
            stream: Optional[bool] = False,
            **kwargs
    ) -> Union[ChatCompletion, Stream[ChatCompletionChunk]]:
        """"""
        async with self.make_mcp_client(self.transport) as client:
            call_times = 0
            finish_reason = None
            completion: Optional[ChatCompletion] = None

            while finish_reason != "stop" and call_times < self.max_calls:
                completion = self.llm.completion(prompt=prompt, messages=messages, tools=self.openai_tools)
                finish_reason = completion.choices[0].finish_reason
                call_times += 1

                if completion.choices[0].finish_reason == "tool_calls":
                    messages.append(completion.choices[0].message)
                    function = completion.choices[0].message.tool_calls[0].function
                    self._logger(msg=f"[Tools] name: {function.name}, arguments: {function.arguments}\n", color="green")
                    observation = await client.call_tool(function.name, eval(function.arguments))
                    messages.append(ToolMessage(role="tool", content=str(observation), tool_call_id=completion.choices[0].message.tool_calls[0].id))

            if call_times >= self.max_calls:
                if completion and completion.choices[0].finish_reason == "tool_calls":
                    function = completion.choices[0].message.tool_calls[0].function
                    msg = f"[Assistant] 达到最大调用次数，模型未能给出最终回答。\n[Last Tool] Function: {function.name}, Arguments: {function.arguments}\n"
                    self._logger(msg=msg, color="red")
                elif completion and completion.choices[0].finish_reason == "stop":
                    pass
                else:
                    self._logger(msg=f"[Assistant] Error: {completion}")
            return completion
