# src/htmlnode.py

class HTMLNode():
    def __init__(self, tag: str|None=None, value: str|None=None, children:list['HTMLNode']|None=None, props: dict|None=None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError

    def props_to_html(self) -> str:
        htmlFound=""
        if self.props:
            for prop in self.props:
                htmlFound+=f' {prop}="{self.props[prop]}"'
        return htmlFound

    def __eq__(self, other: object) -> bool:
        if isinstance(other, HTMLNode):
            if self.tag == other.tag and self.value==other.value and self.children==other.children and self.props==other.props:
                return True
        return False
    
    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    

class LeafNode(HTMLNode):
    def __init__(self, thisTag: str|None, thisValue: str, thisProps: dict|None=None) -> None:
        super().__init__(value=thisValue, tag=thisTag, props=thisProps)
    
    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        if not self.tag:
            return self.value
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
    
    def __repr__(self) -> str:
        return f"HTMLLeafNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
    def __init__(self, thisTag: str | None, thisChildren: list['HTMLNode'] | None, thisProps: dict | None = None) -> None:
        super().__init__(tag=thisTag, children=thisChildren, props=thisProps)

    def to_html(self) -> str:
        if not self.tag:
            raise ValueError("All parent nodes must have a tag")
        elif not self.children:
            raise ValueError("All parent nodes must have children")
        else:
            htmlFound = f'<{self.tag}>'
            for childNode in self.children:
                if isinstance(childNode, HTMLNode):
                    htmlFound+=childNode.to_html()
            htmlFound += f'</{self.tag}>'
            return htmlFound
