from setuptools import setup, find_packages
from io import open

def read(filename):
   with open(filename, "r", encoding="utf-8") as file:
      return file.read()

setup(
    name="freegpts",
    version="1.1.0",
    description="The project provides free access to ChatGPT-4, GPT-4o-mini, and SearchGPT models for integration into Python applications.",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=["requests"],
    project_urls={
        "GitHub": "https://github.com/xevvv/free-chat-gpt"
    },
)
