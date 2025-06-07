from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "normal text"
    BOLD = "**Bold Text**"
    ITALIC = "_Italic Text_"
    CODE = "`Code Text`"
    LINK = "[anchor text](url)"
    IMAGE = "![alt text](url)"

class TextNode():
    def __init__(self, text: str, text_type: TextType, url=""):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if (self.text == other.text and self.text_type == other.text_type and self.url == other.url):
            return True
        return False
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
    
   
    
def text_node_to_html_node(text_node:TextNode):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(tag = None,value = text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode(tag = 'b', value = text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode(tag = 'i', value = text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode(tag = 'code', value = text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode(tag = 'a', value = text_node.text, props = {'href':text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode(tag = 'img', value="", props = {'src': text_node.url, 'alt': text_node.text})
    else:
        raise Exception('invalid text type')