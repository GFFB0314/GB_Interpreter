import sys
from Interpreter.evaluator import Evaluator, Environment, NativeFunction
from Interpreter.parser import parse

PROMPT = ">>> "
CONTINUE_PROMPT = "... "


class REPL:
    """Read-Eval-Print-Loop."""

    # UPDATED: The __init__ method now creates the global environment
    def __init__(self, env=None):
        """Initialize the REPL with a global environment."""
        if env is None:

            def native_print(*args):
                """A native print function that handles strings and other types."""
                print(*(repr(arg) if isinstance(arg, str) else arg for arg in args))
                return None

            def native_input(prompt=""):
                """A native input function that handles user's input and EOF/KeyboardInterrupt."""
                try:
                    line = input(prompt)
                    # Manually check if the returned string is the Ctrl+D character.
                    if line == "\x04":
                        # If it is, we raise the EOFError ourselves so our
                        # main loops can catch it consistently.
                        raise EOFError
                    return line
                except EOFError:
                    # If the underlying input() raises the error, we need to
                    # re-raise it so it can be caught by the calling code.
                    raise

            global_env = Environment()
            global_env["print"] = NativeFunction("print", native_print)
            global_env["input"] = NativeFunction("input", native_input)
            self.evaluator = Evaluator(global_env)
        else:
            self.evaluator = Evaluator(env)

    def run_program(self, program_string: str):
        """Run a program string and return the last result."""
        ast_nodes = parse(program_string)
        last_result = None
        for node in ast_nodes:
            last_result = self.evaluator.eval(node)
        return last_result

    def run(self):
        """Run the REPL Loop."""
        buffer = ""
        brace_level = 0
        while True:
            try:
                current_prompt = CONTINUE_PROMPT if buffer else PROMPT
                line = input(current_prompt)

                if buffer == "" and line.strip() in ("exit", "quit"):
                    print("Goodbye!")
                    break

                buffer += line + "\n"
                brace_level += line.count("{")
                brace_level -= line.count("}")

                if brace_level <= 0:
                    try:
                        result = self.run_program(buffer)
                        if result is not None:
                            print(repr(result))
                    except Exception as e:
                        print(f"Error: {e}")
                    finally:
                        buffer = ""
                        brace_level = 0
            except (EOFError, KeyboardInterrupt):
                print("\nGoodbye!")
                break


if __name__ == "__main__":
    repl = REPL()
    if len(sys.argv) > 1:
        if not sys.argv[1].endswith(".gb"):
            sys.exit("Usage: python repl.py [filename].gb")
        filename = sys.argv[1]
        try:
            with open(filename, "r") as f:
                program_content = (
                    f.read()
                )  # Read the entire file content as a single string.
                final_result = repl.run_program(program_content)
                if final_result is not None:
                    print(repr(final_result))  # Print the final result of the program.
        except FileNotFoundError:
            print(f"Error: File not found '{filename}'")
        # Add a specific block to catch exit signals during script execution.
        except (KeyboardInterrupt, EOFError):
            print("\nProgram execution interrupted by user.")
            # sys.exit is used here because there's no loop to break out of.
            sys.exit(0)
        except Exception as e:
            print(f"Error running {filename}: {e}")
    else:
        print(
            "Simple Interpreter v1.4 (Interrupts fixed). Type 'quit' or 'exit' to leave."
        )
        repl.run()
