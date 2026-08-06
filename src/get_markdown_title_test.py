import unittest
from main import get_markdown_title

class TestGetMarkdownTitle(unittest.TestCase):
    def test_get_markdown_title(self):
        markdown = "# Hello, World!"
        expected = "Hello, World!"
        self.assertEqual(get_markdown_title(markdown), expected)

    def test_get_markdown_title_no_title(self):
        markdown = "This is some text without a title."
        with self.assertRaises(Exception):
            get_markdown_title(markdown)

    def test_get_markdown_title_multiple_titles(self):
        markdown = "# First Title\nSome text.\n# Second Title"
        expected = "First Title"
        self.assertEqual(get_markdown_title(markdown), expected)

    def test_get_markdown_title_with_whitespace(self):
        markdown = "#   Title with whitespace   "
        expected = "Title with whitespace"
        self.assertEqual(get_markdown_title(markdown), expected)

    def test_get_markdown_title_only_second_heading(self):
        markdown = "Some text.\n## heading 2\n"
        with self.assertRaises(Exception):
            get_markdown_title(markdown)

if __name__ == "__main__":
    unittest.main()