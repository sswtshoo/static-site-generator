import unittest
from textnode import TextType, TextNode, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is one node", TextType.LINK)
        node2 = TextNode("This is another node", TextType.IMAGE)
        self.assertNotEqual(node, node2)

    def test_text_type(self):
        node = TextNode("This is a node", TextType.CODE)
        node2 =  TextNode("This is a node", TextType.LINK)
        self.assertNotEqual(node, node2)
    
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_image(self):
        node = TextNode("This is image alt", TextType.IMAGE, url="www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'img')
        self.assertEqual(html_node.props['src'], "www.google.com")
    


    

if __name__ == "__main__":
    unittest.main()