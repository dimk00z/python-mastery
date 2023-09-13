class CSVTableFormatter(ITableFormatter):
    def headings(self, headers):
        print(
            ",".join(
                (f"{field}" for field in headers),
            ),
        )

    def row(self, rowdata):
        print(
            ",".join(
                (f"{field}" for field in rowdata),
            ),
        )
