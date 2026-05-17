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
    #text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
    foundResult = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
                             #r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    
    return foundResult #[("rick roll", "Httpsdfk;jd;"), ("kdfj;", "dkf;jldjfs")]

def extract_markdown_links(text) -> list[tuple[str,str]]:
    #testText 
    #test = "This is a text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    foundResult = re.findall(r"(?<!\!)\[(.*?)\]\((.*?)\)", text)
    return foundResult
    #return [("rick roll", "Httpsdfk;jd;"), ("kdfj;", "dkf;jldjfs")]

def markdown_to_blocks(markdown:str) -> list[str]:
    trueResult = []
    split_blocks = markdown.split("\n\n")
    #print(split_blocks)
    for block in split_blocks:
        if block:
            trueResult.append(block.strip())
    return trueResult

def block_to_block_type(markdown_block:str)-> BlockType:
    foundBlockType = BlockType.PARA
    #print(markdown_block)
    if re.search(r"(^>.*\n)*(^>.*)",markdown_block):
        foundBlockType = BlockType.QUOTE
    #if markdown_block.startswith("#"):
    #    #maybe heading
    #    foundBlockType = BlockType.HEAD
    elif re.search(r"^(-.*\n)*(-.*)", markdown_block):
        foundBlockType = BlockType.ULIST
    elif re.search(r"^(1.*\n)([0-9]+.*\n)*([0-9]+.*)", markdown_block):
        foundBlockType = BlockType.OLIST
    elif markdown_block.startswith("```\n") and markdown_block.endswith("```"):
        #TODO make better version
        foundBlockType = BlockType.CODE
    elif re.search(r"^#{1,6}\s",markdown_block):
        foundBlockType = BlockType.HEAD
    
    
    #
    #else:
        #do nothing normal paragraph    

    return foundBlockType

def blocks_to_block_type_list_helper(markdown_blocks:list[str])-> list[BlockType]:
    #print(f'blocks: {blocks}')
    blockTypeList = []
    for block in markdown_blocks:
        blockTypeList.append(block_to_block_type(block))
    return blockTypeList

def extract_title(markdown:str) -> str:
    foundResult = re.findall(r"^#\s([^\n]*)",markdown)
    return foundResult[0]