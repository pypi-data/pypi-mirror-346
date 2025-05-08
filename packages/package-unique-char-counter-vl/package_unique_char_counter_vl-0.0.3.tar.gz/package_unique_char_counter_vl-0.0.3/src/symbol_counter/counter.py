from collections import Counter

from functools import lru_cache

from .cli import create_parser

@lru_cache(maxsize=100)
def count_unique_symbols(string: str) -> int:
    """
    Counts the number of characters that appear only once in the input string.

    Args:
           string: The string which is to be analyzed.

    Returns:
            int: The number of unique characters.

    Raises:
            TypeError: If the input is not a string.

   """
    if not isinstance(string, str):
        raise TypeError("It's not a string")
    else:
        counter = Counter(string)
        unique_value = map(lambda item: 1 if item[1] == 1 else 0, counter.items())
        unique_count = sum(unique_value)
        return unique_count


def main():
    parser = create_parser()
    args = parser.parse_args()

    if args.file:
        with open(args.file, 'r') as file:
            text = file.read()
    elif args.string:
        text = args.string
    else:
        parser.error("There must be --string or --file.")

    result = count_unique_symbols(text)
    print(result)

if __name__ == "__main__":
    main()
