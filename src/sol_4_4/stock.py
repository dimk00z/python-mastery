from decimal import Decimal

from validate import PositiveFloat, PositiveInteger, String


class Stock:
    name = String()
    shares = PositiveInteger()
    price = PositiveFloat()

    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price

    def __repr__(self):
        return f"Stock({self.name!r}, {self.shares!r}, {self.price!r})"

    @property
    def cost(self):
        return self.shares * self.price

    def sell(self, nshares):
        self.shares -= nshares


def read_portfolio(filename):
    """
    Read a CSV file of stock data into a list of Stocks
    """
    import csv

    portfolio = []
    with open(filename) as f:
        rows = csv.reader(f)
        next(rows)
        for row in rows:
            record = Stock.from_row(row)
            portfolio.append(record)
    return portfolio


class DStock(Stock):
    _types = (str, int, Decimal)


class Readonly:
    def __init__(self, obj):
        self.__dict__["_obj"] = obj

    def __setattr__(self, name, value):
        raise AttributeError("Can't set attribute")

    def __getattr__(self, name):
        return getattr(self._obj, name)


def main():
    from src.sol_3_2 import tableformat

    portfolio = read_portfolio("Data/portfolio.csv")

    # Generalized version
    # portfolio = reader.read_csv_as_instances('Data/portfolio.csv', Stock)
    tableformat.print_table(portfolio, ["name", "shares", "price"])
    # portfolio = reader.read_csv_as_instances('Data/portfolio.csv', Stock)
    tableformat.print_table(portfolio, ["name", "shares", "price"])


if __name__ == "__main__":
    pass
    # main()
