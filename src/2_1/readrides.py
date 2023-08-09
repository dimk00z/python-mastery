import csv
from pathlib import Path
from typing import NamedTuple, Type
from dataclasses import dataclass


class RowTuple(NamedTuple):
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


def read_rides_as_tuples(
    filename,
    result_type: Type[
        tuple
        | dict
        | RowTuple
        | RowSimple
        | RowWithSlots
        | RowDataclassWithSlots
        | RowDataclassWithotSlots
    ],
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
            if result_type in (
                RowTuple,
                RowSimple,
                RowWithSlots,
                RowDataclassWithotSlots,
                RowDataclassWithSlots,
            ):
                #     case tuple:
                record = result_type(route, date, daytype, rides)
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

    for res_type in (
        tuple,
        dict,
        RowTuple,
        RowSimple,
        RowWithSlots,
        RowDataclassWithotSlots,
        RowDataclassWithSlots,
    ):
        tracemalloc.start()
        rows = read_rides_as_tuples("Data/ctabus.csv", result_type=res_type)
        print("Memory Use: Current %d, Peak %d" % tracemalloc.get_traced_memory())
        tracemalloc.stop()


# Result type <class 'tuple'>
# Memory Use: Current 123688286, Peak 123718599
# Result type <class 'dict'>
# Memory Use: Current 188375302, Peak 188405671
# Result type <class '__main__.RowTuple'>
# Memory Use: Current 128309014, Peak 128339311
# Result type <class '__main__.RowSimple'>
# Memory Use: Current 142173206, Peak 142203495
# Result type <class '__main__.RowWithSlots'>
# Memory Use: Current 119068110, Peak 119098391
# Result type <class '__main__.RowDataclassWithotSlots'>
# Memory Use: Current 142173334, Peak 142203607
# Result type <class '__main__.RowDataclassWithSlots'>
# Memory Use: Current 119068110, Peak 119098375
