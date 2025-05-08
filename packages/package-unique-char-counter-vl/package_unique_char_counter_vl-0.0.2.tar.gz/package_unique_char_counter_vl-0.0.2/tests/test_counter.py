import pytest

import sys

from unittest import mock

from symbol_counter import count_unique_symbols

from symbol_counter.cli import create_parser

@pytest.mark.parametrize("test_input, expected", [("asdf", 4), ("aaaa", 0), ("", 0), ("assddff", 1), ("asdffgg", 3)])
def test_count_unique_symbols(test_input, expected):
    assert count_unique_symbols(test_input) == expected

def test_count_unique_symbols_from_file():
    mock_file = mock.Mock()
    mock_file.read.return_value = "asdfg"

    with mock.patch('builtins.open', return_value=mock_file):
        result = count_unique_symbols(mock_file.read())
    assert result == 5

def test_cli_string():
    test_args = ["name_of_script", "--string", "asdfg"]
    with mock.patch.object(sys, "argv", test_args):
        parser = create_parser()
        args = parser.parse_args()
        assert args.string == "asdfg"

def test_cli_file():
    test_args = ["name_of_script", "--file", "mock_file.txt"]
    with mock.patch.object(sys, "argv", test_args):
        parser = create_parser()
        args = parser.parse_args()
        assert args.file == "mock_file.txt"
