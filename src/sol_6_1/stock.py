from decimal import Decimal

from structure import Structure


class Stock(Structure):
    _fields = ("name", "shares", "price")

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


# if __name__ == "__main__":
#     from src.sol_3_2 import tableformat

#     portfolio = read_portfolio("Data/portfolio.csv")

#     # Generalized version
#     # portfolio = reader.read_csv_as_instances('Data/portfolio.csv', Stock)
#     tableformat.print_table(portfolio, ["name", "shares", "price"])
