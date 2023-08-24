import csv
from typing import Any, Callable, Iterable

import stock


def convert_csv(
    lines: Iterable[Any],
    converter: Callable[[list[str], list[str]], Any],
    *,
    headers=None
):
    """
    Convert lines of CSV data into data that depends on converter.
    """
    rows = csv.reader(lines)
    if headers is None:
        headers = next(rows)
    return list(map(lambda row: converter(headers, row), rows))


def csv_as_dicts(
    lines: Iterable[str], types: Iterable[type], headers: Iterable[str] | None = None
) -> list[dict[str, Any]]:
    """
    Convert lines of CSV data into a list of dictionaries
    """
    return convert_csv(
        lines,
        lambda headers, row: {
            name: func(val) for name, func, val in zip(headers, types, row)
        },
    )


def csv_as_instances(
    lines: Iterable[str], cls: stock.Stock, headers: Iterable[str] | None = None
) -> list[stock.Stock]:
    """
    Convert lines of CSV data into a list of instances
    """

    return convert_csv(lines, lambda headers, row: cls.from_row(row))


def read_csv_as_dicts(filename, types, *, headers=None):
    """
    Read CSV data into a list of dictionaries with optional type conversion
    """
    with open(filename) as file:
        return csv_as_dicts(file, types, headers=headers)


def read_csv_as_instances(filename, cls, *, headers=None):
    """
    Read CSV data into a list of instances
    """
    with open(filename) as file:
        return csv_as_instances(file, cls, headers=headers)
