import sys
from typing import Type
from src.sol_3_4 import stock
from abc import ABC, abstractclassmethod


class RedirectStdout:
    def __init__(self, out_file):
        self.out_file = out_file

    def __enter__(self):
        self.stdout = sys.stdout
        sys.stdout = self.out_file
        return self.out_file

    def __exit__(self, ty, val, tb):
        sys.stdout = self.stdout


class ITableFormatter(ABC):
    @abstractclassmethod
    def headings(self, headers):
        raise NotImplementedError()

    @abstractclassmethod
    def row(self, rowdata):
        raise NotImplementedError()


class TextTableFormatter(ITableFormatter):
    def headings(self, headers):
        print(
            " ".join(
                (f"{field:>10}" for field in headers),
            ),
        )
        print(
            " ".join(
                (f"{'-'*10}" for _ in range(len(headers))),
            ),
        )

    def row(self, rowdata):
        print(
            " ".join(
                (f"{field:>10}" for field in rowdata),
            ),
        )


class CSVTableFormatter(ITableFormatter):
    def headings(self, headers):
        print(
            ",".join(
                (f"{field}" for field in headers),
            ),
        )

    def row(self, rowdata):
        print(
            ",".join(
                (f"{field}" for field in rowdata),
            ),
        )


class NewFormatter(ITableFormatter):
    def headers(self, headings):
        pass

    def row(self, rowdata):
        pass


def create_formatter(formatter_type: str) -> ITableFormatter:
    formatters: dict[str, Type[ITableFormatter]] = {
        "text": TextTableFormatter,
        "html": HTMLTableFormatter,
        "csv": CSVTableFormatter,
    }
    if formatter_type not in formatters:
        raise RuntimeError(f"Unknown format {formatter_type}")
    return formatters[formatter_type]()


class HTMLTableFormatter(ITableFormatter):
    def headings(self, headers):
        print(" ".join(("<tr>", *(f"<th>{field}</th>" for field in headers), "</tr>")))

    def row(self, rowdata):
        print(
            " ".join(
                ("<tr>", *(f"<td>{field}</td>" for field in rowdata), "</tr>"),
            )
        )


def print_table(
    portfolios: list[stock.Stock],
    fields: list[str],
    formatter: ITableFormatter,
):
    if not isinstance(formatter, ITableFormatter):
        raise TypeError("Wrong formatter type")
    formatter.headings(fields)

    for portfolio in portfolios:
        rowdata = [getattr(portfolio, fieldname) for fieldname in fields]
        formatter.row(rowdata)


if __name__ == "__main__":
    portfolios = stock.read_portfolio("Data/portfolio.csv")
    print_table(
        portfolios=portfolios,
        fields=["name", "shares", "price"],
        formatter=create_formatter("text"),
    )
    print_table(
        portfolios=portfolios,
        fields=[
            "name",
            "shares",
        ],
        formatter=create_formatter("csv"),
    )
    print_table(
        portfolios=portfolios,
        fields=["name", "shares", "price"],
        formatter=create_formatter("html"),
    )
    with RedirectStdout(open("out.txt", "w")) as file:
        print_table(
            portfolios=portfolios,
            fields=["name", "shares", "price"],
            formatter=create_formatter("text"),
        )
        file.close()
