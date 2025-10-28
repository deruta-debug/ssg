import os
from pathlib import Path

from markdown_blocks import markdown_to_html_node


def generate_pages_recursive(basepath, dir_path_content, template_path, dest_dir_path):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(basepath, from_path, template_path, dest_path)
        else:
            generate_pages_recursive(basepath, from_path, template_path, dest_path)


def generate_page(basepath, from_path, template_path, dest_path):
    print(f" * {from_path} {template_path} -> {dest_path}")
    md_content = read_file(from_path)
    template = read_file(template_path)

    node = markdown_to_html_node(md_content)
    html = node.to_html()
    title = extract_title(md_content)

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace('src="/', f'src="{basepath}')

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    with open(dest_path, "w") as to_file:
        to_file.write(template)


def read_file(path):
    with open(path) as file:
        return file.read()


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("no title found")
