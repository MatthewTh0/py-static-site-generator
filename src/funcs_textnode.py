# src/funcs_textnode.py

from textnode import TextNode, TextType
from funcs_extract_markdown  import extract_markdown_images, extract_markdown_links

# !FIX BELOW


def split_nodes_delimiter(old_nodes:list[TextNode], delimiter:str, text_type:TextType) -> list[TextNode]:
    trueResult=[]
    delimiterFound = False
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
                #print("Warning found no instances of delimiter in section")
                continue
            elif split_node_len%2==0:
                trueResult.append(old_node)
                raise ValueError(f'Invalid markdown syntax! Odd number of delimiters found in old_node.text')
            delimiterFound= True
            beginSymbol = split_node[0]
            #endSymbol = split_node[split_node_len-1]
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
            trueResult.extend(resultNodes)
    #if not delimiterFound:
    #    raise ValueError("No instance of delimiter found!")
    return trueResult
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

        
    # result = [
   # TextNode("This is text with a ", TextType.TEXT),
  #  TextNode("code block", TextType.CODE),
  # TextNode(" word", TextType.TEXT),
  #  ]
  #  return result

def split_nodes_image(old_nodes:list[TextNode]) -> list[TextNode]:
    trueResult=[]
    imageFound = False
    for old_node in old_nodes:
        if old_node.text_type!=TextType.TEXT:
            trueResult.append(old_node)
        else:
            imageInfo = extract_markdown_images(old_node.text)
            if len(imageInfo)<1:
                trueResult.append(old_node)
                continue
                #raise ValueError(f'No images found')
            else:
                imageFound= True
                remaining_portion = old_node.text
                #split_= old_node.text.split()
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
    #if not imageFound:
        #raise ValueError(f'No images found')
    return trueResult

def split_nodes_link(old_nodes:list[TextNode]) -> list[TextNode]:
    trueResult=[]
    linkFound = False
    for old_node in old_nodes:
        if old_node.text_type!=TextType.TEXT:
            trueResult.append(old_node)
        else:
            #anchorText,hrefProp =
            linkInfo = extract_markdown_links(old_node.text)
            if len(linkInfo)<1:
                trueResult.append(old_node)
                continue
                #raise ValueError(f'No links found')
            else:
                linkFound= True
                remaining_portion = old_node.text
                #split_= old_node.text.split()
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

                    #else:
                    #    trueResult.append(TextNode(sections[1], TextType.TEXT))    
                    # what if nothing before, won't above fail
                    #trueResult.append(TextNode(anchorText,TextType.LINK,hrefProp))
                    
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
    #print(f'True result of {old_nodes} to new {trueResult}')
    #if not linkFound:
    #    raise ValueError(f'No links found')
    return trueResult

def text_to_textnodes(text:str) -> list[TextNode]:
    #trueResult = []
    startTextNode = [TextNode(text, TextType.TEXT)]
    boldSeperated = split_nodes_delimiter(startTextNode,"**", TextType.BOLD)
    italicSeperated = split_nodes_delimiter(boldSeperated, "_", TextType.ITALIC)
    codeSeperated = split_nodes_delimiter(italicSeperated, "`", TextType.CODE)
    imageSeperated = split_nodes_image(codeSeperated)
    linkSeperated = split_nodes_link(imageSeperated)
    return linkSeperated


    #return trueResult