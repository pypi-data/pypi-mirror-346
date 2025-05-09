from setuptools import setup, find_packages

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="llm-cli-lite",
    version="0.1.1",
    author="mr_hanlu",
    description="A lightweight command-line tool that generates terminal commands from natural language",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mr-hanlu/llm-cli",
    packages=find_packages(),
    install_requires=[
        "openai>=1.77.0",
        "rich>=14.0.0",
        "setuptools>=75.8.0"
    ],
    python_requires=">=3.10",
    classifiers=[
            "Programming Language :: Python :: 3.12",
            "License :: OSI Approved :: MIT License",
        ],
    entry_points={
        "console_scripts": [
            "llm-cli=llm_cli.__main__:main"
        ],
    }
)