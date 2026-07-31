import unittest
from text_manipulation import extract_markdown_images, extract_markdown_links

class TestTextManipulation(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_links(self):
        text = "Here is a link: [Google](https://google.com) and here is another: [GitHub](https://github.com)"
        expected = [("Google", "https://google.com"), ("GitHub", "https://github.com")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_links_not_images(self):
        text = "Here is a link: [Google](https://google.com) and here is an image: ![GitHub](https://github.com)"
        expected = [("Google", "https://google.com")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_images_not_links(self):
        text = "Here is a link: [Google](https://google.com) and here is an image: ![GitHub](https://github.com)"
        expected = [("GitHub", "https://github.com")]
        self.assertEqual(extract_markdown_images(text), expected)

    