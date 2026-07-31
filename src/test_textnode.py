from platform import node
import unittest
from textnode import TextNode, TextType, split_nodes_delimiter, text_node_to_html_node, split_nodes_image, split_nodes_link, text_to_textnodes


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_URL(self):
        node = TextNode("This is a text node", TextType.LINK, "Google.com")
        node2 = TextNode("This is a text node", TextType.LINK, "Google.com")
        self.assertEqual(node, node2)

    def test_DifferentText(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is another text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_DifferentType(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_NoURL(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.BOLD, url="Google.com")
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")

    def test_italic(self):
        node = TextNode("This is an italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic node")

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")

    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, "google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertTrue("href" in html_node.props)
        self.assertEqual(html_node.props["href"], "google.com")


    def test_image(self):
        node = TextNode("This is an image node", TextType.IMAGE, "pic.net")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertTrue("src" in html_node.props)
        self.assertTrue("alt" in html_node.props)
        self.assertEqual(html_node.props["src"], "pic.net")
        self.assertEqual(html_node.props["alt"], "This is an image node")

    def test_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "code block")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text, " word")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

    def test_start_delimiter(self):
        node = TextNode("`This` is text with a code block word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text, "This")
        self.assertEqual(new_nodes[0].text_type, TextType.CODE)
        self.assertEqual(new_nodes[1].text, " is text with a code block word")
        self.assertEqual(new_nodes[1].text_type, TextType.TEXT)

    def test_end_delimiter(self):
        node = TextNode("This is text with a code block `word`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text, "This is text with a code block ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "word")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)

    def test_many_delimiter(self):
        node = TextNode("`This` is `text with` a code block `word`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 5)
        self.assertEqual(new_nodes[0].text, "This")
        self.assertEqual(new_nodes[0].text_type, TextType.CODE)
        self.assertEqual(new_nodes[1].text, " is ")
        self.assertEqual(new_nodes[1].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[2].text, "text with")
        self.assertEqual(new_nodes[2].text_type, TextType.CODE)
        self.assertEqual(new_nodes[3].text, " a code block ")
        self.assertEqual(new_nodes[3].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[4].text, "word")
        self.assertEqual(new_nodes[4].text_type, TextType.CODE)

    def test_types_delimiter(self):
        node = TextNode("This **parser** is fully capable of `handling` multiple **delimiters**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This **parser** is fully capable of ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "handling")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text, " multiple **delimiters**")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
        newer_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
        self.assertEqual(len(newer_nodes), 6)
        self.assertEqual(newer_nodes[0].text, "This ")
        self.assertEqual(newer_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(newer_nodes[1].text, "parser")
        self.assertEqual(newer_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(newer_nodes[2].text, " is fully capable of ")
        self.assertEqual(newer_nodes[2].text_type, TextType.TEXT)
        self.assertEqual(newer_nodes[3].text, "handling")
        self.assertEqual(newer_nodes[3].text_type, TextType.CODE)
        self.assertEqual(newer_nodes[4].text, " multiple ")
        self.assertEqual(newer_nodes[4].text_type, TextType.TEXT)
        self.assertEqual(newer_nodes[5].text, "delimiters")
        self.assertEqual(newer_nodes[5].text_type, TextType.BOLD)

    def test_order_delimiter(self):
        node = TextNode("This **parser** is fully capable of `handling` multiple **delimiters**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        newer_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
        self.assertEqual(len(newer_nodes), 6)
        self.assertEqual(newer_nodes[0].text, "This ")
        self.assertEqual(newer_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(newer_nodes[1].text, "parser")
        self.assertEqual(newer_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(newer_nodes[2].text, " is fully capable of ")
        self.assertEqual(newer_nodes[2].text_type, TextType.TEXT)
        self.assertEqual(newer_nodes[3].text, "handling")
        self.assertEqual(newer_nodes[3].text_type, TextType.CODE)
        self.assertEqual(newer_nodes[4].text, " multiple ")
        self.assertEqual(newer_nodes[4].text_type, TextType.TEXT)
        self.assertEqual(newer_nodes[5].text, "delimiters")
        self.assertEqual(newer_nodes[5].text_type, TextType.BOLD)

    def test_backtoback_delimiter(self):
        node = TextNode("`This`` is` text with a `code` block word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 5)
        self.assertEqual(new_nodes[0].text, "This")
        self.assertEqual(new_nodes[0].text_type, TextType.CODE)
        self.assertEqual(new_nodes[1].text, " is")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text, " text with a ")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[3].text, "code")
        self.assertEqual(new_nodes[3].text_type, TextType.CODE)
        self.assertEqual(new_nodes[4].text, " block word")
        self.assertEqual(new_nodes[4].text_type, TextType.TEXT)

    def test_error_delimiter(self):
        node = TextNode("This is a case of **unencloses text.", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_identical_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_alternating_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png), and the first again ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
                TextNode(", and the first again ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://example.com) and another [second link](https://second-example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://second-example.com"),
            ],
            new_nodes,
        )

    def test_identical_links(self):
        node = TextNode(
            "This is text with a [link](https://example.com) and another [link](https://example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
            ],
            new_nodes,
        )

    def test_alternating_links(self):
        node = TextNode(
            "This is text with a [link](https://example.com) and another [second link](https://second-example.com), and the first again [link](https://example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://second-example.com"),
                TextNode(", and the first again ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
            ],
            new_nodes,
        )

    def test_image_and_links(self):
        node = TextNode(
            "This is text with a [link](https://example.com) and an image: ![alt text](https://example.com/image.png), and a link again [link](https://example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        newer_nodes = split_nodes_link(new_nodes)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(" and an image: ", TextType.TEXT),
                TextNode("alt text", TextType.IMAGE, "https://example.com/image.png"),
                TextNode(", and a link again ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
            ],
            newer_nodes,
        )    

    def test_no_link(self):
        node = TextNode(
            "This is text with an image: ![alt text](https://example.com/image.png), and no link",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an image: ![alt text](https://example.com/image.png), and no link", TextType.TEXT),
            ],
            new_nodes,
        )   

    def test_no_image(self):
        node = TextNode(
            "This is text with a link: [link](https://example.com), and no image",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link: [link](https://example.com), and no image", TextType.TEXT),
            ],
            new_nodes,
        )   

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],  
            nodes,
        )



if __name__ == "__main__":
    unittest.main()