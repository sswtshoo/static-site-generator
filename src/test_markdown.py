import unittest
from markdown import block_to_block_type, BlockType, markdown_to_blocks
from markdown_blocks import markdown_to_html_node, extract_title
class TestMarkdownBlock(unittest.TestCase):
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
            
    def test_markdown_to_blocks2(self):
        md = """
# This is the main heading

**This is some bold text**
_This is some italic text_

This is an ![image](https://i.imgur.com/3elNhQu.png)
This is a [link](https://google.com)
"""

        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [
                 "# This is the main heading",
                 "**This is some bold text**\n_This is some italic text_",
                 "This is an ![image](https://i.imgur.com/3elNhQu.png)\nThis is a [link](https://google.com)"
        ])
    
    def test_block_to_block_type(self):
        text = """
```
This is some code
```
"""
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, BlockType.CODE)

    def test_block_to_block_type2(self):
        text = """
> An eye for an eye makes the whole world blind. - MK Gandhi
> Ours is a world of nuclear giants and ethical infants. We know more about war than we know about peace, more about killing than we know about living. - Gen Omar Bradley
> The death of one man is a tragedy. The death of millions is a statistic. - Joseph Stalin
> Never think that war, no matter how necessary, nor how justified, is not a crime. - Ernest Hemingway
"""     
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, BlockType.QUOTE)

    
    def test_block_to_block_type3(self):
        text = """
### This is the start of something important
"""
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_to_block_type4(self):
        text = """
> You fucking die for 3 points. - Gandhi
-  This is not what I meant
> This is going to ruin the tour. - Justin Timberlake
""" 
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type5(self):
        text = """
1. A Girl Like You - Edwyn Collins
2. Stairway to Heaven - Led Zeppelin
3. Come As You Are - Nirvana
4. Californication - Red Hot Chilli Peppers
"""
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)


    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )
    
    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_headings(self):
        md = """
### This is the start of something important

There's a graveyard in northern France where all the dead boys from D-Day are buried. The white crosses reach from one horizon to the other. I remember looking it over and thinking it was a forest of graves. But the rows were like this, dizzying, diagonal, perfectly straight, so after all it wasn't a forest but an orchard of graves. Nothing to do with nature, unless you count human nature.
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
                        html,
        """<div><h3>This is the start of something important</h3><p>There's a graveyard in northern France where all the dead boys from D-Day are buried. The white crosses reach from one horizon to the other. I remember looking it over and thinking it was a forest of graves. But the rows were like this, dizzying, diagonal, perfectly straight, so after all it wasn't a forest but an orchard of graves. Nothing to do with nature, unless you count human nature.</p></div>"""
        )
    
    def test_ordered_list(self):
        md = """
1. A Girl Like You - Edwyn Collins
2. Stairway to Heaven - Led Zeppelin
3. Come As You Are - Nirvana
4. Californication - Red Hot Chilli Peppers
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>A Girl Like You - Edwyn Collins</li><li>Stairway to Heaven - Led Zeppelin</li><li>Come As You Are - Nirvana</li><li>Californication - Red Hot Chilli Peppers</li></ol></div>"
        )

    def test_quotes(self):
        md = """
> An eye for an eye makes the whole world blind. - MK Gandhi
""" 
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>An eye for an eye makes the whole world blind. - MK Gandhi</blockquote></div>"
        )

    def test_big_one(self):
        md = """
# This is H1

### This is H3

**The death of one man is a tragedy. The death of millions is a statistic.** - _Joseph Stalin_
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is H1</h1><h3>This is H3</h3><p><b>The death of one man is a tragedy. The death of millions is a statistic.</b> - <i>Joseph Stalin</i></p></div>"
        )

    def test_extract_title(self):
        md = """
# This is H1

### This is H3

**The death of one man is a tragedy. The death of millions is a statistic.** - _Joseph Stalin_
"""
        heading = extract_title(md)
        self.assertEqual(heading, 'This is H1')

    def test_extract_title2(self):
        md = """
# Favorite Songs

#   My Favorite Songs

1. A Girl Like You - Edwyn Collins
2. Stairway to Heaven - Led Zeppelin
3. Come As You Are - Nirvana
4. Californication - Red Hot Chilli Peppers
"""
        heading = extract_title(md)
        self.assertEqual(heading, 'My Favorite Songs')

    