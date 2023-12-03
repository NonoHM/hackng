import requests
import argparse
import re
import os
import pathlib
import pypandoc

parser = argparse.ArgumentParser()

parser.add_argument('-f', '--file_name', help='file_name')
parser.add_argument('-pdf', '--pdf_output', action='store_true', help='change to pdf in latex format using pandoc')
# parser.add_argument('-a', '--pandoc_args', type=str, nargs='+', help='args to be passed through pandoc, ex: -a "--toc --template=template.latex". Files will be taken from the directory of the markdown file.')
args = parser.parse_args()


class ImageDownloader:
    def __init__(self, file_name) -> None:
        self.file_name = file_name
        self.L = []

    def link_searcher(self) -> None:
        with open(self.file_name, 'r') as f:
            for line in f.readlines():
                if re.match(r'!\[[^\]]*\]\((.*?)\s*("(?:.*[^"])")?\s*\)', line):
                    try:
                        url = re.search(r'https?://\S+', line).group().strip(')')
                        self.L.append(url)
                    except:
                        pass

    def download(self) -> None:
        session = requests.Session()
        file_path = os.path.dirname(args.file_name)
        path = os.path.join(file_path, "images")
        
        if not os.path.exists(path):
            os.mkdir(path)
        
        for image_link in self.L:
            r = session.get(image_link)
            image_name = image_link.split('/')[-1]
            with open(pathlib.Path(path) / image_name, 'wb') as f:
                f.write(r.content)
                
                
    def change_link(self) -> None:
        with open(self.file_name, 'r') as f:
            lines = f.readlines()

        with open(self.file_name, 'w') as f:
            for line in lines:
                match = re.match(r'!\[[^\]]*\]\((.*?)\s*("(?:.*[^"])")?\s*\)', line)
                if match:
                    try:
                        url = re.search(r'https?://\S+', match.group()).group().strip(')')
                        name = f"./images/{self.L.pop(0).split('/')[-1]}"
                        line = line.replace(url, name)
                    except:
                        pass
                f.write(line)
                    
class FileConverter:
    
    def __init__(self, file_name) -> None:
        self.file_name = file_name
        if not pypandoc.get_pandoc_version():
            pypandoc.download_pandoc()
      
    def convert_to_pdf(self) -> None:
        markdown_dir = os.path.dirname(os.path.abspath(self.file_name))
        os.chdir(markdown_dir)  
        
        base_name = os.path.splitext(os.path.basename(self.file_name))[0]
        
        pypandoc.convert_file(self.file_name, 'pdf', outputfile=f"{base_name}.pdf", extra_args=args)
       
                    
def main():
    if args.file_name is None:
        print('Please input a valid file path')
        exit()
    file_name = args.file_name
    image_downloader = ImageDownloader(file_name)
    print('Searching for images...')
    image_downloader.link_searcher()
    print('Downloading images...')
    image_downloader.download()
    print('Changing links to image\'s names...')
    image_downloader.change_link()
    
    if args.pdf_output:
        file_converter = FileConverter(file_name)
        print('Converting to pdf...')
        file_converter.convert_to_pdf()

if __name__ == '__main__':
    main()