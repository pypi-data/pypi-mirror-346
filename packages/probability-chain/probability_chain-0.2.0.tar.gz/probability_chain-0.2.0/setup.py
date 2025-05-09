# setup.py
from setuptools import setup, find_packages
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="probability-chain",
    version="0.2.0",
    description="Simulate and optimize chained probability stages",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Your Name",
    author_email="your@email.com",
    url="https://github.com/yourusername/probability-chain",
    packages=find_packages(),
    install_requires=[
        "matplotlib",
        "numpy",
    ],
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)