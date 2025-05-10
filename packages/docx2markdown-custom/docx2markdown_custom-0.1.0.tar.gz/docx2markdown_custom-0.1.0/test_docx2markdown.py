from docx2markdown_custom import docx_to_markdown_custom

if __name__ == "__main__":
    with open("./Test_Spec.docx", "rb") as f:
        docx_bytes = f.read()
    md = docx_to_markdown_custom(docx_bytes)
    print(md) 