import unittest
from lumix.llm import OpenAI
from lumix.types.messages import ImageMessage


class TestImageMessage(unittest.TestCase):
    """"""
    def test_image_message(self):
        """"""
        image_message = ImageMessage(
            role="user",
            content="介绍图片",
            images=["https://pic3.zhimg.com/v2-6ac0e399774bde7efb391f76b7f262ca_1440w.jpg"],
        )
        print(image_message)
        # print(image_message.to_openai(image_type="base64"))
        # print(image_message.to_openai(image_type="url"))
        # print(image_message.to_dict(image_type="base64"))
        # print(image_message.to_dict(image_type="url"))
        print(image_message.to_dict(image_type="PIL"))

    def test_image_message_dict(self):
        """"""
        base_url = "https://api-inference.modelscope.cn/v1/"
        model = "Qwen/Qwen2.5-VL-32B-Instruct"
        llm = OpenAI(model=model, base_url=base_url, key_name="MODELSCOPE_TOKEN", verbose=False)
        messages = [
            ImageMessage(
                role="user",
                content="介绍图片",
                images=["https://pic3.zhimg.com/v2-6ac0e399774bde7efb391f76b7f262ca_1440w.jpg"],
            ).to_openai()
        ]
        completion = llm.completion(messages=messages)
        print(completion.choices[0].message.content)
