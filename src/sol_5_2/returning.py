import time


def parse_line(line: str, sep: str = "=") -> tuple[str, str] | None:
    if len(line.split(sep=sep)) < 2:
        return
    name, value = line.split(sep=sep)
    return name, value


def worker(x, y):
    print("About to work")
    time.sleep(20)
    print("Done")
    return x + y


def main():
    pass


if __name__ == "__main__":
    main()
