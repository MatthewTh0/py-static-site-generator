# main.py

from textnode import TextNode, TextType

def main():
    print("# hello world")
    testTextNode = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    
    print(testTextNode)


main()