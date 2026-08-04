from enum import Enum
import re
from typing import Tuple

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown: str):
    blocks = markdown.split("\n\n")
    return [block.strip() for block in blocks if block.strip()]

def block_to_block_type(block: str) -> BlockType:
    lines = block.split("\n")
    if re.match(r"^#{1,6} ", lines[0]):
        return BlockType.HEADING
    elif block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE
    elif block.startswith(">"):
        return BlockType.QUOTE
    elif all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    elif all(line[0].isdigit() and line[1] == "." and line[2] == " " for line in lines) and all(lines[i][0] <= lines[i + 1][0] for i in range(len(lines) - 1)) and lines[0][0] == "1":
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH

def block_to_text(block: str) -> Tuple[str, BlockType]:
    block_type = block_to_block_type(block)
    if block_type == BlockType.HEADING:
        return block.lstrip("#").strip(), block_type
    elif block_type == BlockType.CODE:
        return block[4:-3], block_type
    elif block_type == BlockType.QUOTE:
        return block[1:].strip(), block_type
    elif block_type == BlockType.UNORDERED_LIST:
        return "\n".join(line[2:] for line in block.split("\n")), block_type
    elif block_type == BlockType.ORDERED_LIST:
        return "\n".join(line[3:] for line in block.split("\n")), block_type
    else:
        return block, BlockType.PARAGRAPH
