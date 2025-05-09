# setup.py
from setuptools import setup, find_packages

setup(
    name="probability-chain",
    version="0.1.0",
    description="Simulate and optimize chained probability stages",
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