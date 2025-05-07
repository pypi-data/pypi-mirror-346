from setuptools import setup, find_packages

# Reading  README.md to PyPI
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="calculator-lib-henriqk0",
    version="0.1.0",
    packages=["calculator_lib"], 
    description="Biblioteca de operações matemáticas básicas em Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Henrique de Souza Lima",
    author_email="henriquedeslima2811@gmail.com",
    url="https://github.com/henriqk0/calculator-fastapi-lib",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",

)