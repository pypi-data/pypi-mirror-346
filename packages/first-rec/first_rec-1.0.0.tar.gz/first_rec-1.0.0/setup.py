from setuptools import setup, find_packages

setup(
    name="first-rec",
    version='1.0.0',
    author="Matteo Watson",
    author_email="<m.watson12@gmail.com>",
    description='Find first file record',
    long_description=open("README.md").read(),
    long_description_content_type='text/markdown',

    include = ["LICENSE", "README.md"],
    license = "MIT License",

    keywords=[],
    classifiers = [
        "Framework :: Flask",
        "Development Status :: 6 - Mature",
        "Programming Language :: Python :: 3"
    ],

    packages=find_packages(),
    install_requires=[],
)
