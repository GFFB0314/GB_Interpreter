import pytest
from Interpreter.parser import parse
from Interpreter.ast_nodes import (
    Number, Variable, String, BinOp, Assign, IfStmt, WhileStmt,
    FunctionDef, FunctionCall
)

def test_parse_single_assignment():
    """Tests parsing of a single assignment statement."""
    src = "x = 7;"
    ast = parse(src)
    assert ast == [Assign(Variable("x"), Number(7))]

def test_parse_expression_with_precedence():
    """Tests that the parser correctly handles operator precedence."""
    src = "1 + 2 * 3;"
    ast = parse(src)
    # Expected: 1 + (2 * 3)
    expected_expr = BinOp(Number(1), '+', BinOp(Number(2), '*', Number(3)))
    assert ast == [expected_expr]

def test_parse_if_statement():
    """Tests parsing of an if statement without an else block."""
    src = "if (x > 0) { x = 1; }"
    ast = parse(src)
    expected = [
        IfStmt(
            condition=BinOp(Variable('x'), '>', Number(0)),
            then_block=[Assign(Variable('x'), Number(1))],
            else_block=None
        )
    ]
    assert ast == expected

def test_parse_if_else_statement():
    """Tests parsing of a full if-else statement."""
    src = "if (a == b) { print(a); } else { print(b); }"
    ast = parse(src)
    expected = [
        IfStmt(
            condition=BinOp(Variable('a'), '==', Variable('b')),
            then_block=[FunctionCall('print', [Variable('a')])],
            else_block=[FunctionCall('print', [Variable('b')])]
        )
    ]
    assert ast == expected

def test_parse_while_loop():
    """Tests parsing of a while loop."""
    src = "while (i < 10) { i = i + 1; }"
    ast = parse(src)
    expected = [
        WhileStmt(
            condition=BinOp(Variable('i'), '<', Number(10)),
            body=[Assign(Variable('i'), BinOp(Variable('i'), '+', Number(1)))]
        )
    ]
    assert ast == expected

def test_parse_function_definition():
    """Tests parsing a function definition with multiple parameters."""
    src = "def add(a, b) { a + b; }"
    ast = parse(src)
    expected = [
        FunctionDef(
            name='add',
            params=['a', 'b'],
            body=[BinOp(Variable('a'), '+', Variable('b'))]
        )
    ]
    assert ast == expected

def test_parse_function_call():
    """Tests parsing a function call with arguments."""
    src = 'my_func(1, "hello");'
    ast = parse(src)
    expected = [
        FunctionCall(
            name='my_func',
            args=[Number(1), String('hello')]
        )
    ]
    assert ast == expected

def test_parse_multiple_statements():
    """Tests parsing a program with multiple statements."""
    src = "sup x = 1; sup y = 2; x + y;"
    ast = parse(src)
    assert len(ast) == 3
    assert isinstance(ast[0], Assign)
    assert isinstance(ast[1], Assign)
    assert isinstance(ast[2], BinOp)