from pathlib import Path
import logging

DATA_PATH = Path("Data/portfolio3.dat")


class CalcError(Exception):
    pass


def portfolio_cost(*, file_path: Path) -> float:
    with open(file_path, mode="r") as portfolio_file:
        result = 0
        for line in portfolio_file.readlines():
            fields = line.split()
            try:
                shares = float(fields[1])
                price = float(fields[2])
            except ValueError as ex:
                logging.error("Couldn't parse: %s", repr(line))
                logging.error("Reason: %s", ex)
                raise CalcError()

            result += price * shares

    return result


def main() -> None:
    try:
        print(
            "Total: ",
            portfolio_cost(
                file_path=DATA_PATH,
            ),
        )
    except CalcError:
        print("Got error")


if __name__ == "__main__":
    main()
