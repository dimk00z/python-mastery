import sys
from abc import ABC, abstractmethod
from typing import Type

from src.sol_3_4 import stock


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
    @abstractmethod
    def headings(self, headers):
        raise NotImplementedError()

    @abstractmethod
    def row(self, rowdata):
        raise NotImplementedError()


class UpperHeadersMixin:
    def headings(self, headers):
        super().headings([h.upper() for h in headers])


class ColumnFormatMixin:
    formats = []

    def row(self, rowdata):
        rowdata = [(fmt % item) for fmt, item in zip(self.formats, rowdata)]
        super().row(rowdata)


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


def create_formatter(
    formatter_name: str,
    column_formats=None,
    upper_headers: bool = False,
) -> ITableFormatter:
    formatters: dict[str, Type[ITableFormatter]] = {
        "text": TextTableFormatter,
        "html": HTMLTableFormatter,
        "csv": CSVTableFormatter,
    }
    if formatter_name not in formatters:
        raise RuntimeError(f"Unknown format {formatter_name}")
    formatter_cls = formatters[formatter_name]
    if column_formats:

        class formatter_cls(ColumnFormatMixin, formatter_cls):
            formats = column_formats

    if upper_headers:

        class formatter_cls(UpperHeadersMixin, formatter_cls):
            pass

    return formatter_cls()


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
        formatter=create_formatter(
            "text",
            upper_headers=True,
            column_formats=["%s", "%d", "%0.2f"],
        ),
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
    # with RedirectStdout(open("out.txt", "w")) as file:
    #     print_table(
    #         portfolios=portfolios,
    #         fields=["name", "shares", "price"],
    #         formatter=create_formatter("text"),
    #     )
    #     file.close()
