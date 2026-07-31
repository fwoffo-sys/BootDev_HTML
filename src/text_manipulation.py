import re

FIND_MARKDOWN_SYNTAX = r"\[([^\[\]]*)\]\(([^\(\)]*)\)"

def extract_markdown_images(text):
    return re.findall(r"!" + FIND_MARKDOWN_SYNTAX, text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)" + FIND_MARKDOWN_SYNTAX, text)