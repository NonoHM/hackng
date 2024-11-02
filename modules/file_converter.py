# file_converter.py

import os
import pypandoc

class FileConverter:
    def __init__(self, file_name, pandoc_args=None):
        self.file_name = file_name
        self.pandoc_args = ['--' + arg for arg in (pandoc_args or [])]
        if not pypandoc.get_pandoc_version():
            pypandoc.download_pandoc()
        
    def convert_to_pdf(self):
        markdown_dir = os.path.dirname(os.path.abspath(self.file_name))
        os.chdir(markdown_dir)  
        
        base_name = os.path.splitext(os.path.basename(self.file_name))[0]
        pypandoc.convert_file(self.file_name, 'pdf', outputfile=f"{base_name}.pdf", extra_args=self.pandoc_args)
