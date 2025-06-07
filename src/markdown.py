from enum import Enum

class BlockType(Enum):
    PARAGRAPH = 'paragraph'
    HEADING = 'heading'
    CODE = 'code'
    QUOTE = 'quote'
    UNORDERED_LIST = 'unordered list'
    ORDERED_LIST = 'ordered list'

def block_to_block_type(md_block: str):
    md_text = md_block.strip('\n')
    if md_text.startswith('#'):
        hash_count = len(md_text) - len(md_text.lstrip('#'))
        if 1 <= hash_count <= 6 and md_text[hash_count:].startswith(' '):
            return BlockType.HEADING
        
    if md_text.startswith('```') and md_text.endswith('```') and len(md_text) > 6:
        return BlockType.CODE
    md_lines = md_text.split('\n')
    if len(md_lines) == 1 and md_lines[0].startswith('> '):
        return BlockType.QUOTE
    quote_count = 0
    for line in md_lines:
        if line.startswith('>') and (line == '>' or line.startswith('> ')):
            quote_count += 1

    if quote_count == len(md_lines):
        return BlockType.QUOTE

    dash_count = 0
    for line in md_lines:
        if line.startswith('- '):
            dash_count += 1
    if len(md_lines) == 1 and md_lines[0:2] == '- ':
        return BlockType.UNORDERED_LIST
    
    if dash_count == len(md_lines):
        return BlockType.UNORDERED_LIST
    
    if len(md_lines) == 1 and md_lines[0:3] == '1. ':
        return BlockType.ORDERED_LIST
    
    order_count = 0
    for i in range(0, len(md_lines)):
        if md_lines[i][0:3] == f"{i+1}. ":
            order_count += 1
    if order_count == len(md_lines):
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH

def markdown_to_blocks(markdown: str):
    md_list = markdown.split('\n\n')
    filtered = []
    for block in md_list:
        if block == '':
            continue
        block = block.strip()
        filtered.append(block)
    return filtered

md = """
> "I am in fact a Hobbit in all but size."
>
> -- J.R.R. Tolkien
"""

blocks = markdown_to_blocks(md)
for block in blocks:
    print(block_to_block_type(block))