import unittest

from inline_md import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes
from textnode import TextType, TextNode

class TestExtract(unittest.TestCase):
    def test_bold(self):
        node = TextNode('This is a **bold text** and this is **another**', TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], '**', TextType.BOLD)
        self.assertEqual(new_nodes, [TextNode('This is a ', TextType.TEXT), TextNode('bold text', TextType.BOLD), TextNode(' and this is ', TextType.TEXT), TextNode('another', TextType.BOLD)])

    def test_bold_mult(self):
        node = TextNode("**Start** middle **End**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], '**', TextType.BOLD)
        self.assertEqual(new_nodes, [TextNode('Start', TextType.BOLD), TextNode(' middle ', TextType.TEXT), TextNode('End', TextType.BOLD)])

    def test_code(self):
        node1 = TextNode("`init` in the beginning and `exit` at the end", TextType.TEXT)
        node2 = TextNode("`first` then `second`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node1, node2], '`', TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode('init', TextType.CODE), TextNode(' in the beginning and ', TextType.TEXT), TextNode('exit', TextType.CODE), TextNode(' at the end', TextType.TEXT), TextNode('first', TextType.CODE), TextNode(' then ', TextType.TEXT), TextNode('second', TextType.CODE)
        ])

    def test_italic(self):
        node = TextNode("_Entire sentence in italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node],'_', TextType.ITALIC)
        self.assertEqual(new_nodes, [TextNode('Entire sentence in italic', TextType.ITALIC)])

    def test_extract_md_image(self):
        text =  "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        self.assertEqual(extract_markdown_images(text), [("image", "https://i.imgur.com/zjjcJKZ.png")])

    def test_extract_md_link(self):
        text = "This is some text with a [link](https://imgur.com/gallery/when-real-person-finds-phone-kclxhSE#ZoMcj5u)"
        self.assertEqual(extract_markdown_links(text), [("link", "https://imgur.com/gallery/when-real-person-finds-phone-kclxhSE#ZoMcj5u")])

    def test_extract_md_images(self):
        text = "This is the ![first](https://unsplash.com/photos/blue-and-white-classic-cars-rear-end-pu8MDF91KH4) and this is the ![second](https://unsplash.com/photos/a-modern-kitchen-with-natural-light--ha9LWGj_EU)"
        self.assertEqual(extract_markdown_images(text), [(
            'first', 'https://unsplash.com/photos/blue-and-white-classic-cars-rear-end-pu8MDF91KH4'
        ),
        (
            'second', 'https://unsplash.com/photos/a-modern-kitchen-with-natural-light--ha9LWGj_EU'
        )])

    def test_extract_md_links(self):
        text = "This is [song 1](https://youtu.be/Dy4HA3vUv2c?si=Og-79HTLpive8lIY), this is [song 2](https://youtu.be/Ty9Pcg3qrmU?si=V-3wtKIp27SAzu2k)"
        self.assertEqual(extract_markdown_links(text), [
            ("song 1", "https://youtu.be/Dy4HA3vUv2c?si=Og-79HTLpive8lIY"),
            ("song 2", "https://youtu.be/Ty9Pcg3qrmU?si=V-3wtKIp27SAzu2k")
        ])

    def test_extract_image(self):
        node = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)", TextType.TEXT)
        self.assertEqual(split_nodes_image([node]), [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode(
                "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
            ),
        ])

    def test_extract_images(self):
        node = TextNode("This is some text with ![first image](https://unsplash.com/photos/blue-and-white-classic-cars-rear-end-pu8MDF91KH4), this is ![second image](https://unsplash.com/photos/a-modern-kitchen-with-natural-light--ha9LWGj_EU) and here is some extra text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(new_nodes, 
                         [
                             TextNode('This is some text with ', TextType.TEXT),
                             TextNode('first image', TextType.IMAGE, 'https://unsplash.com/photos/blue-and-white-classic-cars-rear-end-pu8MDF91KH4'),
                             TextNode(', this is ', TextType.TEXT),
                             TextNode('second image', TextType.IMAGE, 'https://unsplash.com/photos/a-modern-kitchen-with-natural-light--ha9LWGj_EU'),
                             TextNode(' and here is some extra text', TextType.TEXT)
                         ])


    def test_extract_images_nodes(self):
        node1 = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)", TextType.TEXT)
        node2 = TextNode("This is some text with ![first image](https://unsplash.com/photos/blue-and-white-classic-cars-rear-end-pu8MDF91KH4), this is ![second image](https://unsplash.com/photos/a-modern-kitchen-with-natural-light--ha9LWGj_EU) and here is some extra text", TextType.TEXT)
        new_nodes= split_nodes_image([node1, node2])
        self.assertEqual(new_nodes, [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode(
                "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
            ),
            TextNode('This is some text with ', TextType.TEXT),
            TextNode('first image', TextType.IMAGE, 'https://unsplash.com/photos/blue-and-white-classic-cars-rear-end-pu8MDF91KH4'),
            TextNode(', this is ', TextType.TEXT),
            TextNode('second image', TextType.IMAGE, 'https://unsplash.com/photos/a-modern-kitchen-with-natural-light--ha9LWGj_EU'),
            TextNode(' and here is some extra text', TextType.TEXT)
        ])

    def test_extract_links(self):
        node = TextNode("This is [song 1](https://youtu.be/Dy4HA3vUv2c?si=Og-79HTLpive8lIY), this is [song 2](https://youtu.be/Ty9Pcg3qrmU?si=V-3wtKIp27SAzu2k)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes, [
            TextNode('This is ', TextType.TEXT), 
            TextNode('song 1', TextType.LINK, 'https://youtu.be/Dy4HA3vUv2c?si=Og-79HTLpive8lIY'),
            TextNode(', this is ', TextType.TEXT),
            TextNode('song 2', TextType.LINK, 'https://youtu.be/Ty9Pcg3qrmU?si=V-3wtKIp27SAzu2k')
        ])

    def test_extract_links_nodes(self):
        node1 = TextNode("This is [song 1](https://youtu.be/Dy4HA3vUv2c?si=Og-79HTLpive8lIY), this is [song 2](https://youtu.be/Ty9Pcg3qrmU?si=V-3wtKIp27SAzu2k)", TextType.TEXT)
        node2 = TextNode("This is text with an [image](https://i.imgur.com/zjjcJKZ.png) and another [second image](https://i.imgur.com/3elNhQu.png)", TextType.TEXT)
        new_nodes = split_nodes_link([node1, node2])
        self.assertEqual(new_nodes,[
            TextNode('This is ', TextType.TEXT), 
            TextNode('song 1', TextType.LINK, 'https://youtu.be/Dy4HA3vUv2c?si=Og-79HTLpive8lIY'),
            TextNode(', this is ', TextType.TEXT),
            TextNode('song 2', TextType.LINK, 'https://youtu.be/Ty9Pcg3qrmU?si=V-3wtKIp27SAzu2k'),
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second image", TextType.LINK, "https://i.imgur.com/3elNhQu.png")
        ])

    def test_text_to_nodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertEqual(nodes, [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ])

    def test_text_to_nodes2(self):
        text = "Start with plain text, then _italic_, then **bold**, then  + “inline code,” +  followed by [a cool link](https://google.com), and a ![nice image](https://placekitten.com/300/300)"
        nodes = text_to_textnodes(text)
        self.assertEqual(nodes, [
            TextNode("Start with plain text, then ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(", then ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(", then  + “inline code,” +  followed by ", TextType.TEXT),
            TextNode("a cool link", TextType.LINK, "https://google.com"),
            TextNode(", and a ", TextType.TEXT),
            TextNode("nice image", TextType.IMAGE, "https://placekitten.com/300/300"),
        ])

    def test_text_to_nodes3(self):
        text = "_Italic start_ and then **bold inside**, plus  + “code block,” +  and here’s a combo of [link1](https://link1.com), [link2](https://link2.com), and ![img1](https://img1.com/img.png), all together."
        nodes = text_to_textnodes(text)
        self.assertEqual(nodes, [
            TextNode("Italic start", TextType.ITALIC),
            TextNode(" and then ", TextType.TEXT),
            TextNode("bold inside", TextType.BOLD),
            TextNode(", plus  + “code block,” +  and here’s a combo of ", TextType.TEXT),
            TextNode("link1", TextType.LINK, "https://link1.com"),
            TextNode(", ", TextType.TEXT),
            TextNode("link2", TextType.LINK, "https://link2.com"),
            TextNode(", and ", TextType.TEXT),
            TextNode("img1", TextType.IMAGE, "https://img1.com/img.png"),
            TextNode(", all together.", TextType.TEXT),
        ])