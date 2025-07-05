# GB Interpreter 🧩 

Welcome to the **GB Interpreter** – a simple, general-purpose programming language built entirely from scratch in Python. This project is a deep dive into the fundamentals of language design, featuring a complete pipeline from raw text to computed result. It's an ideal learning tool for anyone interested in how programming languages work under the hood.


## Table of Contents
- [GB Interpreter 🧩](#gb-interpreter-)
  - [Table of Contents](#table-of-contents)
  - [About the Project 📖](#about-the-project-)
    - [✨ Key Features:](#-key-features)
  - [Technologies \& Libraries Used 🛠️](#technologies--libraries-used-️)
  - [Getting Started 🚀](#getting-started-)
    - [Prerequisites](#prerequisites)
    - [⚙️ Installation](#️-installation)
  - [Usage Guide 🖥️](#usage-guide-️)
    - [1. Interactive Mode (REPL)](#1-interactive-mode-repl)
    - [2. Script Mode](#2-script-mode)
  - [Contributing 🤝](#contributing-)
  - [Contact ✉️](#contact-️)
  - [License ©️](#license-️)


## About the Project 📖

The GB Interpreter started as a simple expression evaluator and evolved into a feature-rich language. The entire architecture is modeled after a restaurant, making it easy to understand:

*   **The Waiter (`repl.py`):** The user-facing Read-Eval-Print-Loop (REPL) that takes your orders.
*   **The Prep Cook (`lexer.py`):** Chops your code into a clean list of tokens.
*   **The Sous-Chef (`parser.py`):** Writes the tokens onto structured "recipe cards" (an Abstract Syntax Tree, or AST).
*   **The Head Chef (`evaluator.py`):** Executes the recipe to produce the final result.

This project was built to be both functional and educational, demonstrating core computer science concepts in a tangible way.

### ✨ Key Features:

*   **Variables:** Declare variables with `sup my_var = 10;` or assign directly with `my_var = 10;`.
*   **Control Flow:** Full support for `if`/`else` statements and `while` loops.
*   **Functions:** Define your own functions with parameters using `def my_func(a, b) { ... }`.
*   **Data Types:** Handles integers and double-quoted strings, including string concatenation.
*   **Rich Operators:** Includes arithmetic (`+`, `-`, `*`, `/`) and all comparison/equality operators (`==`, `!=`, `>`, `<`, etc.) with correct precedence.
*   **Built-in Functions:** Comes with native functions like `print()` and `input()` right out of the box.
*   **Two Execution Modes:** Run code interactively in the REPL or execute `.gb` script files directly.
*   **Robust Error Handling:** Provides clear error messages for syntax, runtime, and name errors.

---

## Technologies & Libraries Used 🛠️

This project keeps its dependencies minimal to focus on the core logic.

*   🐍 **Python 3:** The core language used to build the interpreter.
*   📦 **Pytest:** Used for the comprehensive unit test suite to ensure code quality and correctness.

---

## Getting Started 🚀

Follow these steps to get a local copy up and running.

### Prerequisites

Make sure you have Python 3 installed on your system.
*   **Python 3.x**

You will also need `pip` to install the testing library.

### ⚙️ Installation

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/GFFB0314/GB_Interpreter.git
    cd GB_Interpreter
    ```

2.  **Project Structure:**
    The code is organized into two main directories:
    *   `Interpreter/`: Contains the core logic for the lexer, parser, evaluator, etc.
    *   `tests/`: Contains all the unit tests.

3.  **Install development dependencies:**
    For running the tests, you'll need `pytest`. It's recommended to create a `requirements.txt` file.

    Create a file named `requirements.txt` and add the following line:
    ```
    pytest
    ```
    Then, install it:
    ```sh
    pip install -r requirements.txt
    ```

4.  **Run the tests (Optional but Recommended):**
    Verify that everything is set up correctly by running the test suite.
    ```sh
    python -m pytest
    ```
    You should see all 29 tests pass! ✅

---

## Usage Guide 🖥️

You can run the GB Interpreter in two modes:

### 1. Interactive Mode (REPL)

This mode is perfect for experimenting and trying out code snippets.

*   **To start the REPL:**
    ```sh
    python repl.py
    ```
*   **Example Session:**
    ```
    Simple Interpreter v1.5 (Robust Interrupts). Type 'quit' or 'exit' to leave.
    >>> def say_hello(name) {
    ...     print("Hello, " + name + "!");
    ... }
    >>> say_hello("World");
    'Hello, World!'
    >>> quit
    Goodbye!
    ```

### 2. Script Mode

This mode allows you to execute programs written in `.gb` files.

*   **To run a script:**
    ```sh
    python repl.py path/to/your/script.gb
    ```
*   **Example Script (`example.gb`):**
    ```
    # A script to calculate the 5th Fibonacci number
    sup a = 0;
    sup b = 1;
    sup i = 0;

    while (i < 4) {
        sup temp = a + b;
        a = b;
        b = temp;
        i = i + 1;
    }

    # The final expression's value is printed
    b;
    ```
*   **Execution and Output:**
    ```sh
    > python repl.py example.gb
    5
    ```

---

## Contributing 🤝

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request.

1.  **Fork** the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a **Pull Request**

---

## Contact ✉️
For any questions, issues, or suggestions, please feel free to contact us at:
- Email: gbetnkom.bechir@gmail.com
- GitHub Issues: [Project Issues](https://github.com/GFFB0314/GB_Interpreter/issues)

---

## License ©️
**MIT License** 📝

**© 2025 Fares Gbetnkom**. This project is licensed under the **MIT License** — feel free to use, modify, and distribute it. See the full license text [here](LICENSE).

Thanks for using the **GB Intepreter**! 📜 Happy coding! 😊