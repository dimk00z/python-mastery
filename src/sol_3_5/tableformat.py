from typing import Type
from src.sol_3_4 import stock
from abc import ABC


class TableFormatter(ABC):
    def headings(self, headers):
        raise NotImplementedError()

    def row(self, rowdata):
        raise NotImplementedError()


class TextTableFormatter(TableFormatter):
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


class CSVTableFormatter(TableFormatter):
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


def create_formatter(formatter_type: str) -> TableFormatter:
    formatters: dict[str, Type[TableFormatter]] = {
        "text": TextTableFormatter,
        "html": HTMLTableFormatter,
        "csv": CSVTableFormatter,
    }
    if formatter_type not in formatters:
        raise RuntimeError(f"Unknown format {formatter_type}")
    return formatters[formatter_type]()


class HTMLTableFormatter(TableFormatter):
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
    formatter: TableFormatter,
):
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
