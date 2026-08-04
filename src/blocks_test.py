from blocks import markdown_to_blocks, block_to_block_type, block_to_text, BlockType
import unittest

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_strip_blocks(self):
        md = """
This is **bolded** paragraph with trailing spaces           

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line, no whitespace

         - This is a list
- with items
- and leading whitespace
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_types1(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        block_types = [block_to_block_type(block) for block in blocks]
        self.assertEqual(
            blocks,
            [
                BlockType.PARAGRAPH,
                BlockType.PARAGRAPH,
                BlockType.UNORDERED_LIST,
            ],
        )


    def test_markdown_to_blocks_types2(self):
        md = """
# This is a heading

## so too this

### and this

#### and these

##### still going strong

###### final heading

####### too many hashtags!

#oops forgot a space

'''
hell yeah,
a code block'''

''' not a code block'''

> This is a quote

>so is this
"""
        blocks = markdown_to_blocks(md)
        block_types = [block_to_block_type(block) for block in blocks]
        self.assertEqual(
            blocks,
            [
                BlockType.HEADING,
                BlockType.HEADING,
                BlockType.HEADING,
                BlockType.HEADING,
                BlockType.HEADING,
                BlockType.HEADING,
                BlockType.PARAGRAPH,
                BlockType.PARAGRAPH,
                BlockType.CODE,
                BlockType.PARAGRAPH,
                BlockType.QUOTE,
                BlockType.QUOTE,
            ],
        )

    def test_markdown_to_blocks_types3(self):
        md = """
- This is a list
- with items
- in no particular order

1. This is an ordered list
2. with items
3. in order

- This looks like a list
-but oh no,
- we were missing a space on one line

1. This looks like an ordered list
2.but oh no,
3. we were missing a space on one line

1. We added the line
2. but oh no,
1. we walked backwards in order
"""
        blocks = markdown_to_blocks(md)
        block_types = [block_to_block_type(block) for block in blocks]
        self.assertEqual(
            blocks,
            [
                BlockType.UNORDERED_LIST,
                BlockType.ORDERED_LIST,
                BlockType.PARAGRAPH,
                BlockType.PARAGRAPH,
                BlockType.PARAGRAPH
            ],
        )

    def test_Getting_text_from_blocks1(self):
        md = """
### Heading text
still the heading   

'''
Code block
'''

> This is a quote
which drags
on
and on

- This is a list
- with items
- in no particular order

1. This is an ordered list
2. with items
3. in order

This is a paragraph with **bold** text and _italic_ text.
"""
        blocks = markdown_to_blocks(md)
        text, block_types = [block_to_text(block) for block in blocks]
        self.assertEqual(
            text,
            [
                "Heading text\nstill the heading",
                "Code block",
                "This is a quote\nwhich drags\non\nand on",
                "This is a list\nwith items\nin no particular order",
                "This is an ordered list\nwith items\nin order",
                "This is a paragraph with **bold** text and _italic_ text.",
            ],
        )

        self.assertEqual(
            block_types,
            [
                BlockType.HEADING,
                BlockType.CODE,
                BlockType.QUOTE,
                BlockType.UNORDERED_LIST,
                BlockType.ORDERED_LIST,
                BlockType.PARAGRAPH,
            ],
        )

if __name__ == "__main__":
    unittest.main()