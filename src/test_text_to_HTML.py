from platform import node

from htmlnode import HTMLNode, LeafNode, ParentNode
from text_to_HTML import block_to_html_node, markdown_to_html
import unittest

class TestHTMLNode(unittest.TestCase):
    def test_heading_to_html(self):
        block = "## Heading here, with some **bold** text"
        parent_node = block_to_html_node(block)
        self.assertEqual(
            parent_node.to_html(),
            "<h2>Heading here, with some <b>bold</b> text</h2>",
        )

    def test_code_to_html(self):
        block = "```\npython\nprint('Hello, World!')\n```"
        parent_node = block_to_html_node(block)
        self.assertEqual(
            parent_node.to_html(),
            "<pre><code>python\nprint('Hello, World!')\n</code></pre>",
        )

    def test_quote_to_html(self):
        block = "> This is a quote"
        parent_node = block_to_html_node(block)
        self.assertEqual(
            parent_node.to_html(),
            "<blockquote>This is a quote</blockquote>",
        )

    def test_unordered_list_to_html(self):
        block = "- Item 1\n- Item 2\n- Item 3"
        parent_node = block_to_html_node(block)
        self.assertEqual(
            parent_node.to_html(),
            "<ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul>",
        )

    def test_ordered_list_to_html(self):
        block = "1. Item 1\n2. Item 2\n3. Item 3"
        parent_node = block_to_html_node(block)
        self.assertEqual(
            parent_node.to_html(),
            "<ol><li>Item 1</li><li>Item 2</li><li>Item 3</li></ol>",
        )

    def test_ordered_list_with_subcomponents_to_html(self):
        block = "1. **Item 1**\n2. Item _number_ 2\n3. Item 3"
        parent_node = block_to_html_node(block)
        self.assertEqual(
            parent_node.to_html(),
            "<ol><li><b>Item 1</b></li><li>Item <i>number</i> 2</li><li>Item 3</li></ol>",
        )

    def test_paragraph_to_html(self):
        block = "This is a paragraph."
        parent_node = block_to_html_node(block)
        self.assertEqual(
            parent_node.to_html(),
            "<p>This is a paragraph.</p>",
        )  

    def test_multi_line_paragraph_to_html(self):
        block = "This is a paragraph.\nit has multiple lines.\nThose should be joined by spaces."
        parent_node = block_to_html_node(block)
        self.assertEqual(
            parent_node.to_html(),
            "<p>This is a paragraph. it has multiple lines. Those should be joined by spaces.</p>",
        )  

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )


    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )


if __name__ == "__main__":
    unittest.main()