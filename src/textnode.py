from enum import Enum
from htmlnode import *
from text_manipulation import extract_markdown_images, extract_markdown_links


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold text"
    ITALIC = "italic text"
    CODE = "code text"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    output = []
    for node in old_nodes:
        if not node.text_type == TextType.TEXT:
            output.append(node)
        else:
            #first we make sure that the number of delimiters is even, otherwise we have an unclosed delimiter. This includes having no delimiters
            if node.text.count(delimiter) % 2 != 0:
                raise ValueError("Unmatched delimiter in text node")
            #we remove empty strings from the start and end
            split_text = node.text.split(delimiter)
            if split_text[0] == "":
                split_text = split_text[1:]
            if split_text[-1] == "":
                split_text = split_text[:-1]

            #we alternate between text and text_type nodes, starting with what the first node should be.
            if node.text.startswith(delimiter):
                start_type = text_type
                second_type = TextType.TEXT
            else:
                start_type = TextType.TEXT
                second_type = text_type

            for i in range(len(split_text)):
                #if the string is empty, we skip
                if split_text[i] == "":
                    continue
                else:
                    if i % 2 == 0:
                        output.append(TextNode(split_text[i], start_type))
                    else:
                        output.append(TextNode(split_text[i], second_type))
    return output

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    output = []
    for node in old_nodes:
        if not node.text_type == TextType.TEXT:
            output.append(node)
        else:
            images = extract_markdown_images(node.text)
            if len(images) == 0:
                output.append(node)
            else:
                intermediate_nodes = [node]
                for image in images:
                    image_alt, image_url = image
                    intermediate_nodes = split_specific_image(intermediate_nodes, image_alt, image_url)
                output.extend(intermediate_nodes)
    return output

def split_specific_image(old_nodes: list[TextNode], image_alt: str, image_url: str) -> list[TextNode]:
    output = []
    for node in old_nodes:
        if not node.text_type == TextType.TEXT or f"![{image_alt}]({image_url})" not in node.text:
            output.append(node)
        else:
            #we split the text into parts, and so long as that image exists we split the text
            sections = node.text.split(f"![{image_alt}]({image_url})", 1)
            while True:
                if sections[0] != "":
                    output.append(TextNode(sections[0], TextType.TEXT))
                if len(sections) > 1:
                    output.append(TextNode(image_alt, TextType.IMAGE, image_url))
                else:
                    break
                sections = sections[1].split(f"![{image_alt}]({image_url})", 1)
    return output

#Always call after split_nodes_image, since if there are images and links with identical content, the image split function can distinguish them but this one cannot.
def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    output = []
    for node in old_nodes:
        if not node.text_type == TextType.TEXT:
            output.append(node)
        else:
            links = extract_markdown_links(node.text)
            if len(links) == 0:
                output.append(node)
            else:
                intermediate_nodes = [node]
                for link in links:
                    link_text, link_url = link
                    intermediate_nodes = split_specific_link(intermediate_nodes, link_text, link_url)
                output.extend(intermediate_nodes)
    return output

def split_specific_link(old_nodes: list[TextNode], link_text: str, link_url: str) -> list[TextNode]:
    output = []
    for node in old_nodes:
        if not node.text_type == TextType.TEXT or f"[{link_text}]({link_url})" not in node.text:
            output.append(node)
        else:
            #we split the text into parts, and so long as that link exists we split the text
            sections = node.text.split(f"[{link_text}]({link_url})", 1)
            while True:
                if sections[0] != "":
                    output.append(TextNode(sections[0], TextType.TEXT))
                if len(sections) > 1:
                    output.append(TextNode(link_text, TextType.LINK, link_url))
                else:
                    break
                sections = sections[1].split(f"[{link_text}]({link_url})", 1)
    return output

def text_to_textnodes(text: str) -> list[TextNode]:
    start_node = TextNode(text, TextType.TEXT)
    nodes = [start_node]
    #always call image split before link split
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    return nodes
