import sys
import os
# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# This allows us to import the REPL class from the repl module.
import pytest
from repl import REPL
import sys
from io import StringIO
import textwrap

@pytest.fixture
def repl_instance():
    """Provides a fresh REPL instance for each test."""
    return REPL()

def test_single_line_execution(monkeypatch, capsys, repl_instance):
    """Tests that a simple, single-line statement executes and prints."""
    # Simulate a user typing "10 + 5;" and then "quit"
    monkeypatch.setattr('sys.stdin', StringIO("10 + 5;\nquit\n"))
    repl_instance.run()
    captured = capsys.readouterr()
    # Check that the output contains the result
    assert "15" in captured.out

def test_variable_persistence(monkeypatch, capsys, repl_instance):
    """Tests that variables are remembered across multiple lines."""
    input_lines = textwrap.dedent("""
        sup x = 10;
        x * 2;
        quit
    """)
    monkeypatch.setattr('sys.stdin', StringIO(input_lines))
    repl_instance.run()
    captured = capsys.readouterr()
    # The first line should print nothing (it returns None).
    # The second line should print the result 20.
    assert "20" in captured.out

def test_multi_line_block_execution(monkeypatch, capsys, repl_instance):
    """Tests that the REPL correctly buffers and executes a multi-line block."""
    input_lines = textwrap.dedent("""
        sup x = 0;
        if (1 > 0) {
            x = 100;
        }
        x;
        quit
    """)
    # --- THE FIX IS HERE ---
    # We pass the multi-line string directly to StringIO.
    # No need for .replace(), which was causing the error.
    monkeypatch.setattr('sys.stdin', StringIO(input_lines))
    repl_instance.run()
    captured = capsys.readouterr()
    # The REPL should now correctly execute the block and print 100.
    assert "100" in captured.out

def test_file_execution_mode(tmp_path, repl_instance):
    """Tests running the interpreter in script/file mode by testing the run_program method."""
    # Create a temporary script file content
    script_content = textwrap.dedent("""
        # My test script
        sup a = 21;
        def double(n) { n * 2; }
        double(a);
    """)
    
    # The `if __name__ == '__main__'` block is hard to test directly.
    # A better unit test calls the core logic that block would use.
    # Here, we test the `run_program` method, which is the heart of file execution.
    result = repl_instance.run_program(script_content)
    
    # Assert that the final evaluated result is correct.
    assert result == 42