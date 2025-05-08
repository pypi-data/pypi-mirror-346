import argparse

def create_parser():
    parser = argparse.ArgumentParser(description='Count unique characters in a string')
    parser.add_argument('-s', '--string', type=str, help='Input string to process')
    parser.add_argument('-f', '--file', type=str, help='Path to text file to process')
    return parser
