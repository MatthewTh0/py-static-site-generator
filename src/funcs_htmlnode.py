# src/funcs_htmlnode.py

import re
from htmlnode import HTMLNode, ParentNode
from funcs_textnode import text_to_textnodes
from textnode import TextType, TextNode
from funcs_extract_markdown import markdown_to_blocks, block_to_block_type, BlockType


def container_for_headers(md_block:str) -> HTMLNode:
    foundTags = md_block.split(maxsplit=1)
    tagNum = len(foundTags[0])
    return ParentNode(f'h{tagNum}', [])

def container_from_block_type(blockType:BlockType) -> HTMLNode:
    match blockType:
        case BlockType.PARA:
            return ParentNode("p",[])
        case BlockType.ULIST:
            return ParentNode("ul", [])
        case BlockType.OLIST:
            return ParentNode("ol", [])
        case BlockType.CODE:
            return ParentNode("pre", [])
        case BlockType.QUOTE:
            return ParentNode("blockquote", [])
        case _:
            raise Exception("Invalid BlockType!")

# inline markdown to children
def text_to_children(text: str)->list[HTMLNode]:
    htmlNodeList = []
    # assign proper child  HTMLNode objects to the the block node
    textNodeLists = text_to_textnodes(text)
    
    for textNodeList in textNodeLists:
        htmlNodeList.append(textNodeList.to_html_node())
    return htmlNodeList

def inner_block_to_html_node(md_block:str, thisBlockType:BlockType) -> list[HTMLNode]:
    innerBlockChildren = [] 
    match thisBlockType:
        case BlockType.PARA:
            updated_md_block = md_block.replace("\n"," ")
        case BlockType.QUOTE:
            updated_md_block = re.sub(r"^>\s","",md_block)
            updated_md_block = updated_md_block.replace("\n> ","\n")
        case BlockType.ULIST:
            updated_md_block = re.sub(r"^-\s","",md_block)
            updated_md_block = updated_md_block.replace("\n- ","\n")
            split_updated_md_block = updated_md_block.split("\n")
            for list_item in split_updated_md_block:
                listChildren = text_to_children(list_item)
                listItemBlock = ParentNode("li",listChildren)
                innerBlockChildren.append(listItemBlock)
            return innerBlockChildren
        case BlockType.OLIST:
            updated_md_block = re.sub(r"^1.\s","", md_block)
            updated_md_block = re.sub(r"\n[0-9]+.\s","\n", updated_md_block)
            split_updated_md_block = updated_md_block.split("\n")
            for list_item in split_updated_md_block:
                listChildren = text_to_children(list_item)
                listItemBlock = ParentNode("li",listChildren)
                innerBlockChildren.append(listItemBlock)
            return innerBlockChildren
        case BlockType.HEAD:
            updated_md_block = re.sub(r"^#{1,6}\s","", md_block)
        case BlockType.CODE:
            updated_md_block = md_block.replace("```\n", "")
            updated_md_block = updated_md_block.replace("```","")
            tempTextNode = TextNode(updated_md_block, TextType.TEXT)
            codeBlock = tempTextNode.to_html_node()
            codeChild = ParentNode("code", [codeBlock])
            innerBlockChildren.append(codeChild)
            return innerBlockChildren
        case _:
            raise ValueError("Invalid/Unsupported Block Type!")
    innerBlockChildren.extend(text_to_children(updated_md_block))
    return innerBlockChildren
            
def markdown_to_html_node(md_doc:str) -> HTMLNode:
    containerChildren = []
    blockList = markdown_to_blocks(md_doc)
    for block in blockList:
        thisType = block_to_block_type(block)
        # creating container for around block
        if thisType==BlockType.HEAD:
            parentContainer = container_for_headers(block)
        else:
            parentContainer = container_from_block_type(thisType)
        innerBlockChildren = inner_block_to_html_node(block, thisType)
        if isinstance(parentContainer.children,list): 
            parentContainer.children.extend(innerBlockChildren)
        else:
            parentContainer.children = innerBlockChildren
        containerChildren.append(parentContainer)
    containerNode = ParentNode("div",containerChildren)
    trueResult = containerNode
    return trueResult




