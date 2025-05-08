from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open ("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="image_processing_felipeluiz93teste",
    version="0.0.4",
    author="Felipe",
    description="image Processing Package using skimage",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/FelipeLuiz93/image-processing-package.git",
    packages=find_packages(),
    install_requires=requirements,
    python_requires= '>=3.5',
)