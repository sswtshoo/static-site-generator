from markdown import markdown_to_blocks, BlockType, block_to_block_type
from htmlnode import HTMLNode, LeafNode, ParentNode
from inline_md import text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType

def extract_title(markdown: str):
    blocks = markdown_to_blocks(markdown)
    flag = 0
    for block in blocks:
        block = block.lstrip()
        block_type = block_to_block_type(block)
        if block_type == BlockType.HEADING:
            hash_count = len(block) - len(block.lstrip('#'))
            if hash_count == 1:
                flag = 1
                heading = block[hash_count:].lstrip()
    
    if flag == 0:
        raise Exception('No h1 heading found')
    else:
        return heading

def markdown_to_html_node(markdown: str):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        children.append(block_to_html_node(block))
    return ParentNode('div', children=children)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return para_to_html_nodes(block)
    elif block_type == BlockType.CODE:
        return code_to_html_node(block)
    elif block_type == BlockType.HEADING:
        return heading_to_html_nodes(block)
    elif block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    elif block_type == BlockType.ORDERED_LIST:
        return olist_to_html_node(block)
    elif block_type == BlockType.UNORDERED_LIST:
        return ulist_to_html_node(block)
    raise ValueError('invalid block type')
    
    
def text_to_child_nodes(text: str):
    nodes = text_to_textnodes(text)
    children = []
    for node in nodes:
        children.append(text_node_to_html_node(node))
    return children

def para_to_html_nodes(block: str):
    lines = block.split('\n')
    paragraph = " ".join(lines)
    children = text_to_child_nodes(paragraph)
    return ParentNode('p', children=children)

def heading_to_html_nodes(block: str):
    hash_count = len(block) - len(block.lstrip('#'))
    if hash_count + 1 >= len(block):
        raise ValueError('invalid heading markdown')
    heading = block[hash_count + 1:]
    child = text_to_child_nodes(heading)
    return ParentNode(f"h{hash_count}", children=child)
def code_to_html_node(block: str):
    if not block.startswith('```') and not block.endswith('```'):
        raise ValueError('invalid code markdown')
    text = block.strip("`").strip()
    text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(text_node)
    code_node = ParentNode('code', children=[child])
    return ParentNode('pre', children=[code_node])

def quote_to_html_node(block: str):
    lines = block.split('\n')
    children = []
    stripped_lines = []
    for line in lines:
        if not line.startswith('>'):
            raise ValueError('invalid quote markdown')
        stripped_lines.append(line.lstrip('>').strip())
    text = " ".join(stripped_lines)
    children = text_to_child_nodes(text)
    return ParentNode(tag='blockquote', children=children)


def ulist_to_html_node(block: str):
    lists = block.split('\n')
    children = []
    for item in lists:
        text = item[2:]
        child = text_to_child_nodes(text)
        children.append(ParentNode("li", children=child))
    return ParentNode('ul', children=children)

def olist_to_html_node(block: str):
    lists = block.split('\n')
    children = []
    for item in lists:
        text = item[3:]
        child = text_to_child_nodes(text)
        children.append(ParentNode("li", children=child))
    return ParentNode('ol', children=children)


# html_node = markdown_to_html_node("![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)")
# print(html_node.to_html())