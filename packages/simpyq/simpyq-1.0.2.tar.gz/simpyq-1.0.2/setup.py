from setuptools import setup, find_packages

setup(
    name="simpyq",
    version="1.0.2",
    author="Mohamed Gueni",
    author_email="mohamedgueni@outlook.com",
    description="CLI tool to query and analyze simulation CSV data with natural language",
    long_description=open("README.md").read(),
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
