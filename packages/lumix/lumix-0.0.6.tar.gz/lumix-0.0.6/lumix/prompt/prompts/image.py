from lumix.prompt.template import PromptTemplate


__all__ = [
    "image_classify_prompt",
    "images_classify_prompt",
]


template_image_classify = """Classify the image into one of these categories: \
{categories}. 

Return only the exact category name from the list provided, without explanations."""


image_classify_prompt = PromptTemplate(
    input_variables=["categories"],
    template=template_image_classify,
)


template_images_classify = """Classify each image into one of these categories: \
{categories}. 

Return a Python-style list of category names (e.g., ['cat', 'car', 'mountain']) in the same order as the input images. \
Do not include explanations, indexes, or formatting characters like quotes."""


images_classify_prompt = PromptTemplate(
    input_variables=["categories"],
    template=template_images_classify,
)
