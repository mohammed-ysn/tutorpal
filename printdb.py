import sqlite3

from str_utils import truncate_str


def print_pretty_table(table_name):
    """
    Prints a formatted table of data retrieved from the specified table in an SQLite database.

    Args:
        table_name (str): The name of the table to retrieve data from.

    """
    # connect to the SQLite database
    conn = sqlite3.connect("tutoring.db")
    cursor = conn.cursor()

    # execute a query to retrieve data from the specified table
    cursor.execute(f"SELECT * FROM {table_name}")

    # fetch all rows from the result
    rows = cursor.fetchall()

    # get the column names from the cursor description
    headers = [desc[0] for desc in cursor.description]

    conn.close()

    max_column_width = 16

    # set the maximum width for each column to the longest cell
    # but cut off at 16
    max_widths = [
        min(max_column_width, max(len(header), max(len(str(row[i])) for row in rows)))
        for i, header in enumerate(headers)
    ]

    # truncate and align the headers
    header_data = [
        truncate_str(header, max_width).ljust(max_width)
        for header, max_width in zip(headers, max_widths)
    ]
    print(" | ".join(header_data))
    print("-" * (sum(max_widths) + (3 * len(headers) - 1)))  # Separator line

    # truncate and align the data rows
    for row in rows:
        row_data = [
            truncate_str(str(item), max_width).ljust(max_width)
            for item, max_width in zip(row, max_widths)
        ]
        print(" | ".join(row_data))
