from setuptools import setup, find_packages

setup(
    name='chatprompt',
    version='1.0.2',
    packages=find_packages(),
    install_requires=[
        'requests>=2.32.3',
        'beautifulsoup4>=4.12.3'
    ],
    entry_points={
        "console_scripts": [
            "chatprompt = chatprompt.cli:main",
        ],
    },
    description='A Python package to interact with powerfull AI',
    long_description=open('README.md').read(),
)