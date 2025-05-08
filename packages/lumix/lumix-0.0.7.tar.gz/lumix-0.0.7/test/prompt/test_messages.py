import unittest
from lumix.embedding import PretrainedEmbedding
from lumix.prompt import MessagesPrompt, PromptTemplate
from lumix.types.messages import SystemMessage, UserMessage, AssistantMessage


class TestPromptFewShotRerank(unittest.TestCase):
    """"""

    def setUp(self):
        """"""
        self.system_message = SystemMessage(content="你是一个计算器")
        self.few_shot = [
            UserMessage(content="1+1="),
            AssistantMessage(content="2"),
            UserMessage(content="1+2="),
            AssistantMessage(content="3"),
            UserMessage(content="1+3="),
            AssistantMessage(content="4"),
        ]
        self.name_or_path = "/home/models/BAAI/bge-small-zh-v1.5"
        self.embedding = PretrainedEmbedding(
            name_or_path=self.name_or_path,
            batch_size=2,
            normalize_embeddings=True,
            verbose=True,
        )

    def test_rerank(self):
        """"""
        messages_prompt = MessagesPrompt(
            system_message=self.system_message,
            few_shot=self.few_shot,
            n_shot=2, rerank=True,
            support_system=True,
            embedding=self.embedding,
            verbose=True,
        )
        messages = messages_prompt.prompt_format(content="1+3=")
        for message in messages:
            print(f"{message.role}: {message.content}")
