from lumix.prompt.template import PromptTemplate


__all__ = [
    "template_extract_table",
    "template_extract_content",
    # "extract_table_prompt"
]


template_extract_table = """Please extract all tables from the given document and \
output them as HTML tables. Only provide the HTML code for each table without \
any additional explanations or text outside the HTML tags. Each table should \
be formatted with proper <table>, <tr>, <th>, and <td> tags as appropriate. \
Maintain the original table structure, headers, and data alignment from the \
source document."""


template_extract_content = """Extract all textual content and tables from the provided document. \
Convert the content into HTML format with the following specifications:

1. Represent all main body text in <p> paragraph tags
2. Convert all tables into proper HTML <table> structures with:
    - <thead> for header rows
    - <tbody> for data rows
    - <tr> for table rows
    - <th> for header cells
    - <td> for data cells
3. Preserve original table structures including merged cells using colspan/rowspan attributes
4. Maintain hierarchical relationships between content and tables
5. Omit all non-content elements (page numbers, footers, etc.)
6. Output only the HTML code without any additional text or explanations

Ensure the final output is valid HTML5 and properly formatted with appropriate indentation."""

# extract_table_prompt = PromptTemplate(
#     input_variables=["content"],
#     template=template_extract_table,
# )
