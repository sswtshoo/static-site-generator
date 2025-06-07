import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test(self):
        node1 = HTMLNode('a', 'Hello World',props={'href': 'https://www.google.com', 'height': 200})
        self.assertEqual(node1.props_to_html(), 'href="https://www.google.com" height="200"')


    def test2(self):
        node1 = HTMLNode('a', 'Google', props={'href':'https://www.google.com'})
        self.assertEqual(node1.props_to_html(), 'href="https://www.google.com"')

    def test_eq(self):
        node1 = HTMLNode('p', "This is a paragraph", props={'size': 20})
        node2 = HTMLNode('p', "This is a paragraph", props={'size': 20})
        self.assertEqual(node1, node2)


class TestLeafNode(unittest.TestCase):
    def test(self):
        node = LeafNode('a','Google.com', props={'href':'https://www.google.com'})
        self.assertEqual('<a href="https://www.google.com">Google.com</a>', node.to_html())

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
         parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    def test_to_html_with_multi_children(self):
        child_node1 = LeafNode('h1', 'Main Heading')
        child_node2 = LeafNode('p', 'This is a p-tag')
        list_node1 = LeafNode('li', 'first point')
        list_node2 = LeafNode('li', 'second point')
        list_node3 = LeafNode('li', 'third point')
        child_node3 = ParentNode('ul', [list_node1, list_node2, list_node3])
        parent_node = ParentNode('div', [child_node1, child_node2, child_node3])

        self.assertEqual(
            parent_node.to_html(),
            "<div><h1>Main Heading</h1><p>This is a p-tag</p><ul><li>first point</li><li>second point</li><li>third point</li></ul></div>"
        )

    def test_to_html_with_multi_children2(self):
        child_node1 = LeafNode('h1', 'Main Heading')
        child_node2 = LeafNode('p', 'This is a p-tag')
        list_node1 = LeafNode('li', 'first point')
        list_node2 = LeafNode('li', 'second point')
        list_node3 = LeafNode('li', 'third point')
        child_node3 = ParentNode('ul', [list_node1, list_node2, list_node3])
        child_node4 = LeafNode('img','', props={'src': 'www.google.com', 'alt': 'a photo'})
        parent_node = ParentNode('div', [child_node1, child_node2, child_node3, child_node4])
        self.assertEqual(parent_node.to_html(),
            '<div><h1>Main Heading</h1><p>This is a p-tag</p><ul><li>first point</li><li>second point</li><li>third point</li></ul><img src="www.google.com" alt="a photo"/></div>'
        )