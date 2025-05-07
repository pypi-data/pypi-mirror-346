import unittest
import matplotlib.pyplot as plt
from lumix.llm import OpenAI
from lumix.documents import StructuredPDF
from lumix.types.messages import ImageMessage
from lumix.prompt.prompts import *


class TestExtractTablePrompt(unittest.TestCase):
    """"""
    def setUp(self):
        """"""
        self.pdf_path = "https://pdf.dfcfw.com/pdf/H3_AP202503201645075160_1.pdf?1742482089000.pdf"
        base_url = "https://api-inference.modelscope.cn/v1/"
        model = "Qwen/Qwen2.5-VL-32B-Instruct"
        self.llm = OpenAI(model=model, base_url=base_url, key_name="MODELSCOPE_TOKEN", verbose=False)

    def test_image_message_dict(self):
        """"""
        messages = [
            ImageMessage(
                role="user",
                content=template_extract_table,
                images=["../data/extract-image-table.png"],
            ).to_openai()
        ]
        completion = self.llm.completion(messages=messages)
        print(completion.choices[0].message.content)

    def test_image_classify(self):
        """"""
        pdf = StructuredPDF(self.pdf_path)
        images = pdf.extract_images()
        for image in images:
            messages = [
                ImageMessage(
                    role="user",
                    content=image_classify_prompt.format_prompt(
                        categories=["table", "industry chain", "icon", "chart"]).to_string(),
                    images=[image],
                ).to_openai()
            ]
            completion = self.llm.completion(messages=messages)
            print(completion.choices[0].message.content)
            plt.imshow(image)
            plt.axis('off')
            plt.show()

    def test_images_classify(self):
        """"""
        pdf = StructuredPDF(self.pdf_path)
        images = pdf.extract_images()
        messages = [
            ImageMessage(
                role="user",
                content=images_classify_prompt.format_prompt(
                    categories=["table", "industry chain", "icon", "chart"]).to_string(),
                images=images,
            ).to_openai()
        ]

        completion = self.llm.completion(messages=messages)
        print(completion.choices[0].message.content)
