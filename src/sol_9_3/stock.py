import structly


class Stock(structly.Structure):
    name = structly.String()
    shares = structly.PositiveInteger()
    price = structly.PositiveFloat()

    @property
    def cost(self):
        return self.shares * self.price

    def sell(self, nshares):
        self.shares -= nshares


if __name__ == "__main__":
    portfolio = structly.read_csv_as_instances("../../Data/portfolio.csv", Stock)
    formatter = structly.create_formatter("text")
    structly.print_table(portfolio, ["name", "shares", "price"], formatter)
