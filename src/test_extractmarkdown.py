# src/test_extractmarkdown.py

import unittest

from extract_markdown import extract_markdown_images, extract_markdown_links

class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
        #print("1 no exists")

    def test_extract_markdown_demo_image(self):
        extractedImage = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")],extractedImage)
        #print("2 is first?")

    def test_extract_markdown_demo_link(self):
        extractedLink = extract_markdown_links(
            "This is a text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")],extractedLink)
        #print("3")

    def test_extract_markdown_links(self):
        extractedLink = extract_markdown_links(
            "This is a text with a link [to google](https://www.google.com)"
        )
        self.assertListEqual([("to google", "https://www.google.com")], extractedLink)
        #print("4")

    def test_extract_markdown_mixed_links(self):
        extractedLink = extract_markdown_links(
            "This is a text with a link [to boot dev](https://www.boot.dev) and an image of a flower. ![flower image](https://www.gstatic.com/webp/gallery3/1.png)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], extractedLink)

    def test_extract_mixedImage(self):
        extractedImage = extract_markdown_images(
            "This is a text with a link [to boot dev](https://www.boot.dev) and an image of a flower. ![flower image](https://www.gstatic.com/webp/gallery3/1.png)"
        )
        #print("I was here")
        self.assertListEqual([("flower image", "https://www.gstatic.com/webp/gallery3/1.png")],extractedImage)
        

if __name__ == "__main__":
    unittest.main()

    