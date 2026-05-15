import unittest

from textnode import TextNode, TextType, split_nodes_delimiter
from htmlnode import LeafNode

def broken_function():
        raise Exception('This is broken')

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_type_neq(self):
        node = TextNode("This is a text node", TextType.LINK, "https://www.google.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://www.google.com")
        self.assertNotEqual(node,node2)
    
    def test_text_neq(self):
        node = TextNode("This is right", TextType.TEXT)
        node2 = TextNode("This is wrong", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_type_image_to_html(self):
        node = TextNode("This is a stock flower from Google", TextType.IMAGE, "https://www.gstatic.com/webp/gallery3/1.png")
        html_node = node.to_html_node()
        self.assertEqual(html_node, LeafNode("img","", {"src": "https://www.gstatic.com/webp/gallery3/1.png", "alt": "This is a stock flower from Google"}))
        
    def test_text_to_html(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = node.to_html_node()
        self.assertEqual(html_node, LeafNode(None,"This is a text node"))
    
    def test_split_node_italic_delim_test(self):
        italicNode = TextNode("This is a test with a _italic looking_ word", TextType.TEXT) 
        result = split_nodes_delimiter([italicNode],"_", TextType.ITALIC)
        expectedResult=[
            TextNode("This is a test with a ", TextType.TEXT),
            TextNode("italic looking", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
        ]
        #print(f'result=\n{result}\nvs\nexpectedresult=\n{expectedResult}')
        self.assertEqual(expectedResult,result)
        #print("It worked?")

    def test_split_node_bold_delim_test(self):
        boldNode = TextNode("This is text with a **bold bored** word", TextType.TEXT)
        result = split_nodes_delimiter([boldNode],"**", TextType.BOLD)
        expectedResult=[
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold bored", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ]

        self.assertEqual(expectedResult,result)

    def test_split_node_code_delim_test(self):
        codeNode = TextNode("This is text with a `code block` word", TextType.TEXT)
        result = split_nodes_delimiter([codeNode],"`", TextType.CODE)
        expectedResult=[
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]

        self.assertEqual(expectedResult,result)
        #
        # Tried to have error raising verified, but idk doesn't work
    def test_split_node_invalid_delim_test(self):
        #with self.assertRaises(Exception) as context:
        invalidNode = TextNode("This is text with a `code block word", TextType.TEXT)
       
        with self.assertRaises(ValueError) as context:
            # broken function ()
            split_nodes_delimiter([invalidNode],"`", TextType.CODE)
        #print(f'Found exception perhaps: {str(context.exception)} {context.exception}')    
        self.assertTrue('Invalid markdown syntax! One or less found of delimiter in old_node.text' in str(context.exception))

    def test_text_error_to_html(self):
        wrongTypeNode = TextNode("Blah", "hello") # type: ignore
        with self.assertRaises(ValueError) as context:
            wrongTypeNode.to_html_node()
        self.assertTrue('Not one of recognized text node types!' in str(context.exception))

     
    def test_multi_split(self):
        codeBoldNode = TextNode("This is text with a `code block` and **bold bored** words in it.", TextType.TEXT)
        codeDelimited = split_nodes_delimiter([codeBoldNode],"`", TextType.CODE)
        
        boldDelimited = split_nodes_delimiter([codeDelimited[2]],"**", TextType.BOLD)
        expectedResult=[
            TextNode("This is text with a ", TextType.TEXT ),
            TextNode("code block", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("bold bored", TextType.BOLD),
            TextNode(" words in it.", TextType.TEXT),
        ]
        fullResult = []
        fullResult.append(codeDelimited[0])
        fullResult.append(codeDelimited[1])
        fullResult.extend(boldDelimited)
        self.assertEqual(expectedResult,fullResult)


    def test_mechanic(self):
        with self.assertRaises(Exception) as context:
            broken_function()

        self.assertTrue('This is broken' in str(context.exception))
     
        # expectedResult=[
        #    TextNode("This is text with a ", TextType.TEXT),
        #    TextNode("code block", TextType.CODE),
        #    TextNode(" word", TextType.TEXT),
        #]

        #self.assertEqual(expectedResult,result)
        #print("It worked?")
        # Below doest't work
        #def test_text_error_to_html(self):
        #    node = TextNode("Blah", "hello") # type: ignore
        #    self.assertRaises(ValueError,TextNode("Blah", "hello").to_html_node())


if __name__ == "__main__":
    unittest.main()