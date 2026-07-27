from textnode import TextNode, TextType
from htmlnode import HTMLNode

def main():
    node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(node)
    properties = {
    "href": "https://www.google.com",
    "target": "_blank",
    }
    htmlNode = HTMLNode(tag="p", value="blahblahblah", props=properties)
    print(htmlNode)
    print(htmlNode.props_to_html())

main()