import sys
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

def generate_page(from_path, template_path, dest_path, basepath):
    with open(from_path, "r") as f:
        markdown = f.read()
    markdown_title = get_markdown_title(markdown)
    html_content = markdown_to_html(markdown).to_html()

    with open(template_path, "r") as f:
        template = f.read()

    page = template.replace(r"{{ Title }}", markdown_title).replace(r"{{ Content }}", html_content)
    page = page.replace(r'href="/', f'href="{basepath}').replace(r'src="/', f'src="{basepath}')

    #make sure the destination directory exists
    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    with open(dest_path, "w") as f:
        f.write(page)

def generate_page_recursively(from_dir, template_path, dest_dir, basepath):
    files = os.listdir(from_dir)
    for file in files:
        from_path = os.path.join(from_dir, file)
        if os.path.isfile(from_path) and file.endswith(".md"):
            relative_path = os.path.relpath(from_path, from_dir)
            dest_path = os.path.join(dest_dir, relative_path[:-3] + ".html")
            generate_page(from_path, template_path, dest_path, basepath)
        elif os.path.isdir(from_path):
            dest_subdir = os.path.join(dest_dir, file)
            generate_page_recursively(from_path, template_path, dest_subdir, basepath)

def main():
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    copy_directory("./static", "./docs")
    generate_page_recursively("./content", "./template.html", "./docs", basepath)

main()