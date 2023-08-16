from pathlib import Path
from readrides import read_rides, RowStruct
from collections import Counter, defaultdict
from pprint import pprint


def total_number_of_rides(rides: list[RowStruct]) -> Counter:
    results: Counter = Counter()
    for row in rides:
        results[row.route] += row.rides
    return results


def get_bus_stat(rides: list[RowStruct], route: str, needed_date: str) -> int:
    return sum(
        (row.rides for row in rides if row.route == route and row.date == needed_date)
    )


def ridies_by_year(rides: list[RowStruct]) -> dict[int, Counter]:
    results: dict[int, Counter] = defaultdict(Counter)
    for row in rides:
        year = int(row.date.split("/")[-1])
        results[year][row.route] += row.rides
    return results


def get_rides_increase_by_year(
    ridies_by_year: dict[int, Counter], first_year: int, last_year: int
):
    return ridies_by_year[last_year] - ridies_by_year[first_year]


if __name__ == "__main__":
    data_path = Path("./Data/ctabus.csv")
    rides = read_rides(filename=data_path, result_type=RowStruct)
    buses_with_rides = total_number_of_rides(rides=rides)
    print("How many bus routes exist in Chicago?")
    pprint(f"Total buses routes {len(buses_with_rides)}")
    print("Most common:")
    pprint(tuple(buses_with_rides.most_common(5)))

    pprint(buses_with_rides["22"])
    print("How many people rode the number 22 bus on February 2, 2011?")
    pprint(get_bus_stat(rides=rides, route="22", needed_date="02/02/2011"))
    rides_with_years = ridies_by_year(rides=rides)
    print(
        "What five bus routes had the greatest ten-year increase in ridership from 2001 to 2011?"
    )
    diffs = get_rides_increase_by_year(rides_with_years, 2001, 2011)
    pprint(tuple(diffs.most_common(5)))
