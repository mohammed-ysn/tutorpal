def print_table(headers, rows):
    """
    Prints a formatted table of data.

    Args:
        headers (list of str): The headers of the table.
        rows (list of tuples): The rows of data to be displayed in the table.

    """
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


def truncate_str(string, max_length=16):
    """
    Truncates a string to a specified maximum length and adds ellipsis if necessary.

    Args:
        string (str): The input string to truncate.
        max_length (int): The maximum length of the truncated string. Default is 16.

    Returns:
        str: The truncated string with ellipsis if necessary.

    """
    if len(string) <= max_length:
        return string
    else:
        half = (max_length - 3) // 2
        return string[:half] + "..." + string[-half:]
