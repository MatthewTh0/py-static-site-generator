# main.py

from textnode import TextNode, TextType
from funcs_transfer import copy_directory_content, generate_pages_recursive
from funcs_extract_markdown import extract_title
import argparse, sys

def main():
    basepath="/"
    if sys.argv:
        basepath = sys.argv[1]
    copy_directory_content("static/","docs/", False)
    generate_pages_recursive("content","template.html", "docs", basepath)

main()