# modules/argument_parser.py

import argparse

def parse_arguments():
    desc_message = """
    In order to download the images, the links must be in the format: ![alt text](https://url.com/image.png).
    The images will be downloaded to a folder named 'images/file_name' in the same directory as the markdown file.
    Important: The note should be public/readable for eveyone in order to download the images.
    """
    
    parser = argparse.ArgumentParser(description=desc_message)

    parser.add_argument('-f', '--file-name', help='file_name')
    parser.add_argument('-d', '--directory', help='directory where the .md files are located')
    parser.add_argument('-r', '--recursive', action='store_true', help='search for .md files in the directory and subdirectories')
    
    parser.add_argument('--replace-image-liquid', action='store_true', help='convert markdown images to Liquid tags')
    parser.add_argument('--new-base-path', help='new base path for images without altering filenames (e.g., ./images -> /assets/images). Does not move the images.')
    
    parser.add_argument('-nd', '--no-download', action='store_true', help='do not download images')
    parser.add_argument('-nl', '--no-link', action='store_true', help='do not change links')
    parser.add_argument('-s', '--skip', action='store_true', help='skip the download and link change process')

    parser.add_argument('-pdf', '--pdf-output', action='store_true', help='change to pdf in latex format using pandoc')
    parser.add_argument('-a', '--pandoc-args', nargs="+", help='args to be passed through pandoc, e.g., -a toc template=template.latex')

    return parser.parse_args()
