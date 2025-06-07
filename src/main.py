from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
import os, shutil
from markdown_blocks import markdown_to_html_node, extract_title
import sys

def main():
    base_path = sys.argv[1] if len(sys.argv) > 1 else "/"
    static_dir = '/Users/saswat/workspace/github.com/sswtshoo/static-site-generator/static'
    public_dir = '/Users/saswat/workspace/github.com/sswtshoo/static-site-generator/docs'
    content_dir = '/Users/saswat/workspace/github.com/sswtshoo/static-site-generator/content'
    template_dir = '/Users/saswat/workspace/github.com/sswtshoo/static-site-generator/template.html'
    if not os.path.exists(public_dir):
        os.mkdir(public_dir)
    for file in os.listdir(public_dir):
        file_path = os.path.join(public_dir, file)
        if os.path.isdir(file_path):
            shutil.rmtree(file_path)
        else:
            os.remove(file_path)
    
    del_and_copy_files(static_dir, public_dir)
    generate_pages_recursive(content_dir, template_dir, public_dir, base_path)

def generate_page(from_path: str, template_path: str, dest_path: str, base_path: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    from_file = open(from_path, 'r')
    from_md = from_file.read()
    from_html_node = markdown_to_html_node(from_md)
    from_html = from_html_node.to_html()
    title = extract_title(from_md)
    template_file = open(template_path, 'r')
    template = template_file.read()
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", from_html)
    template = template.replace('href="/', f'href="{base_path}')
    template = template.replace('src="/', f'src="{base_path}')
    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    dest_file = open(dest_path, 'w')
    dest_file.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, base_path):

    for file in os.listdir(dir_path_content):
        dest_path = os.path.join(dest_dir_path, file)
        curr_path = os.path.join(dir_path_content, file)
        if os.path.isdir(curr_path):
            os.makedirs(dest_path, exist_ok=True)
            generate_pages_recursive(curr_path, template_path, dest_path, base_path)
        elif file.endswith('.md'):
            html_name = os.path.splitext(file)[0] + '.html'
            dest_file_path = os.path.join(dest_dir_path, html_name)
            generate_page(curr_path, template_path, dest_file_path, base_path)

def del_and_copy_files(source, destination):
    if not os.path.exists(source):
        raise ValueError("Source file path doesn't exist")
    try:
        del_tree(destination)
    except (FileNotFoundError, PermissionError, NotADirectoryError) as e:
        print(f"Deletion failed: {e}")
    except Exception as e:
        print(f"Error occured: {e}")

    copy_files(source, destination)
    
def copy_files(source, destination):
    try:
        for file in os.listdir(source):
            file_path = os.path.join(source, file)
            dest_path = os.path.join(destination, file)
            if not os.path.isdir(file_path):
                dest_path = os.path.join(destination, file)
                shutil.copy(file_path, dest_path)
            else:
                os.mkdir(dest_path)
                copy_files(file_path, dest_path)
    except Exception as e:
        print(f"Error copying files: {e}")

def del_tree(path):
    if not os.path.exists(path):
        os.mkdir(path)
        print(f"Directory does not exist. Creating new directory")
    else:
        parent = os.path.dirname(path)
        if not os.access(parent, os.W_OK | os.X_OK):
            raise PermissionError(f"Permission denied for path: {path}")
        if not os.path.isdir(path):
            raise NotADirectoryError('Path provided is not a directory')
    
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
            else:
                os.remove(item_path)

main()
