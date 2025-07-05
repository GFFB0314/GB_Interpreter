import pytest
from Interpreter.evaluator import Evaluator, Environment
from Interpreter.parser import parse

# Helper function to set up and run programs for tests
def evaluate_program(program_string, env=None):
    """Parses and evaluates a full program string."""
    ast = parse(program_string)
    evaluator = Evaluator(env if env is not None else Environment())
    last_result = None
    for statement in ast:
        last_result = evaluator.eval(statement)
    return last_result

def test_evaluate_arithmetic():
    """Tests basic arithmetic and precedence."""
    src = "sup x = (2 + 3) * 4; x;"
    assert evaluate_program(src) == 20

def test_evaluate_boolean_and_comparison():
    """Tests boolean and comparison operators."""
    assert evaluate_program("1 < 2;") == True
    assert evaluate_program("1 > 2;") == False
    assert evaluate_program("5 == 5;") == True
    assert evaluate_program('"a" != "b";') == True

def test_if_statement_execution():
    """Tests that the correct branch of an if statement is executed."""
    src_true = "sup x = 0; if (10 > 5) { x = 1; } else { x = 2; } x;"
    assert evaluate_program(src_true) == 1

    src_false = "sup x = 0; if (10 < 5) { x = 1; } else { x = 2; } x;"
    assert evaluate_program(src_false) == 2

def test_while_loop_execution():
    """Tests that a while loop executes correctly and terminates."""
    src = """
    sup i = 0;
    sup total = 0;
    while (i < 5) {
        total = total + i;
        i = i + 1;
    }
    total;
    """
    assert evaluate_program(src) == 10 # 0+1+2+3+4

def test_function_definition_and_call():
    """Tests defining a function and then calling it."""
    src = """
    def add(a, b) {
        sup result = a + b;
        result;
    }
    add(7, 8);
    """
    assert evaluate_program(src) == 15

def test_scope_of_variables():
    """Tests that variables inside a function do not leak into the global scope."""
    src = """
    sup x = 100;
    def my_func() {
        sup x = 5; # This x is local
    }
    my_func(); # Call the function
    x; # Should still be the global value
    """
    assert evaluate_program(src) == 100

def test_undefined_variable_error():
    """Tests that using an undefined variable raises a NameError."""
    with pytest.raises(NameError, match="Undefined variable 'y'"):
        evaluate_program("y + 1;")

def test_function_argument_mismatch_error():
    """Tests that calling a function with the wrong number of arguments raises a TypeError."""
    src = """
    def add(a, b) { a + b; }
    add(1);
    """
    with pytest.raises(TypeError, match="Function 'add' expects 2 arguments, but got 1"):
        evaluate_program(src)