from collections.abc import Sequence
import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Any, NamedTuple, Type

from msgspec import Struct
from pydantic import BaseModel


class RowTuple(NamedTuple):
    route: str
    date: str
    daytype: str
    rides: int


class RowPydantic(BaseModel):
    route: str
    date: str
    daytype: str
    rides: int


class RowStruct(Struct):
    route: str
    date: str
    daytype: str
    rides: int


@dataclass(
    slots=True,
)
class RowDataclassWithSlots:
    route: str
    date: str
    daytype: str
    rides: int


@dataclass
class RowDataclassWithotSlots:
    route: str
    date: str
    daytype: str
    rides: int


class RowSimple:
    def __init__(self, route, date, daytype, rides):
        self.route = route
        self.date = date
        self.daytype = daytype
        self.rides = rides


class RowWithSlots:
    __slots__ = ["route", "date", "daytype", "rides"]

    def __init__(self, route, date, daytype, rides):
        self.route = route
        self.date = date
        self.daytype = daytype
        self.rides = rides


data_path = Path("./Data/ctabus.csv")

TYPES_CLASSES = (
    RowTuple,
    RowSimple,
    RowWithSlots,
    RowDataclassWithotSlots,
    RowDataclassWithSlots,
    RowPydantic,
    RowStruct,
)
TYPES = (
    tuple,
    dict,
    *TYPES_CLASSES,
)


class RideData(Sequence):
    def __init__(self):
        self.routes = []  # Columns
        self.dates = []
        self.daytypes = []
        self.numrides = []

    def __len__(self):
        # All lists assumed to have the same length
        return len(self.routes)

    def __getitem__(self, index):
        return {
            "route": self.routes[index],
            "date": self.dates[index],
            "daytype": self.daytypes[index],
            "rides": self.numrides[index],
        }

    def append(self, d):
        self.routes.append(d["route"])
        self.dates.append(d["date"])
        self.daytypes.append(d["daytype"])
        self.numrides.append(d["rides"])


def read_rides(
    filename,
    result_type: Type[Any],
):
    """
    Read the bus ride data as a list of tuples
    """
    records: list[result_type] | RideData = [] if result_type != dict else RideData()
    with open(filename) as f:
        rows = csv.reader(f)
        next(rows)  # Skip headers
        for row in rows:
            route = row[0]
            date = row[1]
            daytype = row[2]
            rides = int(row[3])
            if result_type in TYPES_CLASSES:
                #     case tuple:
                record = result_type(
                    route=route,
                    date=date,
                    daytype=daytype,
                    rides=rides,
                )
                records.append(record)

            if result_type == tuple:
                records.append((route, date, daytype, rides))
            if result_type == dict:
                records.append(
                    {
                        "route": route,
                        "date": date,
                        "daytype": daytype,
                        "rides": rides,
                    }
                )
    return records


if __name__ == "__main__":
    import tracemalloc

    for res_type in TYPES:
        print(res_type)
        tracemalloc.start()
        rows = read_rides("Data/ctabus.csv", result_type=res_type)
        current, peak = tracemalloc.get_traced_memory()
        print(f"Memory Use: Current {current}, Peak {peak}")
        tracemalloc.stop()
