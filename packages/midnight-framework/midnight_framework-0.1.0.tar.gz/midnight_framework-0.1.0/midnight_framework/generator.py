import os
import shutil
from pathlib import Path

class ProjectGenerator:
    def __init__(self, project_name):
        self.project_name = project_name
        self.template_dir = os.path.join(os.path.dirname(__file__), 'templates')
        
    def generate(self):
        try:
            os.makedirs(self.project_name, exist_ok=False)

            for root, dirs, files in os.walk(self.template_dir):
                rel_path = os.path.relpath(root, self.template_dir)
                dest_path = os.path.join(self.project_name, rel_path)
                
                os.makedirs(dest_path, exist_ok=True)
                
                for file in files:
                    src_file = os.path.join(root, file)
                    dest_file = os.path.join(dest_path, file)
                    shutil.copy2(src_file, dest_file)
            
            with open(os.path.join(self.project_name, '.env'), 'w') as f:
                f.write('TOKEN=your_bot_token_here\n')
            
            print(f"Project '{self.project_name}' successfully created!")
            print(f"don't forget to fill in the .env file and configure enums.py")
            return True
        
        except FileExistsError:
            print(f"Error: Directory '{self.project_name}' it already exists..")
            return False