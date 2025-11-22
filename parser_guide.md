# Understanding the GB Interpreter Parser 🧠

Welcome to the engine room of the GB Interpreter! This guide explains how the **Parser** (`parser.py`) works. If the **Lexer** chops the ingredients (code) into pieces (tokens), the **Parser** is the Chef who organizes them into a structured recipe (Abstract Syntax Tree).

---

## 1. The Blueprint: EBNF 📐

Before writing code, we need a set of rules for our language. We use **EBNF** (Extended Backus-Naur Form), which is just a fancy way of saying "Grammar Rules".

It describes the structure of our language hierarchically.

### The Hierarchy (Order of Operations)
Notice how it flows from the **lowest** priority (Equality) to the **highest** priority (Factor). This ensures that `1 + 2 * 3` is treated as `1 + (2 * 3)` and not `(1 + 2) * 3`.

```ebnf
program        = statement*
statement      = if_stmt | while_stmt | func_def | assignment | expression ";"
block          = "{" statement* "}"

expression     = equality
equality       = comparison (("==" | "!=") comparison)*
comparison     = additive ((">" | "<" | ">=" | "<=") additive)*
additive       = term (("+" | "-") term)*
term           = factor (("*" | "/") factor)*
factor         = NUMBER | STRING | IDENTIFIER | "(" expression ")" | call
call           = IDENTIFIER "(" [expression ("," expression)*] ")"
```

**Relationship to Code:**
Each rule in the EBNF corresponds directly to a function in `parser.py`.
*   `program` -> `parse_program()`
*   `statement` -> `parse_statement()`
*   `additive` -> `parse_additive_expr()`

---

## 2. The Tools: Peek & Consume 🛠️

The parser reads tokens one by one using two main tools. Think of the list of tokens as a conveyor belt.

### `peek()` - The Eyes 👀
*   **What it does:** Looks at the *current* token on the belt without removing it.
*   **Why:** To decide what to do next. "Is this an `if` statement? Or a variable named `if_value`?"

### `consume(expected)` - The Hand ✋
*   **What it does:** Picks up the current token, verifies it's what we want, and moves the belt forward.
*   **Validation:** If we expect a `;` but find a `}`, `consume` stops everything and yells "Syntax Error!". This is where we catch mistakes like missing semicolons.

---

## 3. The Logic: Recursive Descent 🪆

Our parser uses a technique called **Recursive Descent**. It starts at the top (`parse_program`) and recursively calls functions to handle smaller and smaller parts of the code.

### Step-by-Step Walkthrough

#### A. `parse_program()` - The Manager
The entry point. It simply asks `parse_statement()` to handle tokens one by one until the file is empty.

#### B. `parse_statement()` - The Traffic Controller 🚦
It looks at the first token (`peek()`) to decide which rule to apply:
*   Starts with `if`? -> Call `parse_if_statement()`
*   Starts with `while`? -> Call `parse_while_statement()`
*   Starts with `sup`? -> It's a variable declaration.
*   Starts with `def`? -> It's a function definition.
*   None of the above? -> It must be an expression (like `print("hi")` or `1 + 1`).

#### C. The Expression Ladder (Math Logic) 🧮
When parsing math, we climb *down* the ladder of precedence.

1.  **`parse_expression()`**: Calls `parse_equality()`.
2.  **`parse_equality()`**: Handles `==` and `!=`. It calls `parse_comparison()` for the left side, checks for an operator, and calls `parse_comparison()` for the right side.
3.  **`parse_comparison()`**: Handles `>`, `<`, etc. Calls `parse_additive()`.
4.  **`parse_additive()`**: Handles `+` and `-`. Calls `parse_term()`.
5.  **`parse_term()`**: Handles `*` and `/`. Calls `parse_factor()`.
6.  **`parse_factor()`**: The bottom of the chain. It handles:
    *   Numbers (`42`)
    *   Strings (`"Hello"`)
    *   Variables (`x`)
    *   Parentheses `( ... )` -> **Recursion Alert!** If it sees `(`, it calls `parse_expression()` again to handle what's inside, resetting the priority.

---

## 4. Example Trace 🕵️‍♀️

Let's trace how the parser handles: `sup x = 1 + 2;`

1.  **`parse_statement()`** sees `sup`.
    *   It knows this is an assignment.
    *   Calls `consume(IDENT, "sup")`. (Eats `sup`)
    *   Calls `consume(IDENT)`. (Eats `x`)
    *   Calls `consume(SYMBOL, "=")`. (Eats `=`)
    *   Now it needs the *value*, so it calls **`parse_expression()`**.

2.  **`parse_expression()`** dives down the ladder...
    *   `equality` -> `comparison` -> `additive`...

3.  **`parse_additive()`**
    *   Calls `parse_term()` -> `parse_factor()` -> returns `1`.
    *   Sees `+`. Eats it.
    *   Calls `parse_term()` -> `parse_factor()` -> returns `2`.
    *   Creates a `BinOp` node: `(1 + 2)`.

4.  **Back to `parse_statement()`**
    *   It gets the `BinOp` node.
    *   Calls `consume(SYMBOL, ";")`. (Eats `;`)
    *   Returns an `Assign` node: `Assign(x, BinOp(1 + 2))`.

And that's it! The text `sup x = 1 + 2;` has been transformed into a structured object the computer can understand.
