class TextTableFormatter(ITableFormatter):
    def headings(self, headers):
        print(
            " ".join(
                (f"{field:>10}" for field in headers),
            ),
        )
        print(
            " ".join(
                (f"{'-'*10}" for _ in range(len(headers))),
            ),
        )

    def row(self, rowdata):
        print(
            " ".join(
                (f"{field:>10}" for field in rowdata),
            ),
        )
