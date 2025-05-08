# Symbol Counter Package

This is a simple Python package for text analysis for counting unique characters. 

## Installation

To install the package locally from the project root, run the following command in your terminal: 

```bash
pip install .
```
## Usage

After installation, you can use the package as follows:
```
from symbol_counter import count_unique_symbols

text = "example text"
result = count_unique_symbols(text)
print(result)
```
## CLI Usage

After installing the package, you can use the command-line interface:

```bash
python -m symbol_counter.counter --string "original text"
```