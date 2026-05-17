# main.py

from textnode import TextNode, TextType
from funcs_transfer import copy_directory_content, generate_pages_recursive
from funcs_extract_markdown import extract_title
import argparse

def main():
    #print("# hello world")
    #testTextNode = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    
    #print(testTextNode)

    # Parsing Arguments
    parser = argparse.ArgumentParser(description="Static site generator")
    #parser.add_argument("user_prompt", type=str, help="User prompt")
    #parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("--safe", action="store_true",help="Ask before deleting destination folder")
    args = parser.parse_args()
    safeValue=args.safe
    #print(safeValue)
    #print(extract_title("# Hello"))
    copy_directory_content("static/","public/",args.safe)
    #generate_page("content/index.md","template.html","public/index.html")
    generate_pages_recursive("content","template.html","public")

main()