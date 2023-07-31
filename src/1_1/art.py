import sys
import random

chars: str = r"\|/"


def draw(
    rows: int,
    columns: int,
) -> None:
    [
        print(
            "".join(
                (
                    random.choice(
                        chars,
                    )
                    for _ in range(
                        columns,
                    )
                )
            )
        )
        for _ in range(
            rows,
        )
    ]


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit(
            "Usage: art.py rows columns",
        )
    draw(
        rows=int(sys.argv[1]),
        columns=int(sys.argv[2]),
    )
