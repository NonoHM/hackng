# modules/image_replacer.py

import re

class ImageReplacer:
    def __init__(self, file_name):
        self.file_name = file_name

    def update_image_paths(self, new_base_path):
        """ Update only the path component for both Markdown and Liquid syntax """
        # Patterns to match Markdown and Liquid image syntax
        markdown_pattern = re.compile(r'!\[([^\]]+)\]\(([^)]+)\)')
        liquid_pattern = re.compile(r'{%\s*include\s+figure\.liquid\s+path="([^"]+)"\s+title="([^"]+)"\s+class="([^"]+)"\s*%}')
        
        with open(self.file_name, 'r') as f:
            lines = f.readlines()

        with open(self.file_name, 'w') as f:
            for line in lines:
                # Update path for Markdown images
                markdown_match = markdown_pattern.search(line)
                if markdown_match:
                    alt_text = markdown_match.group(1)
                    original_path = markdown_match.group(2)
                    
                    # Keep filename, change only the base path
                    new_path = f"{new_base_path.rstrip('/')}/{original_path.split('/')[-1]}"
                    new_line = f'![{alt_text}]({new_path})\n'
                    f.write(new_line)
                    continue

                # Update path for Liquid images
                liquid_match = liquid_pattern.search(line)
                if liquid_match:
                    original_path = liquid_match.group(1)
                    title = liquid_match.group(2)
                    css_class = liquid_match.group(3)
                    
                    # Keep filename, change only the base path
                    new_path = f"{new_base_path.rstrip('/')}/{original_path.split('/')[-1]}"
                    new_line = f'{{% include figure.liquid path="{new_path}" title="{title}" class="{css_class}" %}}\n'
                    f.write(new_line)
                    continue

                # Write original line if no match
                f.write(line)

    def convert_to_liquid_syntax(self):
        """ Convert Markdown image syntax to Liquid tags and update path if new_base_path is provided """
        markdown_pattern = re.compile(r'!\[([^\]]+)\]\(([^)]+)\)')
        
        with open(self.file_name, 'r') as f:
            lines = f.readlines()

        with open(self.file_name, 'w') as f:
            for line in lines:
                # Match Markdown image syntax
                markdown_match = markdown_pattern.search(line)
                if markdown_match:
                    alt_text = markdown_match.group(1)
                    original_path = markdown_match.group(2)
                
                    new_line = f'{{% include figure.liquid path="{original_path}" title="{alt_text}" class="img-fluid rounded z-depth-1" %}}\n'
                    f.write(new_line)
                    continue

                # Write original line if no match
                f.write(line)
