# modules/file_utils.py

import os
from modules.image_downloader import ImageDownloader
from modules.file_converter import FileConverter
from modules.argument_parser import parse_arguments
from modules.image_replacer import ImageReplacer

def directory_searcher(args):
    files_directory = os.path.realpath(args.directory)
    
    if args.recursive:
        for root, dirs, files in os.walk(files_directory):
            for file in files:
                if file.endswith('.md'):
                    path = os.path.join(root, file)
                    downloader(path, args)
                    pdf_converter(path, args)
                    update_image_paths(path, args)
                    convert_markdown_to_liquid(path, args)
                    
    else:
        for file in os.listdir(files_directory):
            if file.endswith('.md'):
                path = os.path.join(files_directory, file)
                downloader(path, args)
                pdf_converter(path, args)
                update_image_paths(path, args)
                convert_markdown_to_liquid(path, args)
       
def downloader(file_name, args):
    if args.skip:
        return
    
    image_downloader = ImageDownloader(file_name)
    print(f'Searching for images in {file_name}...')
    image_downloader.link_searcher()
    if not args.no_download:
        print(f'Downloading images in {file_name}...')
        image_downloader.download()
    if not args.no_link:
        print(f'Changing links to image\'s names in {file_name}...')
        image_downloader.change_link()

def pdf_converter(file_name, args):
    if args.pdf_output:
        file_converter = FileConverter(file_name, args.pandoc_args)
        print('Converting to pdf...')
        file_converter.convert_to_pdf()

def convert_markdown_to_liquid(file_name, args):
    if args.replace_image_liquid:
        """ Convert Markdown image syntax to Liquid tags, optionally with a new base path """
        image_replacer = ImageReplacer(file_name)
        print(f'Converting markdown images to Liquid syntax in {file_name}')
        image_replacer.convert_to_liquid_syntax()

def update_image_paths(file_name, args):
    """ Update only the base path for images in both Markdown and Liquid syntax """
    path = args.new_base_path
    if path:
        image_replacer = ImageReplacer(file_name)
        print(f'Updating image paths in {file_name} to new base path: {path}')
        image_replacer.update_image_paths(path)

def checker(args):
    if not args.file_name and not args.directory:
        print('Please input a valid file path or directory path.')
        exit(1)
    
    if args.file_name and not os.path.isfile(args.file_name):
        print(f'File not found: {args.file_name}')
        exit(1)
    
    if args.directory and not os.path.isdir(args.directory):
        print(f'Directory not found: {args.directory}')
        exit(1)
   
    if args.directory:
        directory_searcher(args)
    
    if args.file_name:
        downloader(args.file_name, args)
        convert_markdown_to_liquid(args.file_name, args)  
        update_image_paths(args.file_name, args)
        pdf_converter(args.file_name, args)
