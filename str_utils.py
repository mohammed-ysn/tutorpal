def truncate_str(string, max_length=16):
    """
    Truncates a string if it exceeds the maximum length, placing the ellipsis in the middle.

    Args:
        string (str): The string to truncate.
        max_length (int): The maximum length of the truncated string.

    Returns:
        str: The truncated string with ellipsis if necessary.

    """
    if len(string) <= max_length:
        return string
    else:
        half = (max_length - 3) // 2
        return string[:half] + "..." + string[-half:]
