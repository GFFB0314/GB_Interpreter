from Interpreter.ast_nodes import (
    Number,
    Variable,
    String,
    BinOp,
    Assign,
    IfStmt,
    WhileStmt,
    FunctionDef,
    FunctionCall,
)


class NativeFunction:
    """Represents a function that is built-in to the interpreter (written in Python)."""

    def __init__(self, name, py_callable):
        """Store the function name and the Python callable."""
        self.name = name
        self.py_callable = py_callable  # The actual Python function to call

    def __repr__(self):
        """Represent the native function in a readable format."""
        return f"<native function: {self.name}>"


class Environment(dict):
    """Represents the environment in which the code is executed, storing variables."""

    def __init__(self, initial=None, outer=None):
        """This is the environment where variables are stored."""
        if initial:
            self.update(initial)
        self.outer = outer

    def __getitem__(self, name):
        """Retrieve a variable from the environment, checking outer scopes if necessary."""
        if name in self:
            return super().__getitem__(name)
        if self.outer:
            return self.outer[name]
        raise NameError(f"Undefined variable '{name}'")

    def __setitem__(self, name, value):
        """Set a variable in the environment, allowing for nested scopes."""
        super().__setitem__(name, value)


class Evaluator:
    """Evaluates the AST nodes and executes the code."""

    def __init__(self, env=None):
        """Initialize the evaluator with an environment."""
        self.env = env if env is not None else Environment()

    def eval(self, node):
        """Evaluate the AST node based on its type."""
        method_name = f"eval_{type(node).__name__}"
        evaluator_method = getattr(self, method_name, self.generic_eval)
        return evaluator_method(node)

    def generic_eval(self, node):
        """Fallback method for unknown node types."""
        raise TypeError(f"Unknown AST node type: {type(node)}")

    def eval_Number(self, node: Number):
        """Evaluate a Number node."""
        return node.value

    def eval_String(self, node: String):
        """Evaluate a String node."""
        return node.value

    def eval_Variable(self, node: Variable):
        """Evaluate a Variable node."""
        return self.env[node.name]

    def eval_Assign(self, node: Assign):
        """Evaluate an Assign node."""
        value = self.eval(node.value)
        self.env[node.name.name] = value
        return None

    def eval_BinOp(self, node: BinOp):
        """Evaluate a BinOp node."""
        left_val = self.eval(node.left)
        right_val = self.eval(node.right)
        op = node.op
        if op == "+" and isinstance(left_val, str) and isinstance(right_val, str):
            return left_val + right_val
        if op == "+":
            return left_val + right_val
        if op == "-":
            return left_val - right_val
        if op == "*":
            return left_val * right_val
        if op == "/":
            if right_val == 0:
                raise ZeroDivisionError("Division by zero")
            return left_val / right_val
        if op == "==":
            return left_val == right_val
        if op == "!=":
            return left_val != right_val
        if op == ">":
            return left_val > right_val
        if op == "<":
            return left_val < right_val
        if op == ">=":
            return left_val >= right_val
        if op == "<=":
            return left_val <= right_val
        raise ValueError(f"Unknown operator '{op}'")

    def eval_list(self, node: list):
        """Evaluate a Block node."""
        result = None
        for stmt in node:
            result = self.eval(stmt)
        return result

    def eval_IfStmt(self, node: IfStmt):
        """Evaluate an IfStatement node."""
        if self.eval(node.condition):
            return self.eval(node.then_block)
        elif node.else_block:
            return self.eval(node.else_block)
        return None

    def eval_WhileStmt(self, node: WhileStmt):
        """Evaluate a WhileLoop node."""
        result = None
        while self.eval(node.condition):
            result = self.eval(node.body)
        return result

    def eval_FunctionDef(self, node: FunctionDef):
        """Evaluate a Function Definition node."""
        self.env[node.name] = node
        return None

    # UPDATED: This method now handles both kinds of functions
    def eval_FunctionCall(self, node: FunctionCall):
        """Evaluate a Function Call node."""
        func = self.env[node.name]
        args = [self.eval(arg) for arg in node.args]

        if isinstance(func, FunctionDef):
            if len(args) != len(func.params):
                raise TypeError(
                    f"Function '{node.name}' expects {len(func.params)} arguments, but got {len(args)}"
                )
            local_env = Environment(outer=self.env)
            for name, val in zip(func.params, args):
                local_env[name] = val
            evaluator = Evaluator(local_env)
            return evaluator.eval(func.body)

        elif isinstance(func, NativeFunction):
            return func.py_callable(*args)

        else:
            raise TypeError(f"'{node.name}' is not a function")
