import unittest

from textnode import TextNode, TextType
from funcs_textnode import split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes
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
        self.assertEqual(expectedResult,result)

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
        
    def test_split_node_invalid_delim_test(self):
        invalidNode = TextNode("This is text with a `code block word", TextType.TEXT)
       
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter([invalidNode],"`", TextType.CODE) 
        self.assertTrue('Invalid markdown syntax! Odd number of delimiters found in old_node.text' in str(context.exception))

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

    def test_multi_split_alternate_method(self):
        codeBoldNode = TextNode("This is text with a `code block` and **bold bored** words in it.", TextType.TEXT)
        codeDelimited = split_nodes_delimiter([codeBoldNode],"`", TextType.CODE)
        boldDelimited = split_nodes_delimiter(codeDelimited,"**", TextType.BOLD)
        
        expectedResult=[
            TextNode("This is text with a ", TextType.TEXT ),
            TextNode("code block", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("bold bored", TextType.BOLD),
            TextNode(" words in it.", TextType.TEXT),
        ]
        self.assertEqual(expectedResult, boldDelimited)

    def test_split_italic_at_beginning_and_end(self):
        codeItalicTest = TextNode("_An unpopular opinion, I know._", TextType.TEXT)
        codeDelimited = split_nodes_delimiter([codeItalicTest],"_",TextType.ITALIC)
        expectedResult = [
            TextNode("An unpopular opinion, I know.", TextType.ITALIC)
        ]
        #print("HEREE")
        self.assertEqual(codeDelimited,expectedResult)

    def test_multi_code_delim_with_delim_at_end(self):
        codeDoubleNode = TextNode("This is text with not just `one code block` but `two code blocks`", TextType.TEXT)
        codeDelimited = split_nodes_delimiter([codeDoubleNode], "`", TextType.CODE)
        exceptedResult =[
            TextNode("This is text with not just ", TextType.TEXT ),
            TextNode("one code block", TextType.CODE),
            TextNode(" but ", TextType.TEXT),
            TextNode("two code blocks", TextType.CODE),
        ]
        self.assertEqual(codeDelimited, exceptedResult)

    def test_multi_code_delim_with_delim_not_and_edges(self):
        codeTripleNode = TextNode("This is text with not just `one code block` but `two code blocks` with words in it.", TextType.TEXT)
        codeDelimited = split_nodes_delimiter([codeTripleNode], "`", TextType.CODE)
        exceptedResult =[
            TextNode("This is text with not just ", TextType.TEXT ),
            TextNode("one code block", TextType.CODE),
            TextNode(" but ", TextType.TEXT),
            TextNode("two code blocks", TextType.CODE),
            TextNode(" with words in it.", TextType.TEXT),
        ]
        self.assertEqual(codeDelimited, exceptedResult)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with one [to boot dev](https://www.boot.dev) link and another [to google](https://www.google.com) link",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with one ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" link and another ", TextType.TEXT),
                TextNode(
                    "to google", TextType.LINK, "https://www.google.com"
                ),
                TextNode(" link", TextType.TEXT)
            ],
            new_nodes,
        )

    def test_extract_mixedLink(self):
        node = TextNode(
            "This is a text with a link [to boot dev](https://www.boot.dev) and an image of a flower. ![flower image](https://www.gstatic.com/webp/gallery3/1.png)",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is a text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and an image of a flower. ![flower image](https://www.gstatic.com/webp/gallery3/1.png)", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_extract_mixedImage(self):
        node = TextNode(
            "This is a text with a link [to boot dev](https://www.boot.dev) and an image of a flower. ![flower image](https://www.gstatic.com/webp/gallery3/1.png)",
            TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is a text with a link [to boot dev](https://www.boot.dev) and an image of a flower. ", TextType.TEXT),
                TextNode("flower image", TextType.IMAGE, "https://www.gstatic.com/webp/gallery3/1.png"),
            ],
            new_nodes,
        )

    def test_multiple_types(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and **bold text**! Wow!",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        last_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and ", TextType.TEXT),
                TextNode("bold text", TextType.BOLD),
                TextNode("! Wow!", TextType.TEXT)
            ],
            last_nodes,
        )

    def test_mechanic(self):
        with self.assertRaises(Exception) as context:
            broken_function()

        self.assertTrue('This is broken' in str(context.exception))

    def test_complete_package(self):
        text= "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        expected_result = [
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
        ]
        self.assertEqual(new_nodes, expected_result)

    def test_partial_package(self):
        text= "This is **text** with an _italic_ word and a `code block`"
        new_nodes = text_to_textnodes(text)
        expected_result = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
        ]
        self.assertEqual(new_nodes, expected_result)

    def test_partial_delim_package_multiples(self):
        text= "This is **bold** text that also has _italic_ text. Very **beautiful**. _Very_."
        new_nodes = text_to_textnodes(text)
        expected_result = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text that also has ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text. Very ", TextType.TEXT),
            TextNode("beautiful", TextType.BOLD),
            TextNode(". ", TextType.TEXT),
            TextNode("Very", TextType.ITALIC),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected_result)

    def test_partial_package_multiples_delim_and_images(self):
        text= "This is a `code` block, an image ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg), another `code` block, and a last image ![flower image](https://www.gstatic.com/webp/gallery3/1.png)"
        new_nodes = text_to_textnodes(text)
        expected_result = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" block, an image ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(", another ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" block, and a last image ", TextType.TEXT),
            TextNode("flower image", TextType.IMAGE, "https://www.gstatic.com/webp/gallery3/1.png"),
        ]
        self.assertEqual(new_nodes, expected_result)

if __name__ == "__main__":
    unittest.main()