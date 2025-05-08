from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='midnight-framework',
    version='0.1.0',
    author='z0nyx',
    author_email='midnight.framework@gmail.com',
    description='Framework for quickly creating Discord bots with Disnake',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/z0nyx/midnight-framework',
    packages=find_packages(),
    package_data={
        'midnight_framework': ['templates/*', 'templates/cogs/*', 'templates/Buttons/*', 'templates/core/*'],
    },
    include_package_data=True,
    install_requires=[
        'disnake>=2.8.0',
        'python-dotenv>=0.19.0',
        'colorama>=0.4.4',
    ],
    entry_points={
        'console_scripts': [
            'midnight=midnight_framework.cli:main',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
    keywords='discord bot framework disnake',
    project_url={
        'Source': 'https://github.com/z0nyx/midnight-framework',
    },
)