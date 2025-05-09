from setuptools import setup, find_packages

setup(
    name="simpyq",
    version="1.0.0",
    author="Mohamed Gueni",
    author_email="mohamedgueni@outlook.com",
    description="CLI tool to query and analyze simulation CSV data with natural language",
    long_description="CLI tool to query and analyze simulation CSV data with natural language. It uses OpenAI's GPT-3.5-turbo model to process and analyze the data, providing a user-friendly interface for data exploration.",
    long_description_content_type="text/markdown",
    url="https://github.com/Gueni/simpyq",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "pandas",
        "numpy",
        "matplotlib",
        "rich",
        "pyfiglet",
        "spacy",
    ],
    entry_points={
        "console_scripts": [
            "simpyq=simpyq.cli:main",  # assuming cli.py has a `main()` function
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
