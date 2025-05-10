from setuptools import setup, find_packages

setup(
    name="shell-prompt",
    version="0.1.0",
    description=("A command-line tool that converts natural language instructions into shell "
                 "commands and executes them."),
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Roko Torbarina",
    author_email="rokotorbarina9@gmail.com",
    url="https://github.com/082T/shell-prompt",
    packages=find_packages(),
    install_requires=[
        "argparse"
    ],
    extras_require={
        "openai": ["langchain[openai]"],
        "anthropic": ["langchain[anthropic]"],
        "google-genai": ["langchain[google-genai]"],
        "groq": ["langchain[groq]"],
        "cohere": ["langchain[cohere]"],
        "langchain-nvidia-ai-endpoints": ["langchain-nvidia-ai-endpoints"],
        "fireworks": ["langchain[fireworks]"],
        "mistralai": ["langchain[mistralai]"],
        "together": ["langchain[together]"],
        "langchain-xai": ["langchain-xai"],
        "langchain-perplexity": ["langchain-perplexity"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license="MIT",
    entry_points={
        "console_scripts": [
            "shell-prompt = shell_prompt.cli.main:main",
        ],
    },
)
