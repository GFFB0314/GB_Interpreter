"""This module provides a lexer for a simple programming language."""

# Define token types
NUMBER = "NUMBER"
IDENT = "IDENT"
SYMBOL = "SYMBOL"
STRING = "STRING"


class Token:
    """Token class represents a single token in the input string."""

    def __init__(self, type_, value):
        """Initializes a Token object with a type and value."""
        self.type = type_
        self.value = value

    def __repr__(self):
        """Represent a Token object."""
        return f"Token({self.type}, {self.value})"

    def __eq__(self, other):
        """Check if two tokens are equal based on their type and value."""
        return (
            isinstance(other, Token)
            and self.type == other.type
            and self.value == other.value
        )


def lex(input_str: str) -> list[Token]:
    """Splitting sequence of characters into a sequence of tokens"""
    tokens: list[Token] = []
    i: int = 0
    while i < len(input_str):
        ch = input_str[i]

        if ch.isspace():
            i += 1
            continue

        # FIXED: Added support for line comments.
        # If a '#' is found, we skip all characters until a newline is encountered.
        if ch == "#":
            i += 1  # Move past the '#'
            # Keep advancing until the end of the string or a newline character
            while i < len(input_str) and input_str[i] != "\n":
                i += 1
            continue  # Restart the loop to process the next character

        if ch == '"':
            i += 1  # Consume the opening quote
            str_val = ""
            while i < len(input_str) and input_str[i] != '"':
                str_val += input_str[i]
                i += 1
            if i >= len(input_str):
                raise ValueError("Unterminated string literal")
            i += 1  # Consume the closing quote
            tokens.append(Token(STRING, str_val))
            continue

        if ch.isdigit():
            num = ch
            i += 1
            while i < len(input_str) and input_str[i].isdigit():
                num += input_str[i]
                i += 1
            tokens.append(Token(NUMBER, int(num)))
            continue

        if ch.isalpha() or ch == "_":
            ident = ch
            i += 1
            while i < len(input_str) and (
                input_str[i].isalnum() or input_str[i] == "_"
            ):
                ident += input_str[i]
                i += 1
            tokens.append(Token(IDENT, ident))
            continue

        if ch in ["+", "-", "*", "/", "=", "!", "<", ">", ";", "(", ")", "{", "}", ","]:
            next_ch = input_str[i + 1] if i + 1 < len(input_str) else ""
            two_char_sym = ch + next_ch
            if two_char_sym in ["==", "!=", "<=", ">="]:
                tokens.append(Token(SYMBOL, two_char_sym))
                i += 2
            else:
                tokens.append(Token(SYMBOL, ch))
                i += 1
        else:
            raise ValueError(f"Unknown character: {ch}")

    return tokens


if __name__ == "__main__":
    print(lex("sup x = 3 + 4;"))
    # [Token(IDENT, 'sup'), Token(IDENT, 'x'), Token(SYMBOL, '='), Token(NUMBER, 3), Token(SYMBOL, '+'), Token(NUMBER, 4), Token(SYMBOL, ';')]

    correct_function_string = "def find_max(a, b) { if (a > b) { a; } else { b; } }"
    print(lex(correct_function_string))
    # [Token(IDENT, def), Token(IDENT, find_max), Token(SYMBOL, (), Token(IDENT, a), Token(SYMBOL, ,), Token(IDENT, b),
    # Token(SYMBOL, )), Token(SYMBOL, {), Token(IDENT, if), Token(SYMBOL, (), Token(IDENT, a), Token(SYMBOL, >),
    # Token(IDENT, b), Token(SYMBOL, )), Token(SYMBOL, {), Token(IDENT, a), Token(SYMBOL, ;), Token(SYMBOL, }),
    # Token(IDENT, else), Token(SYMBOL, {), Token(IDENT, b), Token(SYMBOL, ;), Token(SYMBOL, }), Token(SYMBOL, })]
