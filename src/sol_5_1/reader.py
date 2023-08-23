import csv
from typing import Any, Iterable

import stock


def csv_as_dicts(
    lines: Iterable[str], types: Iterable[type], headers: Iterable[str] | None = None
) -> list[dict[str, Any]]:
    """
    Convert lines of CSV data into a list of dictionaries
    """
    records: list[dict[str, Any]] = []
    rows = csv.reader(lines)
    if headers is None:
        headers = next(rows)
    for row in rows:
        record: dict[str, Any] = {
            name: func(val) for name, func, val in zip(headers, types, row)
        }
        records.append(record)
    return records


def csv_as_instances(
    lines: Iterable[str], cls: stock.Stock, headers: Iterable[str] | None = None
) -> list[stock.Stock]:
    """
    Convert lines of CSV data into a list of instances
    """

    records: list[stock.Stock] = []
    rows = csv.reader(lines)
    if headers is None:
        headers = next(rows)
    for row in rows:
        record = cls.from_row(row)
        records.append(record)
    return records


def read_csv_as_dicts(
    file_name: str, types: Iterable[type], *, headers: Iterable[str] | None = None
) -> list[dict[str, Any]]:
    """
    Read CSV data into a list of dictionaries with optional type conversion
    """
    with open(file_name, mode="r") as file:
        return csv_as_dicts(file, types, headers=headers)


def read_csv_as_instances(
    file_name: str, cls: stock.Stock, *, headers: Iterable[str] | None = None
) -> list[stock.Stock]:
    """
    Read CSV data into a list of instances
    """
    with open(file_name, mode="r") as file:
        return csv_as_instances(file, cls, headers=headers)
