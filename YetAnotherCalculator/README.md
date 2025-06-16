# Auto
# C++ Console Calculator

A simple, yet powerful, command-line calculator written in C++. It features an interactive text-based user interface (TUI) that runs directly in the Windows console. The calculator correctly handles operator precedence and parentheses using the Shunting-yard algorithm.

![Language](https://img.shields.io/badge/language-C%2B%2B-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows-0078D6.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Screenshot

Here is a simulation of what the calculator looks like in the console:

```
-INPUT-------------
(3.5 + 1.5) * 10 / 2

-OUTPUT------------
25
-------------------
```

## Features

- **Basic Arithmetic:** Supports Addition (`+`), Subtraction (`-`), Multiplication (`*`), and Division (`/`).
- **Exponentiation:** Supports powers using the caret (`^`) symbol.
- **Operator Precedence:** Correctly evaluates expressions by following mathematical order of operations (e.g., `*` and `/` before `+` and `-`).
- **Parentheses:** Allows for grouping expressions with parentheses `()` to override default precedence.
- **Floating-Point Numbers:** Handles decimal inputs and calculations.
- **Interactive TUI:** A simple, clean interface built for the Windows console.
- **Live Editing:** Use `Backspace` to edit your input expression.

## How It Works

The calculator's core logic is based on a two-step process for evaluating mathematical expressions:

1.  **Infix to Postfix Conversion (Shunting-yard Algorithm):** The standard human-readable expression (infix notation, e.g., `5 + 3`) is converted into a postfix (Reverse Polish) notation (e.g., `5 3 +`). This conversion is done using Dijkstra's Shunting-yard algorithm, which makes the expression easy to evaluate with a stack.
2.  **Postfix Evaluation:** The postfix expression is then evaluated using a stack. Numbers are pushed onto the stack, and when an operator is encountered, the required number of operands are popped, the operation is performed, and the result is pushed back onto the stack.

## Requirements

-   **Operating System:** **Windows** is required due to the use of Windows-specific headers (`windows.h`, `conio.h`) for console cursor manipulation and keyboard input.
-   **Compiler:** A C++ compiler that supports C++11 or newer (e.g., **MinGW g++** or **MSVC**).

## How to Compile and Run

1.  Save the code as a `.cpp` file (e.g., `calculator.cpp`).
2.  Open a developer command prompt (like the one included with Visual Studio or a MinGW terminal).
3.  Navigate to the directory where you saved the file.
4.  Compile the code using g++:
    ```sh
    g++ calculator.cpp -o calculator.exe -static-libgcc -static-libstdc++
    ```
    *(The `-static` flags are recommended to bundle the C++ standard libraries, making the `.exe` more portable).*
5.  Run the executable from the command line:
    ```sh
    .\calculator.exe
    ```

## How to Use

-   Type your mathematical expression directly into the input area.
-   Press **`Enter`** to calculate and display the result.
-   Use **`Backspace`** to delete the character before the cursor.
-   Press **`ESC`** to exit the program.

## Code Overview

The code is structured into two main parts: the calculator logic and the user interface functions.

### Calculator Logic

-   `solve_str(string input)`: The main function that takes a raw string expression and returns the final calculated result.
-   `infix_to_postfix(const string& infix_string)`: Implements the Shunting-yard algorithm to convert an infix expression to a postfix queue.
-   `solve_postfix(queue<string> expr)`: Evaluates the postfix expression queue and returns the result.
-   `tokenize(const string& expr)`: Splits the input string into a vector of numbers and operators (e.g., `"10+5"` becomes `{"10", "+", "5"}`).
-   `priority(const string& op)`: Returns the precedence level of a given operator to guide the Shunting-yard algorithm.

### User Interface Functions

-   `ui_control()`: The main application loop that handles user keyboard input (`_getch()`, `_kbhit()`) and updates the display.
-   `display_input(...)` / `display_output(...)`: Functions responsible for drawing the TUI frame and displaying the input/output.
-   `setCursorPosition(...)` / `getCursorPosition(...)` / `gotoxy(...)`: Helper functions that use the Windows API to control the console cursor's position for a smooth TUI experience.

## Limitations & Future Improvements

-   **Platform Dependent:** The current implementation is strictly for Windows. It could be refactored to use a cross-platform library like **ncurses** to run on Linux/macOS.
-   **Error Handling:** Error handling is minimal. Invalid expressions (e.g., `5 * + 3`) or division by zero may cause the program to crash. Robust error detection and user feedback could be added.
-   **Advanced Editing:** While backspace is supported, more advanced editing features like full cursor movement with `Left`/`Right` arrow keys and insert/overwrite modes are not fully implemented.
-   **Extended Functions:** The calculator could be extended with trigonometric functions (`sin`, `cos`, etc.), logarithms, and constants like Pi.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
