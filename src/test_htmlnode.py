import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_no_error_props(self):
        properties = {
        "href": "https://www.google.com",
        "target": "_blank",
        }
        htmlNode = HTMLNode(tag="p", value="blahblahblah", props=properties)
        htmlNode.props_to_html()
        print(htmlNode.props_to_html())

    def test_no_error_print(self):
        properties = {
        "href": "https://www.google.com",
        "target": "_blank",
        }
        htmlNode = HTMLNode(tag="p", value="blahblahblah", props=properties)
        print(htmlNode)

    def test_right_props_formatting(self):
        properties = {
        "href": "https://www.google.com",
        "target": "_blank",
        }
        htmlNode = HTMLNode(tag="p", value="blahblahblah", props=properties)
        self.assertEqual(htmlNode.props_to_html(), " href=\"https://www.google.com\" target=\"_blank\"")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_properties(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "<a href=\"https://www.google.com\">Click me!</a>")

    def test_leaf_tagless(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")


    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )


if __name__ == "__main__":
    unittest.main()