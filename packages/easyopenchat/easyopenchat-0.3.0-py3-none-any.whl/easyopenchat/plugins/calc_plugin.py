def plugin_calc(args):
    """
    Evaluate a simple mathematical expression.
    
    Args:
        args (str): Expression like "2 + 2".
    
    Returns:
        str: Result or error message.
    """
    try:
        return str(eval(args, {"__builtins__": {}}))
    except Exception as e:
        return f"Error: {str(e)}"