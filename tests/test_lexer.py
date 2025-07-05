import pytest
from Interpreter.lexer import lex, Token, NUMBER, SYMBOL, IDENT, STRING

def test_simple_statement():
    """Tests a simple assignment statement."""
    src = "sup x = 5;"
    toks = lex(src)
    assert toks == [
        Token(IDENT, 'sup'),
        Token(IDENT, 'x'),
        Token(SYMBOL, '='),
        Token(NUMBER, 5),
        Token(SYMBOL, ';')
    ]

def test_complex_expression():
    """Tests a more complex expression with various symbols."""
    src = "(5 + 10) * 2;"
    toks = lex(src)
    assert toks == [
        Token(SYMBOL, '('),
        Token(NUMBER, 5),
        Token(SYMBOL, '+'),
        Token(NUMBER, 10),
        Token(SYMBOL, ')'),
        Token(SYMBOL, '*'),
        Token(NUMBER, 2),
        Token(SYMBOL, ';')
    ]

def test_string_literal():
    """Tests the tokenization of string literals."""
    src = 'sup message = "Hello, World!";'
    toks = lex(src)
    assert toks == [
        Token(IDENT, 'sup'),
        Token(IDENT, 'message'),
        Token(SYMBOL, '='),
        Token(STRING, "Hello, World!"),
        Token(SYMBOL, ';')
    ]

@pytest.mark.parametrize("src, expected", [
    ("a == b;", [Token(IDENT, 'a'), Token(SYMBOL, '=='), Token(IDENT, 'b'), Token(SYMBOL, ';')]),
    ("x!=y;",  [Token(IDENT, 'x'), Token(SYMBOL, '!='), Token(IDENT, 'y'), Token(SYMBOL, ';')]),
    ("n <= 10;", [Token(IDENT, 'n'), Token(SYMBOL, '<='), Token(NUMBER, 10), Token(SYMBOL, ';')]),
    ("m>=0;",  [Token(IDENT, 'm'), Token(SYMBOL, '>='), Token(NUMBER, 0), Token(SYMBOL, ';')]),
])
def test_multi_char_symbols(src, expected):
    """Tests that two-character symbols are correctly tokenized."""
    assert lex(src) == expected

def test_comment_handling():
    """Tests that comments are correctly ignored by the lexer."""
    src = """
    # This is a full-line comment.
    sup x = 10; # This is an inline comment.
    # Another comment.
    """
    toks = lex(src)
    assert toks == [
        Token(IDENT, 'sup'),
        Token(IDENT, 'x'),
        Token(SYMBOL, '='),
        Token(NUMBER, 10),
        Token(SYMBOL, ';')
    ]

def test_full_function_definition():
    """Tests tokenization of a complete function, including keywords and punctuation."""
    src = """
    def my_func(arg1, arg2) {
        return arg1 + arg2;
    }
    """
    # Note: 'return' is just an IDENT to the lexer.
    toks = lex(src)
    assert toks == [
        Token(IDENT, 'def'),
        Token(IDENT, 'my_func'),
        Token(SYMBOL, '('),
        Token(IDENT, 'arg1'),
        Token(SYMBOL, ','),
        Token(IDENT, 'arg2'),
        Token(SYMBOL, ')'),
        Token(SYMBOL, '{'),
        Token(IDENT, 'return'),
        Token(IDENT, 'arg1'),
        Token(SYMBOL, '+'),
        Token(IDENT, 'arg2'),
        Token(SYMBOL, ';'),
        Token(SYMBOL, '}'),
    ]