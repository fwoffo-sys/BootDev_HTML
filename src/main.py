from textnode import TextNode, TextType
from htmlnode import HTMLNode
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


def main():
    copy_directory("./static", "./public")

main()