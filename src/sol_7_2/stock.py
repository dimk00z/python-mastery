from structure import Structure
from validate import Integer, validated


class Stock(Structure):
    _fields = ("name", "shares", "price")

    @property
    def cost(self):
        return self.shares * self.price

    @validated
    def sell(self, nshares: Integer):
        self.shares -= nshares

    # sell = ValidatedFunction(sell)


Stock.create_init()
