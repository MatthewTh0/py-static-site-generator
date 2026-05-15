#src/test_htmlnode.py
import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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
        parent_node = ParentNode("div", [None])
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

if __name__ == "__main__":
    unittest.main()