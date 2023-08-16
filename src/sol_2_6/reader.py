from typing import Collection, Type, Any
from pathlib import Path
import csv


def read_csv_as_dicts(filename: str, types: Collection[Type[Any]]):
    """
    Read a CSV file with column type conversion
    """
    records: list[dict[str, Any]] = []
    with open(Path(filename)) as f:
        rows = csv.reader(f)
        headers = next(rows)
        print(headers)
        for row in rows:
            record = {name: func(val) for name, func, val in zip(headers, types, row)}
            records.append(record)
    return records


if __name__ == "__main__":
    records = read_csv_as_dicts("Data/ctabus.csv", [str, str, str, int])
    print(len(records))
    print(records[0])
