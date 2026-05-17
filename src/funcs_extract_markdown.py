# src/extract_markdown.py

import re
from enum import Enum 

class BlockType(Enum):
    PARA = "paragraph"
    HEAD = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"

def extract_markdown_images(text) -> list[tuple[str,str]]:
    foundResult = re.findall(r"!\[(.*?)\]\((.*?)\)", text)    
    return foundResult 

def extract_markdown_links(text) -> list[tuple[str,str]]:
    foundResult = re.findall(r"(?<!\!)\[(.*?)\]\((.*?)\)", text)
    return foundResult

def markdown_to_blocks(markdown:str) -> list[str]:
    trueResult = []
    split_blocks = markdown.split("\n\n")
    for block in split_blocks:
        if block:
            trueResult.append(block.strip())
    return trueResult

def block_to_block_type(markdown_block:str)-> BlockType:
    foundBlockType = BlockType.PARA
    if re.search(r"(^>.*\n)*(^>.*)",markdown_block):
        foundBlockType = BlockType.QUOTE
    elif re.search(r"^(-.*\n)*(-.*)", markdown_block):
        foundBlockType = BlockType.ULIST
    elif re.search(r"^(1.*\n)([0-9]+.*\n)*([0-9]+.*)", markdown_block):
        foundBlockType = BlockType.OLIST
    elif markdown_block.startswith("```\n") and markdown_block.endswith("```"):
        foundBlockType = BlockType.CODE
    elif re.search(r"^#{1,6}\s",markdown_block):
        foundBlockType = BlockType.HEAD    
    return foundBlockType

def blocks_to_block_type_list_helper(markdown_blocks:list[str])-> list[BlockType]:
    blockTypeList = []
    for block in markdown_blocks:
        blockTypeList.append(block_to_block_type(block))
    return blockTypeList

def extract_title(markdown:str) -> str:
    foundResult = re.findall(r"^#\s([^\n]*)",markdown)
    return foundResult[0]
