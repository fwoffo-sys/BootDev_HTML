from htmlnode import HTMLNode
from text_to_HTML import markdown_to_html
import os
import shutil

def copy_directory(src, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    if os.path.isdir(src):
        os.mkdir(dest)
    source_contents = os.listdir(src)
    for content in source_contents:
        src_path = os.path.join(src, content)
        dest_path = os.path.join(dest, content)
        if os.path.isfile(src_path):
            shutil.copy(src_path, dest_path)
        else:
            copy_directory(src_path, dest_path)

def get_markdown_title(markdown):
    lines = markdown.splitlines()
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("No starting title found in markdown")

def generate_page(from_path, template_path, dest_path):
    with open(from_path, "r") as f:
        markdown = f.read()
    markdown_title = get_markdown_title(markdown)
    html_content = markdown_to_html(markdown).to_html()

    with open(template_path, "r") as f:
        template = f.read()

    page = template.replace(r"{{ Title }}", markdown_title).replace(r"{{ Content }}", html_content)

    #make sure the destination directory exists
    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    with open(dest_path, "w") as f:
        f.write(page)

def main():
    copy_directory("./static", "./public")
    generate_page("./content/index.md", "./template.html", "./public/index.html")

main()