import unittest
from lumix.llm import OpenAI
from lumix.documents import StructuredPDF
from lumix.prompt.prompts import entities_prompt, relations_prompt


class TestGraphRAGPrompt(unittest.TestCase):
    """"""
    def setUp(self) -> None:
        self.base_url = "https://open.bigmodel.cn/api/paas/v4"
        self.model = "glm-4-flash"
        self.llm = OpenAI(
            model=self.model, base_url=self.base_url,
            key_name="ZHIPU_API_KEY", verbose=True)

    def test_graph_rag_prompt(self):
        """"""
        pdf = StructuredPDF(path_or_data="https://pdf.dfcfw.com/pdf/H3_AP202503201645026964_1.pdf?1742476974000.pdf")
        content = pdf.to_text()
        prompt = entities_prompt.format_prompt(content=content, types=["企业", "产品", "技术"]).to_string()
        completion = self.llm.completion(prompt=prompt)
        print(completion.choices[0].message.content)

    def test_spliter(self):
        """"""
        pdf = StructuredPDF(path_or_data="https://pdf.dfcfw.com/pdf/H3_AP202503201645026964_1.pdf?1742476974000.pdf")
        document = pdf.to_text()

        from langchain_text_splitters import RecursiveCharacterTextSplitter
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=0)
        texts = text_splitter.split_text(document)
        print(len(texts))

    def test_to_split_text(self):
        """"""
        pdf = StructuredPDF(path_or_data="https://pdf.dfcfw.com/pdf/H3_AP202503201645026964_1.pdf?1742476974000.pdf")
        texts = pdf.to_split_text(chunk_size=100, chunk_overlap=0)
        print(len(texts))
        print([len(chunk) for chunk in texts])

    def test_to_split_documents(self):
        """"""
        pdf = StructuredPDF(path_or_data="https://pdf.dfcfw.com/pdf/H3_AP202503201645026964_1.pdf?1742476974000.pdf")
        docs = pdf.to_split_documents(chunk_size=100, chunk_overlap=0)
        print(len(docs))
        print([len(page.page_content) for page in docs])

    def test_extract_images(self):
        """"""
        pdf = StructuredPDF(path_or_data="https://pdf.dfcfw.com/pdf/H3_AP202503201645026964_1.pdf?1742476974000.pdf")
        images = pdf.extract_images()
        print(images)
