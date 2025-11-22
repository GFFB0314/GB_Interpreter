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
from Interpreter.lexer import lex, Token, NUMBER, SYMBOL, IDENT, STRING


class Parser:
    """Parses a sequence of tokens into an Abstract Syntax Tree (AST)."""

    def __init__(self, tokens: list[Token]):
        """Initializes the parser with a list of tokens."""
        self.tokens, self.pos = tokens, 0

    def peek(self):
        """Returns the current token without consuming it."""
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consume(self, expected_type=None, expected_value=None):
        """Consumes the next token if it matches the expected type and value."""
        token = self.peek()
        if token is None:
            raise SyntaxError(
                f"Unexpected end of input, expected {expected_type or ''} {expected_value or ''}"
            )
        if expected_value and token.value != expected_value:
            raise SyntaxError(f"Expected '{expected_value}', got '{token.value}'")
        if expected_type and token.type != expected_type:
            raise SyntaxError(f"Expected type '{expected_type}', got '{token.type}'")
        self.pos += 1
        return token

    def parse_factor(self):
        """
        Parses the highest-precedence expressions:
        - A numeric literal
        - A string literal (NEW)
        - A variable identifier
        - A parenthesized sub-expression
        - A function call
        """
        token = self.peek()
        if token is None:
            raise SyntaxError("Unexpected end of input, expected a factor.")

        # NEW: Handle String literals
        if token.type == STRING:
            self.consume(STRING)
            return String(token.value)

        if token.type == IDENT:
            if (
                self.pos + 1 < len(self.tokens)
                and self.tokens[self.pos + 1].value == "("
            ):
                return self.parse_function_call()
            self.consume(IDENT)
            return Variable(token.value)

        if token.type == NUMBER:
            self.consume(NUMBER)
            return Number(token.value)

        if token.type == SYMBOL and token.value == "(":
            self.consume(SYMBOL, "(")
            node = self.parse_expression()
            self.consume(SYMBOL, ")")
            return node

        raise SyntaxError(f"Unexpected token in expression: {token}")

    def parse_function_call(self):
        """Parses a function call expression."""
        name = self.consume(IDENT).value
        self.consume(SYMBOL, "(")
        args: list = []
        if not (
            self.peek() and self.peek().type == SYMBOL and self.peek().value == ")"
        ):
            while True:
                args.append(self.parse_expression())
                if self.peek() and self.peek().value == ",":
                    self.consume(SYMBOL, ",")
                else:
                    break
        self.consume(SYMBOL, ")")
        return FunctionCall(name, args)

    def parse_term(self):
        """Parses a term, which consists of factors combined by multiplication or division."""
        node = self.parse_factor()
        while True:
            token = self.peek()
            if token and token.type == SYMBOL and token.value in ("*", "/"):
                op, _ = token.value, self.consume(SYMBOL)
                right = self.parse_factor()
                node = BinOp(left=node, op=op, right=right)
            else:
                break
        return node

    def parse_additive_expr(self):
        """Parses an additive expression, which consists of terms combined by addition or subtraction."""
        node = self.parse_term()
        while True:
            token = self.peek()
            if token and token.type == SYMBOL and token.value in ("+", "-"):
                op, _ = token.value, self.consume(SYMBOL)
                right = self.parse_term()
                node = BinOp(left=node, op=op, right=right)
            else:
                break
        return node

    def parse_comparison_expr(self):
        """Parses a comparison expression, which consists of additive expressions combined by comparison operators."""
        node = self.parse_additive_expr()
        while True:
            token = self.peek()
            if token and token.type == SYMBOL and token.value in (">", "<", ">=", "<="):
                op, _ = token.value, self.consume(SYMBOL)
                right = self.parse_additive_expr()
                node = BinOp(left=node, op=op, right=right)
            else:
                break
        return node

    def parse_equality_expr(self):
        """Parses an equality expression, which consists of comparison expressions combined by equality operators."""
        node = self.parse_comparison_expr()
        while True:
            token = self.peek()
            if token and token.type == SYMBOL and token.value in ("==", "!="):
                op, _ = token.value, self.consume(SYMBOL)
                right = self.parse_comparison_expr()
                node = BinOp(left=node, op=op, right=right)
            else:
                break
        return node

    def parse_expression(self):
        """Parses a whole expression."""
        return self.parse_equality_expr()

    def parse_statement(self):
        """Parses a statement, which can be an expression, an assignment, a control flow statement, or a block."""
        token = self.peek()
        if token is None:
            return None

        if token.type == IDENT and token.value == "if":
            self.consume(IDENT, "if")
            self.consume(SYMBOL, "(")
            cond = self.parse_expression()
            self.consume(SYMBOL, ")")
            then_block = self.parse_block()
            else_block = None
            if (
                self.peek()
                and self.peek().type == IDENT
                and self.peek().value == "else"
            ):
                self.consume(IDENT, "else")
                else_block = self.parse_block()
            return IfStmt(cond, then_block, else_block)

        if token.type == IDENT and token.value == "sup":
            self.consume(IDENT, "sup")
            var_node = Variable(self.consume(IDENT).value)
            self.consume(SYMBOL, "=")
            expr = self.parse_expression()
            self.consume(SYMBOL, ";")
            return Assign(var_node, expr)

        if (
            token.type == IDENT
            and self.pos + 1 < len(self.tokens)
            and self.tokens[self.pos + 1].value == "="
        ):
            var_node = Variable(self.consume(IDENT).value)
            self.consume(SYMBOL, "=")
            expr_node = self.parse_expression()
            self.consume(SYMBOL, ";")
            return Assign(var_node, expr_node)

        if token.type == IDENT and token.value == "while":
            self.consume(IDENT, "while")
            self.consume(SYMBOL, "(")
            cond = self.parse_expression()
            self.consume(SYMBOL, ")")
            body = self.parse_block()
            return WhileStmt(cond, body)

        if token.type == IDENT and token.value == "def":
            self.consume(IDENT, "def")
            name = self.consume(IDENT).value
            self.consume(SYMBOL, "(")
            params = []
            if not (
                self.peek() and self.peek().type == SYMBOL and self.peek().value == ")"
            ):
                while True:
                    params.append(self.consume(IDENT).value)
                    if self.peek() and self.peek().value == ",":
                        self.consume(SYMBOL, ",")
                    else:
                        break
            self.consume(SYMBOL, ")")
            body = self.parse_block()
            return FunctionDef(name, params, body)

        if token.type == SYMBOL and token.value == "{":
            return self.parse_block()

        expr = self.parse_expression()
        self.consume(SYMBOL, ";")
        return expr

    def parse_block(self):
        """Parses a block of statements enclosed in curly braces."""
        stmts: list = []
        self.consume(SYMBOL, "{")
        while self.peek() and not (
            self.peek().type == SYMBOL and self.peek().value == "}"
        ):
            statement = self.parse_statement()
            if statement:
                stmts.append(statement)
        self.consume(SYMBOL, "}")
        return stmts

    def parse_program(self):
        """Parses a complete program, which is a sequence of statements."""
        statements: list = []
        while self.peek():
            statements.append(self.parse_statement())
        return [stmt for stmt in statements if stmt is not None]


# This convenience function is now correct
def parse(input_str: str):
    """Parses the input string into an AST."""
    tokens = lex(input_str)
    parser = Parser(tokens)
    return parser.parse_program()
