from src.parser import parse_python_file, parse_notebook_file, parse_file


def test_parse_python_file():
    file_bytes = b'print("hello")'

    result = parse_python_file(file_bytes)

    assert result == 'print("hello")'


def test_parse_notebook_file():
    notebook_json = b'''
    {
        "cells": [
            {
                "cell_type": "markdown",
                "source": ["# title"]
            },
            {
                "cell_type": "code",
                "source": ["x = 1\\n", "print(x)"]
            }
        ]
    }
    '''

    result = parse_notebook_file(notebook_json)

    assert result == "x = 1\nprint(x)"


def test_parse_file_py():
    file_bytes = b"x = 10"

    result = parse_file("sample.py", file_bytes)

    assert result == "x = 10"