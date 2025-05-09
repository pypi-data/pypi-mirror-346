from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="processador-de-imagem-zoemateus324",
    version="0.0.2",
    author="Zoe Santos",
    author_email="zmmateus2@gmail.com",
    description="My first application of image processing with python language",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Zoemateus324/processador-de-imagem",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)