# src/extract_markdown.py

import re

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
