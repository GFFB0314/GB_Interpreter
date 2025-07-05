"""
Gives the structure of the Abstract Syntax Tree (AST) nodes used in the interpreter.
This module defines the classes representing different types of nodes in the AST.
"""


class Number:
    """AST node representing a numeric literal"""

    def __init__(self, value: int):
        """Store the numeric value in the node."""
        self.value = value

    # Custom equality method. Without this, Python would only compare memory addresses,
    # causing tests like `Number('5') == Number('5')` to fail.
    def __eq__(self, other):
        """Equality check for testing"""
        return isinstance(other, Number) and self.value == other.value


class String:
    """AST node representing a string literal"""

    def __init__(self, value: str):
        """Store the string value in the node."""
        self.value = value

    def __eq__(self, other):
        """Equality check for testing"""
        return isinstance(other, String) and self.value == other.value


class Variable:
    """AST node representing a variable identifier"""

    def __init__(self, name: str):
        """Store the identifier value in the node."""
        self.name = name  # Store the variable name in the node

    # Custom equality method. Without this, Python would only compare memory addresses,
    # causing tests like `Variable('x') == Variable('x')` to fail.
    def __eq__(self, other):
        """Equality check for testing"""
        return isinstance(other, Variable) and self.name == other.name


class BinOp:
    """AST node representing a binary operation (e.g +, -, *, /, ==, <, >)"""

    def __init__(self, left, op: str, right):
        """Store the left operand, operator and right operand in the node."""
        self.left, self.op, self.right = left, op, right

    # Custom equality method for tests. It checks the operator and then
    # recursively calls the __eq__ method on the left and right nodes.
    # This is why Number and Variable also need their own __eq__ methods.
    def __eq__(self, other):
        """Equality check for testing"""
        return (
            isinstance(other, BinOp)
            and self.op == other.op
            and self.left == other.left
            and self.right == other.right
        )


class Assign:
    """AST node representing an assignment operation"""

    def __init__(
        self, name: Variable, value: Number | BinOp
    ):  # 'name' is the variable node, 'value' is the subtree for the value
        """Store the variable name and value in the node."""
        self.name = name
        self.value = value

    def __eq__(self, other):
        """Equality check for testing"""
        return (
            isinstance(other, Assign)
            and self.name.name == other.name.name
            and self.value == other.value
        )


class IfStmt:
    """Represents an if statement."""

    def __init__(self, condition, then_block, else_block=None):
        """Store the if-statement condition, then and else block in the node."""
        self.condition = condition
        self.then_block = then_block
        self.else_block = else_block

    def __eq__(self, other):
        """Equality check for testing"""
        return (
            isinstance(other, IfStmt)
            and self.condition == other.condition
            and self.then_block == other.then_block
            and self.else_block == other.else_block
        )


class WhileStmt:
    """Represents a while loop statement"""

    def __init__(self, condition, body):
        """Store the loop condition and body in the node."""
        self.condition = condition
        self.body = body

    def __eq__(self, other):
        """Equality check for testing"""
        return (
            isinstance(other, WhileStmt)
            and self.condition == other.condition
            and self.body == other.body
        )


class FunctionDef:
    """Represents a function definition in the AST"""

    def __init__(self, name, params, body):
        """Storoe the function name, params, body in the node."""
        self.name = name
        self.params = params
        self.body = body

    def __eq__(self, other):
        """Equality check for testing"""
        return (
            isinstance(other, FunctionDef)
            and self.name == other.name
            and self.params == other.params
            and self.body == other.body
        )


class FunctionCall:
    """Represents a function call in the AST"""

    def __init__(self, name, args):
        """Store the function name and arguments in the node."""
        self.name = name
        self.args = args

    def __eq__(self, other):
        """Equality check for testing"""
        return (
            isinstance(other, FunctionCall)
            and self.name == other.name
            and self.args == other.args
        )
