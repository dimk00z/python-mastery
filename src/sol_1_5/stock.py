class Stock:
    def __init__(
        self,
        name: str,
        shares: float | int,
        price: float | int,
    ):
        self.name = name
        self.shares = shares
        self.price = price

    def cost(self) -> float | int:
        return self.shares * self.price
