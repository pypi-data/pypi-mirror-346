import unittest
from lumix.prompt import MessagesPrompt, PromptTemplate
from lumix.types.messages import SystemMessage, UserMessage, AssistantMessage


class TestPromptTemplate(unittest.TestCase):
    """"""
    def test_template(self):
        """"""
        PROMPT_SUMMARY_TMP = """Content: {content}\nQuestion: {question}"""

        summary_prompt = PromptTemplate(
            input_variables=["content", "question"],
            template=PROMPT_SUMMARY_TMP)

        system_message = SystemMessage(
            content="""You were a helpful assistant, answering questions using the reference content provided.""")

        print(summary_prompt.format(content="1+3=", question="What is the answer?"))
        print()
        print(summary_prompt.format(content="1+3=", question="What is the answer?").to_string())
        print()
        print(summary_prompt.format(content="1+3=", question="What is the answer?").to_messages(role="user"))
        print()
        print(summary_prompt.format_prompt(content="1+3=", question="What is the answer?").to_messages(role="user"))
