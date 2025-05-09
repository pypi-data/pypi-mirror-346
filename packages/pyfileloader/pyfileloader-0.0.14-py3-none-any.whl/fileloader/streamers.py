"""
Lightweigth file reader for common API outputs
"""

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
    file: str,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    enc: Union[str, None] = None,
) -> Generator[list[str], None, None]:
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
                line = line.decode(enc)

            items.append(line.strip())
            if len(items) >= chunk_size:
                yield items
                items = []

    if items:
        yield items


# def stream_csv(
#     file: str, chunk_size: int = DEFAULT_CHUNK_SIZE
# ) -> Generator[list[dict[str, Any]], None, None]:
#     """
#     Read and load CSV files. These have a complete JSON record per line
#     """

#     # this is a special case where we have to retain the first line of the file to properly marshal the CSV over time to a list of dictionaries
#     # so we need to load the first line first

#     header = None
#     items = []
#     dict_from_csv = []
#     for lines in stream_text(file, chunk_size):
#         if header is None:
#             header = lines[0]
#             continue

#         if len(items) >= chunk_size:
#             file_csv = csv.DictReader([header] + items)
#             for row in file_csv:
#                 dict_from_csv.append(row)
#             yield dict_from_csv
#             dict_from_csv = []
#             items = []

#     if items:
#         file_csv = csv.DictReader([header] + items)
#         for row in file_csv:
#             dict_from_csv.append(row)
#         yield dict_from_csv
