from setuptools import setup, find_packages
import io

def read_file(filename):
    with io.open(filename, encoding='utf-8') as f:
        return f.read()

setup(
    name="fscolor",
    version="0.1.2",
    author="Yusuf Muhammed Adekunle",
    author_email="muadeyus@gmail.com",
    description="Color formatting for f-strings",
    long_description=read_file('README.md'),
    long_description_content_type="text/markdown",
    url="https://github.com/Kunlex58/fscolor",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)