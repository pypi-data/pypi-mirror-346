from setuptools import setup, find_packages

setup(
    name="FahrenCels",
    version="0.1.0",
    author="annzelly",
    description="A simple Python module for converting temperatures between Celsius and Fahrenheit.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
