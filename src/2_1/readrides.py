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
# Function read_rides_as_tuples('Data/ctabus.csv',) {'result_type': <class 'tuple'>} Took 2.1695 seconds
# Memory Use: Current 123687582, Peak 123717871
# Result type <class 'dict'>
# Function read_rides_as_tuples('Data/ctabus.csv',) {'result_type': <class 'dict'>} Took 2.2279 seconds
# Memory Use: Current 188375382, Peak 188405775
# Result type <class '__main__.RowTuple'>
# Function read_rides_as_tuples('Data/ctabus.csv',) {'result_type': <class '__main__.RowTuple'>} Took 2.2949 seconds
# Memory Use: Current 128309102, Peak 128339375
# Result type <class '__main__.RowSimple'>
# Function read_rides_as_tuples('Data/ctabus.csv',) {'result_type': <class '__main__.RowSimple'>} Took 2.7460 seconds
# Memory Use: Current 142173422, Peak 142203687
# Result type <class '__main__.RowWithSlots'>
# Function read_rides_as_tuples('Data/ctabus.csv',) {'result_type': <class '__main__.RowWithSlots'>} Took 2.5472 seconds
# Memory Use: Current 119068206, Peak 119098463
# Result type <class '__main__.RowDataclassWithotSlots'>
# Function read_rides_as_tuples('Data/ctabus.csv',) {'result_type': <class '__main__.RowDataclassWithotSlots'>} Took 2.6040 seconds
# Memory Use: Current 142173486, Peak 142203735
# Result type <class '__main__.RowDataclassWithSlots'>
# Function read_rides_as_tuples('Data/ctabus.csv',) {'result_type': <class '__main__.RowDataclassWithSlots'>} Took 2.5886 seconds
# Memory Use: Current 119068150, Peak 119098391
# Result type <class '__main__.RowPydantic'>
# Function read_rides_as_tuples('Data/ctabus.csv',) {'result_type': <class '__main__.RowPydantic'>} Took 4.3285 seconds
# Memory Use: Current 359334406, Peak 359364695
# Result type <class '__main__.RowStruct'>
# Function read_rides_as_tuples('Data/ctabus.csv',) {'result_type': <class '__main__.RowStruct'>} Took 1.8755 seconds
# Memory Use: Current 119067814, Peak 119098143
# ❯ poetry run ipython src/2_1/readrides.py
# Result type <class 'tuple'>
# Total 577563
# Function read_rides_as_tuples('Data/ctabus.csv',) {'result_type': <class 'tuple'>} Took 2.0230 seconds
# Memory Use: Current 123688374, Peak 123718663
# Result type <class 'dict'>
# Total 577563
# Function read_rides_as_tuples('Data/ctabus.csv',) {'result_type': <class 'dict'>} Took 2.2997 seconds
# Memory Use: Current 188375382, Peak 188405775
# Result type <class '__main__.RowTuple'>
# Total 577563
# Function read_rides_as_tuples('Data/ctabus.csv',) {'result_type': <class '__main__.RowTuple'>} Took 2.2853 seconds
# Memory Use: Current 128309102, Peak 128339375
# Result type <class '__main__.RowSimple'>
# Total 577563
# Function read_rides_as_tuples('Data/ctabus.csv',) {'result_type': <class '__main__.RowSimple'>} Took 2.7319 seconds
# Memory Use: Current 142173422, Peak 142203687
# Result type <class '__main__.RowWithSlots'>
# Total 577563
# Function read_rides_as_tuples('Data/ctabus.csv',) {'result_type': <class '__main__.RowWithSlots'>} Took 2.5442 seconds
# Memory Use: Current 119068206, Peak 119098463
# Result type <class '__main__.RowDataclassWithotSlots'>
# Total 577563
# Function read_rides_as_tuples('Data/ctabus.csv',) {'result_type': <class '__main__.RowDataclassWithotSlots'>} Took 2.5923 seconds
# Memory Use: Current 142173486, Peak 142203735
# Result type <class '__main__.RowDataclassWithSlots'>
# Total 577563
# Function read_rides_as_tuples('Data/ctabus.csv',) {'result_type': <class '__main__.RowDataclassWithSlots'>} Took 2.5742 seconds
# Memory Use: Current 119068150, Peak 119098391
# Result type <class '__main__.RowPydantic'>
# Total 577563
# Function read_rides_as_tuples('Data/ctabus.csv',) {'result_type': <class '__main__.RowPydantic'>} Took 4.4060 seconds
# Memory Use: Current 359334662, Peak 359364951
# Result type <class '__main__.RowStruct'>
# Total 577563
# Function read_rides_as_tuples('Data/ctabus.csv',) {'result_type': <class '__main__.RowStruct'>} Took 1.8238 seconds
# Memory Use: Current 119067814, Peak 119098143
