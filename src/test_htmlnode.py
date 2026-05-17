#src/test_htmlnode.py
import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode
from funcs_htmlnode import markdown_to_html_node

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode(tag="p")
        node2 = HTMLNode(tag="p")
        self.assertEqual(node, node2)

    def test_tag_neq(self):
        node = HTMLNode(tag="a")
        node2 = HTMLNode(tag="h1")
        self.assertNotEqual(node,node2)
    
    def test_props_neq(self):
        node = HTMLNode(props={"target": "_blank"})
        node2 = HTMLNode(props={"href": "https://www.google.com"})
        self.assertNotEqual(node, node2)

    # Leaf tests
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href":"https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')    

    def test_leaf_to_html_b(self):
        node = LeafNode("b", "I'm bold!")
        self.assertEqual(node.to_html(), "<b>I'm bold!</b>")    

    # Parent/child test
    def test_to_html_multiple_children(self):
        node = ParentNode(
        "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )   
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")
    
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_no_tag(self):
        child_node = LeafNode("b", "grandchild")
        parent_node = ParentNode("",thisChildren=[child_node])
        self.assertRaises(ValueError)

    def test_to_html_with_no_children(self):
        parent_node = ParentNode("div", None)
        self.assertRaises(ValueError)

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_multiple_layers(self):
        granddaughter_node = LeafNode("b", "granddaughter")
        grandson_node = LeafNode("b","grandson")
        sibling_node = LeafNode("div", "sibling")
        child_node = ParentNode("span", [granddaughter_node,grandson_node])
        parent_node = ParentNode("div", [child_node, sibling_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>granddaughter</b><b>grandson</b></span><div>sibling</div></div>",
        )

    def test_markdown_to_html_node_paragraphs(self):
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

    def test_heading_and_quotes(self):
            md = """
### This _is_ **pretty** special

> One small step for a man
> One giant step for mankind
> Neil Armstrong
"""

            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
                html,
                "<div><h3>This <i>is</i> <b>pretty</b> special</h3><blockquote>One small step for a man\nOne giant step for mankind\nNeil Armstrong</blockquote></div>",
            )
    
    def test_ordered_and_unordered_lists(self):
            md = """
- This _is_ an
- unordered list

1. But this **is**
2. Ordered
3. Yep
"""

            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
                html,
                "<div><ul><li>This <i>is</i> an</li><li>unordered list</li></ul><ol><li>But this <b>is</b></li><li>Ordered</li><li>Yep</li></ol></div>",
            )

if __name__ == "__main__":
    unittest.main()