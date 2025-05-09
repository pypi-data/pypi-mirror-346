"""
Lightweigth file reader for common API outputs
"""

import csv
import gzip
import json
from typing import Any, Union

from .helpers import detect_bom

GZIP = ".gz"


def load_json(file: str) -> list[dict[str, Any]]:
    """
    Read and load JSON files
    """

    openfn = open
    needs_decode = False
    if file.endswith(GZIP):
        openfn = gzip.open
        needs_decode = True

    with openfn(file, "r") as f:
        data = f.read()
    if needs_decode and not isinstance(data, str):
        data = data.decode("UTF-8")

    item = json.load(data)
    return item


def load_jsonl(file: str, enc: Union[str, None] = None) -> list[dict[str, Any]]:
    """
    Read and load JSONL or NDJSON files. These have a complete JSON record per line
    """

    lines = load_text(file, enc)
    items = []
    for line in lines:
        items.append(json.loads(line))

    return items


def load_text(file: str, enc: Union[str, None] = None) -> list[str]:
    """
    Quickly load a text file to a list of lines

    :param file: file to load
    :return: list of lines
    """
    if enc is None:
        enc = detect_bom(file)

    openfn = open
    needs_decode = False
    if file.endswith(GZIP):
        openfn = gzip.open
        needs_decode = True

    items = []
    with openfn(file, "r", encoding=enc) as f:
        for line in f:
            if needs_decode and not isinstance(line, str):
                line = line.decode("UTF-8")

            items.append(line.strip())

    return items


def load_csv(file: str, enc: Union[str, None] = None) -> list[dict[str, Any]]:
    """
    Read and load CSV files. These have a complete JSON record per line

    :param file: file to load
    :param enc: encoding to use, if not provided, it will be detected
    :return: list of dictionaries
    """

    # if the encoding isn't explicit
    if enc == "":
        enc = detect_bom(file)

    # in a different manner than the other functions

    lines = load_text(file)
    items = []
    file_csv = csv.DictReader(lines)
    for row in file_csv:
        items.append(row)

    return items
