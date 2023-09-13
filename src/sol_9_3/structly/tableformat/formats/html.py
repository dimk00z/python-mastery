class HTMLTableFormatter(ITableFormatter):
    def headings(self, headers):
        print(" ".join(("<tr>", *(f"<th>{field}</th>" for field in headers), "</tr>")))

    def row(self, rowdata):
        print(
            " ".join(
                ("<tr>", *(f"<td>{field}</td>" for field in rowdata), "</tr>"),
            )
        )
