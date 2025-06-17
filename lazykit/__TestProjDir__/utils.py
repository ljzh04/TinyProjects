# my_dummy_project/utils.py

def add_numbers(a: int, b: int) -> int:
    """
    Adds two numbers and returns their sum.

    Args:
        a (int): The first number.
        b (int): The second number.

    Returns:
        int: The sum of the two numbers.
    """
    return a + b


def greet(name: str) -> str:
    """
    Generates a personalized greeting message.

    Args:
        name (str): The name of the person to greet.

    Returns:
        str: A greeting message.
    """
    return f"Hello, {name}! This is a utility function working."
