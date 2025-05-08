import argparse
from pathlib import Path
from .generator import ProjectGenerator

def create_project(project_name):
    generator = ProjectGenerator(project_name)
    return generator.generate()

def init_project():
    print("Project initialization will be added in future versions")

def main():
    parser = argparse.ArgumentParser(description='Создание нового Discord-бота на основе Midnight Framework')
    parser.add_argument('project_name', help='Название проекта для создания')
    
    args = parser.parse_args()
    create_project(args.project_name)

if __name__ == '__main__':
    main()