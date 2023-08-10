import csv
import time
from dataclasses import dataclass
from functools import wraps
from pathlib import Path
from typing import Any, NamedTuple, Type
from msgspec import Struct
from pydantic import BaseModel


def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f"Function {func.__name__}{args} {kwargs} Took {total_time:.4f} seconds")
        return result

    return timeit_wrapper


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


@timeit
def read_rides_as_tuples(
    filename,
    result_type: Type[Any],
):
    """
    Read the bus ride data as a list of tuples
    """
    records: list[result_type] = []
    print("Result type", result_type)
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
    print(f"Total {len(records)}")
    return records


if __name__ == "__main__":
    import tracemalloc

    for res_type in TYPES:
        tracemalloc.start()
        rows = read_rides_as_tuples("Data/ctabus.csv", result_type=res_type)
        current, peak = tracemalloc.get_traced_memory()
        print(f"Memory Use: Current {current}, Peak {peak}")
        tracemalloc.stop()

# Result type <class 'tuple'>
# Memory Use: Current 123688139, Peak 123718519
# Result type <class 'dict'>
# Memory Use: Current 188375438, Peak 188405807
# Result type <class '__main__.RowTuple'>
# Memory Use: Current 128309110, Peak 128339407
# Result type <class '__main__.RowSimple'>
# Memory Use: Current 142173254, Peak 142203543
# Result type <class '__main__.RowWithSlots'>
# Memory Use: Current 119068038, Peak 119098319
# Result type <class '__main__.RowDataclassWithotSlots'>
# Memory Use: Current 142173318, Peak 142203591
# Result type <class '__main__.RowDataclassWithSlots'>
# Memory Use: Current 119067982, Peak 119098247
# Result type <class '__main__.RowPydantic'> -v2
# Memory Use: Current 359334494, Peak 359364807
# Result type <class '__main__.RowPydantic'> -v1
# Memory Use: Current 345473582, Peak 345503895
# Result type <class '__main__.RowStruct'>
# Memory Use: Current 119067750, Peak 119098055
