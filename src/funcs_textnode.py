# src/funcs_textnode.py

from textnode import TextNode, TextType
from funcs_extract_markdown  import extract_markdown_images, extract_markdown_links

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
            if split_node_len==1:
                trueResult.append(old_node)
                continue
            elif split_node_len%2==0:
                trueResult.append(old_node)
                raise ValueError(f'Invalid markdown syntax! Odd number of delimiters found in old_node.text')
            nextIsSpecial = False
            while counter<split_node_len:
                if not split_node[counter]:
                    nextIsSpecial = not nextIsSpecial
                    counter+=1
                    continue
                elif nextIsSpecial:
                    resultNodes.append(TextNode(split_node[counter], text_type))
                else: 
                    resultNodes.append(TextNode(split_node[counter], TextType.TEXT))
                nextIsSpecial = not nextIsSpecial
                counter+=1
            trueResult.extend(resultNodes)
    return trueResult

def split_nodes_image(old_nodes:list[TextNode]) -> list[TextNode]:
    trueResult=[]
    for old_node in old_nodes:
        if old_node.text_type!=TextType.TEXT:
            trueResult.append(old_node)
        else:
            imageInfo = extract_markdown_images(old_node.text)
            if len(imageInfo)<1:
                trueResult.append(old_node)
                continue
            else:
                remaining_portion = old_node.text
                for altProp, srcProp in imageInfo:
                    sections= remaining_portion.split(f"![{altProp}]({srcProp})",1)
                    if len(sections)==1:
                        raise ValueError("Image not found but should have been?")
                    if sections[0]:
                        trueResult.append(TextNode(sections[0],TextType.TEXT))
                    trueResult.append(TextNode(altProp, TextType.IMAGE, srcProp))
                    remaining_portion = sections[1]
                if remaining_portion:
                    trueResult.append(TextNode(remaining_portion, TextType.TEXT))
    return trueResult

def split_nodes_link(old_nodes:list[TextNode]) -> list[TextNode]:
    trueResult=[]
    for old_node in old_nodes:
        if old_node.text_type!=TextType.TEXT:
            trueResult.append(old_node)
        else:
            linkInfo = extract_markdown_links(old_node.text)
            if len(linkInfo)<1:
                trueResult.append(old_node)
                continue
            else:
                remaining_portion = old_node.text
                for anchorText, hrefProp in linkInfo:
                    sections= remaining_portion.split(f"[{anchorText}]({hrefProp})",1)
                    if len(sections)==1:
                        raise ValueError("Links not found but should have been?")
                    if sections[0]:
                        trueResult.append(TextNode(sections[0],TextType.TEXT))
                    trueResult.append(TextNode(anchorText, TextType.LINK, hrefProp))
                    remaining_portion = sections[1]
                if remaining_portion:
                    trueResult.append(TextNode(remaining_portion, TextType.TEXT))
    return trueResult

def text_to_textnodes(text:str) -> list[TextNode]:
    startTextNode = [TextNode(text, TextType.TEXT)]
    boldSeperated = split_nodes_delimiter(startTextNode,"**", TextType.BOLD)
    italicSeperated = split_nodes_delimiter(boldSeperated, "_", TextType.ITALIC)
    codeSeperated = split_nodes_delimiter(italicSeperated, "`", TextType.CODE)
    imageSeperated = split_nodes_image(codeSeperated)
    linkSeperated = split_nodes_link(imageSeperated)
    return linkSeperated
