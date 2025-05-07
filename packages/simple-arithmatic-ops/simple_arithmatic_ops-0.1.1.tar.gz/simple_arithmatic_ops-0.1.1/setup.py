from setuptools import setup, find_packages
import sys
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

print(f"ran it again with {sys.argv}")

setup(
    name="simple-arithmatic-ops",
    version="0.1.1",
    author="Zilberguy",
    author_email="Some_random_email@gmail.com",
    description="A simple Python package for integer arithmetic operations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
) 