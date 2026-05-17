# src/test_extractmarkdown.py

import unittest

from funcs_extract_markdown import extract_title,extract_markdown_images, extract_markdown_links, markdown_to_blocks, BlockType, blocks_to_block_type_list_helper



class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_demo_image(self):
        extractedImage = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")],extractedImage)

    def test_extract_markdown_demo_link(self):
        extractedLink = extract_markdown_links(
            "This is a text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")],extractedLink)

    def test_extract_markdown_links(self):
        extractedLink = extract_markdown_links(
            "This is a text with a link [to google](https://www.google.com)"
        )
        self.assertListEqual([("to google", "https://www.google.com")], extractedLink)

    def test_extract_markdown_mixed_links(self):
        extractedLink = extract_markdown_links(
            "This is a text with a link [to boot dev](https://www.boot.dev) and an image of a flower. ![flower image](https://www.gstatic.com/webp/gallery3/1.png)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], extractedLink)

    def test_extract_mixedImage(self):
        extractedImage = extract_markdown_images(
            "This is a text with a link [to boot dev](https://www.boot.dev) and an image of a flower. ![flower image](https://www.gstatic.com/webp/gallery3/1.png)"
        )
        self.assertListEqual([("flower image", "https://www.gstatic.com/webp/gallery3/1.png")],extractedImage)
        
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

    def test_markdown_to_blocks_gap(self):
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

    def test_markdown_to_block_types(self):
        md = """
```
dkajfl;djaflk
```

- This is a list
- with items

> A quote here
> keeps doctors away

1. Yes
2. No

### My Heading

Blah Blah

"""
        blocks = markdown_to_blocks(md)
        blockTypeList = blocks_to_block_type_list_helper(blocks)
        self.assertListEqual(blockTypeList, [BlockType.CODE,BlockType.ULIST,BlockType.QUOTE,BlockType.OLIST,BlockType.HEAD,BlockType.PARA])

    def test_markdown_to_block_types_other(self):
        md = """
> FOR
> THE
> EMPEROR

Pargraph here! Ok, maybe
just a few sentences.

- Example
- of
- Unordered 
- List

1. Now, order
2. Yes, order
3. Maybe order?

## Programming Below!

```
blocks = markdown_to_blocks(md)
```

"""
        blocks = markdown_to_blocks(md)
        blockTypeList = blocks_to_block_type_list_helper(blocks)
        self.assertListEqual(blockTypeList, [BlockType.QUOTE,BlockType.PARA, BlockType.ULIST,BlockType.OLIST,BlockType.HEAD,BlockType.CODE])

    def test_extract_title_easy(self):
        found = extract_title("# Hello")
        self.assertEqual(found, "Hello")

    def test_extract_title_medium(self):
        found = extract_title("""# I am doing FINE
                              But what about you?
                              """)
        self.assertEqual(found, "I am doing FINE")

if __name__ == "__main__":
    unittest.main()

    