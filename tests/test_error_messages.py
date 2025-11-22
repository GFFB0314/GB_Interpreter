import pytest
from Interpreter.parser import parse

def test_missing_semicolon():
    code = 'sup x = 10 print("hi");'
    with pytest.raises(SyntaxError, match="Expected ';', got 'print'"):
        parse(code)

def test_missing_assignment_operator():
    code = 'sup x 10;'
    with pytest.raises(SyntaxError, match="Expected '=', got '10'"):
        parse(code)

def test_missing_closing_brace():
    code = 'if (1) { print("hi"); '
    with pytest.raises(SyntaxError, match="Unexpected end of input, expected SYMBOL }"):
        parse(code)
