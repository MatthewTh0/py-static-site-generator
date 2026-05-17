# src/funcs_transfer.py

import os, shutil
from funcs_htmlnode import markdown_to_html_node
from funcs_extract_markdown import extract_title

def copy_directory_content(srcDirectory:str,destDirectory:str, safetyOn:bool=True):
    #print(os.path.abspath("."))
    #print(safetyOn)
    if not os.path.exists(srcDirectory):
        raise NotADirectoryError("Source directory must exist to copy!")
    if os.path.exists(destDirectory):
        if safetyOn:
            print(f"About to delete directory at {destDirectory}. Are you sure? y/n")
            yesCheck = input()
            match yesCheck:
                case "y"|"Y":
                    print(f"Deleting directory?!")
                    shutil.rmtree(destDirectory)
                case "n","N":
                    print("Exiting")
                    return
        else:
            shutil.rmtree(destDirectory)
    os.mkdir(destDirectory)
    #thisSrcDirList = os.listdir(srcDirectory)
    directoryList = os.listdir(srcDirectory)
    for filepath in directoryList:
        fullPath = os.path.join(srcDirectory, filepath)
        #print(f"Filepath {fullPath}")
        if os.path.isfile(fullPath):
            print(f'Copying file: {filepath} from {fullPath} to {destDirectory}')
            shutil.copy(fullPath, destDirectory)
        else:
            subDestPath=os.path.join(destDirectory,filepath)
            print(f"Creating directory {filepath} from {fullPath} to form {subDestPath}")
            os.mkdir(subDestPath)
            copy_directory_content(fullPath,subDestPath, safetyOn)


def generate_page(from_path:str, template_path:str, dest_path:str):
    if os.path.exists(from_path) and os.path.isfile(from_path):

        print(f"Generating page from {from_path} to {dest_path} using {template_path}")
        mdFileContent= ""
        templFile = ""
        with open(from_path) as mdFile:
            mdFileContent= mdFile.read()
        with open(template_path) as templFile:
            templFileContent = templFile.read()
        createdHTMLNodes = markdown_to_html_node(mdFileContent)
        #print(f"Created nodes of: {createdHTMLNodes}")
        createdHTMLFileContent = createdHTMLNodes.to_html()
        thisTitle = extract_title(mdFileContent)
        #print(f"Found title of {thisTitle} and content of {createdHTMLFileContent}")
        finalFileContent = templFileContent.replace("{{ Title }}", thisTitle)
        finalFileContent =finalFileContent.replace("{{ Content }}", createdHTMLFileContent)
        if not os.path.exists(dest_path):
            #print(os.path.dirname(dest_path))

            os.makedirs(os.path.dirname(dest_path),exist_ok=True)
        with open(dest_path, "a") as outFile:
            outFile.write(finalFileContent)
    else:
        raise Exception()
    
def generate_pages_recursive(dir_path_content:str, template_path:str, dest_dir_path:str):
    if not os.path.exists(dir_path_content):
        raise NotADirectoryError()
    dirToCopy= os.listdir(dir_path_content)
    for dirEntry in dirToCopy:
        fullSrcPath = os.path.join(dir_path_content, dirEntry)
        fullDestPath = os.path.join(dest_dir_path, dirEntry)
        if os.path.isfile(fullSrcPath):        
            if not dirEntry.endswith(".md"):
                raise NotImplementedError("Only handles markdown files!")
            else:
                newDirEntry =dirEntry.replace(".md",".html")
                fullNewDestPath=os.path.join(dest_dir_path,newDirEntry)
                generate_page(fullSrcPath, template_path, fullNewDestPath)
        else:
            if not os.path.exists(fullDestPath):
                os.makedirs(fullDestPath, exist_ok=True)
            generate_pages_recursive(fullSrcPath,template_path,fullDestPath)