import unittest
from lumix.documents import StructuredPDF
from lumix.utils.image import drop_similar_images, drop_single_color_images


class TestReadPDF(unittest.TestCase):

    def setUp(self):
        self.pdf_path = "https://pdf.dfcfw.com/pdf/H3_AP202503201645075160_1.pdf?1742482089000.pdf"

    def test_read_pdf(self):
        pdf = StructuredPDF(self.pdf_path)

        print(len(pdf.documents))
        print(pdf.documents[0].metadata.images)
        print(pdf.documents[0].metadata.page_number)

    def test_save_image(self):
        """"""
        pdf = StructuredPDF(self.pdf_path)
        pdf.save_images(path="./")

    def test_tran_image(self):
        """"""
        pdf = StructuredPDF(self.pdf_path)
        images = pdf.page_to_image(dpi=300, pages=[0])
        print(images)

    def test_request(self):
        """"""
        pdf = StructuredPDF(self.pdf_path)
        print(pdf.documents)
        pdf.save_structured(path="./")

    def test_extract_images(self):
        """"""
        pdf = StructuredPDF(self.pdf_path)
        images = pdf.extract_images()
        drop_images = drop_similar_images(images=images)
        print(drop_images)

    def test_show_image(self):
        """"""
        import matplotlib.pyplot as plt
        pdf = StructuredPDF(self.pdf_path)
        images = pdf.extract_images(drop_duplicates=True, size=80)
        for image in images:
            plt.imshow(image)
            plt.axis('off')
            plt.show()
