import sys
from abc import ABC, abstractmethod
from typing import Type


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


def print_table(
    portfolios: list[Type],
    fields: list[str],
    formatter: ITableFormatter,
):
    if not isinstance(formatter, ITableFormatter):
        raise TypeError("Wrong formatter type")
    formatter.headings(fields)

    for portfolio in portfolios:
        rowdata = [getattr(portfolio, fieldname) for fieldname in fields]
        formatter.row(rowdata)
