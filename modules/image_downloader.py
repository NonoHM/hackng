# image_downloader.py

import os
import re
import requests
import pathlib

class ImageDownloader:
    def __init__(self, file_name):
        self.file = file_name
        self.filename = os.path.basename(self.file).split('.')[0].lower().replace(' ', '_')
        self.L = []

    def link_searcher(self):
        with open(self.file, 'r') as f:
            for line in f.readlines():
                if re.match(r'!\[[^\]]*\]\((.*?)\s*("(?:.*[^"])")?\s*\)', line):
                    try:
                        url = re.search(r'https?://\S+', line).group().strip(')')
                        self.L.append(url)
                    except Exception:
                        pass

    def download(self):
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
                
    def change_link(self):
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
                    except Exception:
                        pass
                f.write(line)
