import csv
from pathlib import Path


class Stock:
    def __init__(
        self,
        name: str,
        shares: float | int,
        price: float | int,
    ):
        self.name = name
        self.shares = float(shares)
        self.price = float(price)

    def cost(self) -> float | int:
        return self.shares * self.price

    def sell(self, value: int | float):
        self.shares -= value
        return self.shares

    def __repr__(self) -> str:
        return "%10s %10d %10.2f" % (self.name, self.shares, self.price)


def read_portfolio(path: str) -> list[Stock]:
    with open(Path(path)) as file:
        rows = csv.reader(file)
        next(rows)
        return [Stock(*row) for row in rows]


def print_portfolio(portfolios):
    print("%10s %10s %10s" % ("name", "shares", "price"))
    print(("-" * 10 + " ") * 3)
    for p in portfolios:
        print(p)
