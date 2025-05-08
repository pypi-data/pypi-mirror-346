from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="chatfic-validator",
    version="0.2.2",
    author="Gökhan Mete Ertürk",
    author_email="8rlvjfxsh@mozmail.com",
    description="A Python package for validating chatfic-format data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gokhanmeteerturk/chatfic-validator-python",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
