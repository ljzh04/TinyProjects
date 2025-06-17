# my_dummy_project/main.py

# Import a function from the local utils module
from .utils import add_numbers, greet


def run_main():
    """
    Main function to demonstrate the dummy project.
    It calls functions from utils.py and prints the results.
    """
    print("Welcome to My Dummy Python Project!")

    num1 = 10
    num2 = 5
    sum_result = add_numbers(num1, num2)
    print(f"The sum of {num1} and {num2} is: {sum_result}")

    name = "Tester"
    greeting_message = greet(name)
    print(greeting_message)

    print("\nDummy project execution complete.")


if __name__ == "__main__":
    run_main()
