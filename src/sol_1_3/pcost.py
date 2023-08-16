from pathlib import Path

DATA_PATH = Path("Data/portfolio.dat")


def main() -> None:
    with open(DATA_PATH, mode="r") as portfolio_file:
        result = 0
        for line in portfolio_file.readlines():
            _, shares, price = line.split()
            result += float(price) * float(shares)

    print("Total: ", result)


if __name__ == "__main__":
    main()
