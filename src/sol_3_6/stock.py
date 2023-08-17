from decimal import Decimal


class Stock:
    __slots__ = ("name", "_shares", "_price")

    _types = (str, int, float)

    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price

    @property
    def cost(self) -> int | float:
        return self.shares * self.price

    @property
    def shares(self):
        return self._shares

    @shares.setter
    def shares(self, value):
        shares_type = self._types[1]
        self._validate_number(
            value_type=shares_type,
            value=value,
        )
        self._shares = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        price_type = self._types[2]
        self._validate_number(
            value_type=price_type,
            value=value,
        )
        self._price = value

    def sell(self, nshares):
        self.shares -= nshares

    @staticmethod
    def _validate_number(value_type, value):
        if not isinstance(value, value_type):
            raise TypeError(f"Expected {value_type.__name__}")
        if value < 0:
            raise ValueError("value must be >= 0")

    @classmethod
    def from_row(cls, row):
        values = [func(val) for func, val in zip(cls._types, row)]
        return cls(*values)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}({self.name!r}, {self.shares!r}, {self.price!r})"
        )

    def __eq__(self, other):
        return isinstance(other, Stock) and (
            (self.name, self.shares, self.price)
            == (other.name, other.shares, other.price)
        )


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


if __name__ == "__main__":
    from src.sol_3_2 import tableformat

    portfolio = read_portfolio("Data/portfolio.csv")

    # Generalized version
    # portfolio = reader.read_csv_as_instances('Data/portfolio.csv', Stock)
    tableformat.print_table(portfolio, ["name", "shares", "price"])
