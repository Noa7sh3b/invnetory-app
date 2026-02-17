from io import BytesIO
import pandas as pd
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors


def products_to_excel(products):
    df = pd.DataFrame(products)
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Products")
    output.seek(0)
    return output.read()


def products_to_pdf(products):
    output = BytesIO()
    doc = SimpleDocTemplate(output, pagesize=landscape(A4))
    data = [list(products[0].keys())] if products else [["No data"]]
    for item in products:
        data.append([str(value) for value in item.values()])
    table = Table(data, repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e88ff")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        )
    )
    doc.build([table])
    output.seek(0)
    return output.read()


def products_to_print_html(products):
    if not products:
        return "<p>No data</p>"
    headers = "".join(f"<th>{h}</th>" for h in products[0].keys())
    rows = []
    for item in products:
        cols = "".join(f"<td>{value}</td>" for value in item.values())
        rows.append(f"<tr>{cols}</tr>")
    body = "".join(rows)
    return f"""
    <table border="1" cellpadding="4" cellspacing="0">
        <thead><tr>{headers}</tr></thead>
        <tbody>{body}</tbody>
    </table>
    """
