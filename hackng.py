import requests
import argparse
import re
import os
import pathlib
import pypandoc

desc_message = """
In order to download the images, the links must be in the format: ![alt text](https://url.com/image.png).
The images will be downloaded to a folder named 'images/file_name' in the same directory as the markdown file.
Important: The note should be public in order to download the images.
"""

parser = argparse.ArgumentParser(description=desc_message)

parser.add_argument('-f', '--file-name', help='file_name')
parser.add_argument('-d', '--directory', help='directory where the .md files are located')
parser.add_argument('-r', '--recursive', action='store_true', help='search for .md files in the directory and subdirectories')

parser.add_argument('-nd', '--no-download', action='store_true', help='do not download images')
parser.add_argument('-nl', '--no-link', action='store_true', help='do not change links')
parser.add_argument('-s', '--skip', action='store_true', help='skip the download and link change process')

parser.add_argument('-pdf', '--pdf-output', action='store_true', help='change to pdf in latex format using pandoc')
parser.add_argument('-a', '--pandoc-args', nargs="+", help='args to be passed through pandoc, ex: -a toc template=template.latex. Files will be taken from the directory of the markdown file. Hyphens are automatically added to the args. Ex: -a toc template=template.latex => --toc --template=template.latex')


args = parser.parse_args()

class ImageDownloader:
    def __init__(self, file_name) -> None:
        self.file = file_name
        self.filename = os.path.basename(self.file).split('.')[0].lower().replace(' ', '_')
        self.L = []

    def link_searcher(self) -> None:
        with open(self.file, 'r') as f:
            for line in f.readlines():
                if re.match(r'!\[[^\]]*\]\((.*?)\s*("(?:.*[^"])")?\s*\)', line):
                    try:
                        url = re.search(r'https?://\S+', line).group().strip(')')
                        self.L.append(url)
                    except:
                        pass

    def download(self) -> None:
        session = requests.Session()
        file_path = os.path.dirname(self.file)
        path = os.path.join(file_path, "images", self.filename)
        
        if not os.path.exists(path):
            os.makedirs(path)
        
        for image_link in self.L:
            r = session.get(image_link)
            image_name = image_link.split('/')[-1]
            with open(pathlib.Path(path) / image_name, 'wb') as f:
                f.write(r.content)
                
    def change_link(self) -> None:
        with open(self.file, 'r') as f:
            lines = f.readlines()

        with open(self.file, 'w') as f:
            for line in lines:
                match = re.match(r'!\[[^\]]*\]\((.*?)\s*("(?:.*[^"])")?\s*\)', line)
                if match:
                    try:
                        url = re.search(r'https?://\S+', match.group()).group().strip(')')
                        name = f"./images/{self.filename}/{self.L.pop(0).split('/')[-1]}"
                        line = line.replace(url, name)
                    except:
                        pass
                f.write(line)
                    
class FileConverter:
    
    def __init__(self, file_name, pandoc_args=None) -> None:
        self.file_name = file_name
        self.pandoc_args = ['--' + arg for arg in pandoc_args] or []
        if not pypandoc.get_pandoc_version():
            pypandoc.download_pandoc()
        
    def convert_to_pdf(self) -> None:
        markdown_dir = os.path.dirname(os.path.abspath(self.file_name))
        os.chdir(markdown_dir)  
        
        base_name = os.path.splitext(os.path.basename(self.file_name))[0]
        pypandoc.convert_file(self.file_name, 'pdf', outputfile=f"{base_name}.pdf", extra_args=self.pandoc_args)

def directory_searcher():
    files_directory = args.directory
    files_directory = os.path.realpath(files_directory)
    
    if args.recursive:
        for root, dirs, files in os.walk(files_directory):
            for file in files:
                if file.endswith('.md'):
                    path = os.path.join(root, file)
                    downloader(path)
                    pdf_converter(path)
    else:
        for file in os.listdir(files_directory):
            if file.endswith('.md'):
                path = os.path.join(files_directory, file)
                downloader(path)
                pdf_converter(path)

# Downloads the images and changes the links to the image's names
def downloader(file_name):
    
    if args.skip:
        return
    
    image_downloader = ImageDownloader(file_name)
    print('Searching for images...')
    image_downloader.link_searcher()
    if not args.no_download:
        print('Downloading images...')
        image_downloader.download()
    if not args.no_link:
        print('Changing links to image\'s names...')
        image_downloader.change_link()

# Converts the markdown file to pdf if needed
def pdf_converter(file_name):
    if args.pdf_output:
        file_converter = FileConverter(file_name, args.pandoc_args)
        print('Converting to pdf...')
        file_converter.convert_to_pdf()

# Checks for valid file/directory and runs the downloader    
def checker():
    if not args.file_name and not args.directory:
        print('Please input a valid file path or directory path. \nUsage: python hackmd_png.py -h for help.')
        exit(1)
    
    if args.file_name and not os.path.isfile(args.file_name):
        print(f'File not found: {args.file_name}')
        exit(1)
    
    if args.directory and not os.path.isdir(args.directory):
        print(f'Directory not found: {args.directory}')
        exit(1)
   
    if args.directory:
        directory_searcher()
    
    if args.file_name:
        file_name = args.file_name
        downloader(file_name)
        pdf_converter(file_name)
                    
def main():
    checker()

if __name__ == '__main__':
    main()