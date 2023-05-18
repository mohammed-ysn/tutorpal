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
