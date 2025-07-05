"""
General Interpreter logic.
General Overview of the interpreter's logic flow
It includes steps for tokenization, parsing, building an abstract syntax tree (AST) and evaluation.
"""

"""STEP 1: TOKENS & LEXING"""


def lex(input_str: str) -> list:
    """Splitting sequence of characters into a sequence of tokens."""
    tokens: list = []  # List of tokens
    for part in input_str.split():  # Super-simple splitting
        if part.isdigit():
            tokens.append(("NUMBER", int(part)))
        elif part in ["+", "-", "*", "/", ";", "="]:
            tokens.append(("SYMBOL", part))
        else:
            tokens.append(("IDENT", part))

    return tokens


print("Step1")
print(lex("let x = 3 + 4 ;"))
print("\n")

tokens: list = lex("3 * 4")  # tokens = [("NUMBER",3),("SYMBOL","+"),("NUMBER",4)]
print(tokens)
print()

"""STEP 2: PARSING & THE PARSE TREE"""

pos = 0  # Initial index of each token in tokens


def parse_expression() -> tuple | int:
    """Parse a simple expression from the tokens."""
    global pos  # Allow modification of the global token index
    left: int = int(tokens[pos][1])
    pos += 1  # Move past the number

    # Check if there's another token (e.g., an operator)
    if pos < len(tokens):
        op = tokens[pos][1]
        if op in {"+", "-", "*", "/"}:
            pos += 1  # Skip the operator
            right: int = int(tokens[pos][1])
            pos += 1  # Skip the right operand
            op_name = {"+": "Add", "-": "Sub", "*": "Mul", "/": "Div"}[
                op
            ]  # Can also used get(op, "Unknown"). # But ensure the method actually returns op_name
            return (op_name, left, right)  # AST tuple
        else:
            raise SyntaxError(f"Unsupported operator: {op}")
    else:
        return left  # If there's no operator, return the number directly


print("Step 2")
print(parse_expression())
print()

"""STEP 3: ABSTRACT SYNTAX TREE (AST) LAYOUT"""


class Number:
    """AST node representing a numeric literal"""

    def __init__(self, value: int):
        """Store the numeric value in the node."""
        self.value = value

    def __repr__(self):
        return f"Number({self.value})"  # Facilitates reading


class BinOp:
    """AST node representing a binary operation (e.g +, -, *, /, ==, <, >)"""

    def __init__(self, op: str, left, right):
        """Store the left operand, operator and right operand in the node."""
        self.op, self.left, self.right = op, left, right


class Assign:
    """AST node representing an assignment operation"""

    def __init__(self, name, value):
        """Store the variable name and value in the node."""
        self.name, self.value = name, value


"""STEP 4: SEMANTIC ANALYSIS"""
"""FIRST SKIP IT"""

"""STEP 5: INTERPRETATION / EVALUATION"""

env: dict = {}


def eval_node(node: Assign):
    """Evaluate the AST node."""
    if isinstance(node, Number):
        return node.value
    if isinstance(node, BinOp):
        l = eval_node(node.left)
        r = eval_node(node.right)
        if node.op == "+":
            return l + r
        elif node.op == "-":
            return l - r
        elif node.op == "*":
            return l * r
        elif node.op == "/":
            return l // r
        else:
            raise ValueError(f"Unknown operator: {node.op}")
    if isinstance(node, Assign):
        env[node.name] = eval_node(node.value)
        return env[node.name]


# Example:
# Composition was applied here.
ast = Assign("x", BinOp("/", Number(15), Number(3)))
eval_node(ast)
print("Step 5")
print(f'AST, ("{ast.value.op}", {ast.value.left}, {ast.value.right})')
print(env["x"])
