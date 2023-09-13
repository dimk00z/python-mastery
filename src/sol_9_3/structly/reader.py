import csv
import logging
from typing import Any, Callable, Iterable, Type

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def convert_csv(
    lines: Iterable[Any],
    converter: Callable[[list[str], list[str]], Any],
    *,
    headers=None
) -> list[Any]:
    """
    Convert lines of CSV data into data that depends on converter.
    """
    rows = csv.reader(lines)
    if headers is None:
        headers = next(rows)
    results = []
    for index, row in enumerate(rows, start=1):
        try:
            results.append(converter(headers, row))
        except ValueError as ex:
            logger.info("Row %d: Bad row: %s", index, row)
            logger.debug("Row %d Reason: %s", index, ex)
    return results


def csv_as_dicts(
    lines: Iterable[str], types: Iterable[type], headers: Iterable[str] | None = None
) -> list[dict[str, Any] | Any]:
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
    lines: Iterable[str], cls, headers: Iterable[str] | None = None
) -> list[Type]:
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
