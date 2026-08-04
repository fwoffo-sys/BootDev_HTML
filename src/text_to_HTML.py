from blocks import BlockType,  markdown_to_blocks, block_to_text
from textnode import text_to_html_nodes
from htmlnode import HTMLNode, LeafNode, ParentNode

def block_to_html_node(block: str) -> HTMLNode:
    text, block_type = block_to_text(block)
    match block_type:
        case BlockType.PARAGRAPH:
            return ParentNode("p", text_to_html_nodes(text.replace("\n", " ")))
        case BlockType.HEADING:
            heading_count = len(block) - len(block.lstrip("#"))
            return ParentNode(f"h{heading_count}", text_to_html_nodes(text))
        case BlockType.CODE:
            return ParentNode("pre", [LeafNode("code", text)])
        case BlockType.QUOTE:
            return ParentNode("blockquote", text_to_html_nodes(text))
        case BlockType.UNORDERED_LIST:
            return ParentNode("ul", [ParentNode("li", text_to_html_nodes(line)) for line in text.split("\n")])
        case BlockType.ORDERED_LIST:
            return ParentNode("ol", [ParentNode("li", text_to_html_nodes(line)) for line in text.split("\n")])

def markdown_to_html(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    html_nodes = [block_to_html_node(block) for block in blocks]
    return ParentNode("div", html_nodes)
