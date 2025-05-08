
# from datetime import datetime

# def run():
#     return f"The current time is: {datetime.now().strftime('%H:%M:%S')}"


from datetime import datetime

def plugin_time(args=""):
    """
    Return the current time.
    
    Args:
        args (str): Optional timezone (not implemented).
    
    Returns:
        str: Current time.
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")