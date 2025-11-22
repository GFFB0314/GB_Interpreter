"""
Unit tests for verifying parser error messages.
Ensures that the parser provides helpful feedback for common syntax errors.
"""
import pytest
from Interpreter.parser import parse

def test_missing_semicolon():
    """Test that a missing semicolon raises a specific error."""
    code = 'sup x = 10 print("hi");'
    with pytest.raises(SyntaxError, match="Expected ';', got 'print'"):
        parse(code)

def test_missing_assignment_operator():
    """Test that a missing assignment operator raises a specific error."""
    code = 'sup x 10;'
    with pytest.raises(SyntaxError, match="Expected '=', got '10'"):
        parse(code)

def test_missing_closing_brace():
    """Test that a missing closing brace raises a specific error."""
    code = 'if (1) { print("hi"); '
    with pytest.raises(SyntaxError, match="Unexpected end of input, expected SYMBOL }"):
        parse(code)
