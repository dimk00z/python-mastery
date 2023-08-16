from src.sol_3_1 import stock


def print_table(
    portfolios: list[stock.Stock],
    fields: list[str],
):
    print(
        " ".join(
            (f"{field:>10}" for field in fields),
        ),
    )
    print(
        " ".join(
            (f"{'-'*10}" for _ in range(len(fields))),
        ),
    )

    for portfolio in portfolios:
        print(
            " ".join(
                (f"{getattr(portfolio,field):>10}" for field in fields),
            ),
        )


if __name__ == "__main__":
    portfolios = stock.read_portfolio("Data/portfolio.csv")
    print_table(
        portfolios=portfolios,
        fields=["name", "shares", "price"],
    )
    print_table(
        portfolios=portfolios,
        fields=[
            "name",
            "shares",
        ],
    )
    print_table(
        portfolios=portfolios,
        fields=[
            "shares",
        ],
    )
