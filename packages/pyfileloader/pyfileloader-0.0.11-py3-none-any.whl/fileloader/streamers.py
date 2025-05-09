"""
Lightweigth file reader for common API outputs
"""

import csv
import gzip
import json
from typing import Any, Generator, Union

from .helpers import detect_bom

GZIP = ".gz"
DEFAULT_CHUNK_SIZE = 1000


def stream_jsonl(
    file: str,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
) -> Generator[list[dict[str, Any]], None, None]:
    """
    Read and load JSONL or NDJSON files. These have a complete JSON record per line
    """
    items = []
    for lines in stream_text(file, chunk_size):
        for line in lines:
            items.append(json.loads(line))
        if len(items) >= chunk_size:
            yield items
            items = []

    if items:
        yield items


def stream_text(
    file: str, chunk_size: int = DEFAULT_CHUNK_SIZE
) -> Generator[list[str], None, None]:
    """
    Quickly load a text file to a list of lines

    :param file: file to load
    :return: list of lines
    """
    openfn = open
    needs_decode = False
    if file.endswith(GZIP):
        openfn = gzip.open
        needs_decode = True

    items = []
    with openfn(file, "r") as f:
        for line in f:
            if needs_decode:
                line = line.decode("UTF-8")

            items.append(line.strip())
            if len(items) >= chunk_size:
                yield items
                items = []

    if items:
        yield items


# def stream_csv(file: str, chunk_size: int = DEFAULT_CHUNK_SIZE) -> Generator[list[dict[str, Any]], None, None]:
#     """
#     Read and load CSV files. These have a complete JSON record per line
#     """

#     # this is a special case where we have to retain the first line of the file to properly marshal the CSV over time to a list of dictionaries
#     # so we need to load the first line first

#     header = None
#     first_read = True
#     for lines in stream_text(file, chunk_size):
#         for line in lines:
#             items.append(line)
#         if len(items) >= chunk_size:
#             yield items
#             items = []

#     if items:
