from enum import Enum
from htmlnode import LeafNode


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():
    def __init__(self, text: str, text_type: TextType, url:str|None=None) -> None:
        self.text =text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, TextNode):
            if self.text == other.text and self.text_type==other.text_type and self.url==other.url:
                return True
        return False
    
    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

    def to_html_node(self) -> LeafNode:
        match self.text_type:
            case TextType.TEXT:
                return LeafNode(None,self.text)
            case TextType.BOLD:
                return LeafNode("b",self.text)
            case TextType.ITALIC:
                return LeafNode("i", self.text)
            case TextType.CODE:
                return LeafNode("code", self.text)
            case TextType.LINK:
                return LeafNode("a", self.text, {"href": self.url})
            case TextType.IMAGE:
                return LeafNode("img", "", {"src": self.url, "alt": self.text})
            case _:
                raise ValueError("Not one of recognized text node types!")
            
    