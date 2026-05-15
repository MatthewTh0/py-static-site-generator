from enum import Enum
from htmlnode import LeafNode
from extract_markdown  import extract_markdown_images, extract_markdown_links

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
            
    


# !FIX BELOW


def split_nodes_delimiter(old_nodes:list[TextNode], delimiter:str, text_type:TextType) -> list[TextNode]:
    trueResult=[]
    for old_node in old_nodes:
        if old_node.text_type!=TextType.TEXT:
            # only try to split text nodes
            trueResult.append(old_node)
        else:
            split_node = old_node.text.split(delimiter)
            counter = 0
            resultNodes = []
            split_node_len = len(split_node)
            if split_node_len<3:
                trueResult.append(old_node)
                raise ValueError(f'Invalid markdown syntax! One or less found of delimiter in old_node.text')
            beginSymbol = split_node[0]
            endSymbol = split_node[split_node_len-1]
            nextIsSpecial = False
            if not beginSymbol:
                nextIsSpecial= True
            while counter<split_node_len:
                if not split_node[counter]:
                    nextIsSpecial = not nextIsSpecial
                    counter+=1
                    continue
                elif nextIsSpecial:
                    resultNodes.append(TextNode(split_node[counter], text_type))
                else: # is noo nextisspecial
                    resultNodes.append(TextNode(split_node[counter], TextType.TEXT))
                nextIsSpecial = not nextIsSpecial
                counter+=1

                   #elif split_node_len%2==1: 
            #    while counter<split_node_len:
            #        if not split_node[counter]:
                        # empty section, therefore

                        #counter+1==1
           #         elif counter%2==0:
                      #  resultNodes.append(TextNode(split_node[counter], TextType.TEXT))
           #         else:
                     #   resultNodes.append(TextNode(split_node[counter], text_type))
            #        counter+=1          
                

            # if empty string at beginning means next is code block
            
            
           
                #resultNodes.append(TextNode(split_node[1], text_type))
                #resultNodes.append(TextNode(split_node[2], TextType.TEXT))
                
            # case 1
            #  0     1      2 = len 3
            # `code` and `code2`
            # case 2
            #   0    1     2       3 = len 4
            # `code` and `code2` also
            # case 3
            #  0     1    2     3 = len 4
            # also `code` and `code2`
            # case 4
            # 0     1     2     3      4 = len 5
            # also `code` and `code2` also 
            # case 5
            #   0     1
            # `code` and
            # case 6
            #  0   1
            # and `code`
            # case 7
            #   0
            # `code`
            # case 8
            #  0
            # and

            trueResult.extend(resultNodes)
            #else:
             #   raise NotImplementedError("Not yet supported")
              #  if le
             #   trueResult.extend()
            #print(f"We got this! Here's the split {split_node}")
            
        # if matching closing delimter not found, raise Exception about invalid md syntax
        #else:
            #trueResult.
            #if find
        # .split
        # .extend() ?

    return trueResult
        
    # result = [
   # TextNode("This is text with a ", TextType.TEXT),
  #  TextNode("code block", TextType.CODE),
  # TextNode(" word", TextType.TEXT),
  #  ]
  #  return result

def split_nodes_image(old_nodes:list[TextNode]) -> list[TextNode]:
    trueResult=[]
    for old_node in old_nodes:
        if old_node.text_type!=TextType.TEXT:
            trueResult.append(old_node)
        else:
            
            altProp,srcProp = extract_markdown_images(old_node.text)
            
            #if len(split_node)<3:
            #    trueResult.append(old_node)
            #    raise ValueError(f'Invalid markdown syntax! One or less found of delimiter in old_node.text')
            #elif len(split_node)==3: 
            #    resultNodes=[]
            #    resultNodes.append(TextNode(split_node[0], TextType.TEXT))
            #    resultNodes.append(TextNode(split_node[1], text_type))
            #    resultNodes.append(TextNode(split_node[2], TextType.TEXT))

            #    trueResult.extend(resultNodes)
            #else:
           #     raise NotImplementedError("Not yet supported")
    return trueResult

def split_nodes_link(old_nodes:list[TextNode]) -> list[TextNode]:
    trueResult=[]
    for old_node in old_nodes:
        if old_node.text_type!=TextType.TEXT:
            trueResult.append(old_node)
        else:
            #anchorText,hrefProp =
            linkInfo = extract_markdown_links(old_node.text)
            if len(linkInfo)<1:
                trueResult.append(old_node)
                raise ValueError(f'No links found')
            else:

                #split_= old_node.text.split()
                for anchorText, hrefProp in linkInfo:
                    sections= old_node.text.split(f"![{anchorText}]({hrefProp})",1)
                    trueResult.append(TextNode(sections[0],TextType.TEXT))
                    # what if nothing before, won't above fail
                    trueResult.append(TextNode(anchorText,TextType.LINK,hrefProp))
                    #how do I handle what comes after the last one?
                    #HELP
                    
                    #trueResult.append(TextNode())

                #resultNodes=[]
                #resultNodes.append(TextNode(split_node[0], TextType.TEXT))
                #resultNodes.append(TextNode(split_node[1], text_type))
                #resultNodes.append(TextNode(split_node[2], TextType.TEXT))

                #trueResult.extend(resultNodes)
            #else:
            #    raise NotImplementedError("Not yet supported")
    print(f'True result of {old_nodes} to new {trueResult}')
    return trueResult