from textnode import TextNode, TextType
import re

def extract_markdown_images(text: str):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text: str):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_delimiter(old_nodes: list['TextNode'], delimiter: str, text_type: TextType):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            text_parts = node.text.split(delimiter)

            if len(text_parts) % 2 == 0:
                raise Exception('Invalid markdown syntax')
            
            for i, part in enumerate(text_parts):
                if i % 2 == 0:
                    if part != "":
                        new_nodes.append(TextNode(part, TextType.TEXT))
                else:
                    new_nodes.append(TextNode(part, text_type))
           
    return new_nodes


def split_nodes_image(old_nodes: list['TextNode']):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        node_text = node.text
        matches = extract_markdown_images(node_text)

        if not matches:
            new_nodes.append(node)
            continue

        remaining_text = node_text
        for alt_text, url in matches:
            split_str = f"![{alt_text}]({url})"
            parts = remaining_text.split(split_str, 1)
            
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url=url))
            remaining_text = parts[1]

        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes: list['TextNode']):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        node_text = node.text
        matches = extract_markdown_links(node_text)

        if not matches:
            new_nodes.append(node)
            continue

        remaining_text = node_text
        for link_text, link_url in matches:
            split_str = f"[{link_text}]({link_url})"
            parts = remaining_text.split(split_str, 1)

            if len(parts) != 2:
                raise ValueError("Invalid markdown link syntax")

            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            new_nodes.append(TextNode(link_text, TextType.LINK, url=link_url))
            remaining_text = parts[1]
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes

def text_to_textnodes(text: str):
    nodes = split_nodes_link(split_nodes_image(split_nodes_delimiter(split_nodes_delimiter(split_nodes_delimiter([TextNode(text, TextType.TEXT)], '**', TextType.BOLD), "_", TextType.ITALIC), '`', TextType.CODE)))
    return nodes


# example = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a ![image](https://i.imgur.com/fJRaedVk.jpeg) and a [link](https://boot.dev)"


# print(text_to_textnodes(example))