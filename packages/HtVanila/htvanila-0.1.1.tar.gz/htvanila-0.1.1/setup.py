# setup.py
from setuptools import setup, find_packages
import os
import sys

setup(
    name="HtVanila",
    version="0.1.1",
    author="Developer",
    author_email="acounts687@gmail.com",
    description="A library for combining HTML, CSS, JS and images into a single HTML file",
    packages=find_packages(),
    install_requires=[
        "beautifulsoup4",
        "flask",
        "click",
        "colorama",
        "pillow",
    ],
    entry_points={
        "console_scripts": [
            "vanila=htvanila.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)