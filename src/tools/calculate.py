import ast
import contextlib
import io
import traceback
from typing import Any

from langchain_core.tools import tool, ToolException

session = {}


def execute_code(code: str, exec_ns: dict) -> tuple[str, Any]:
    """
    Execute Python code and capture output.

    Returns:
        (output, return_value) - Last expression value if it's an expression, else None
    """
    stdout, stderr = io.StringIO(), io.StringIO()

    try:
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            # Parse and check if last line is an expression
            tree = ast.parse(code)
            last_is_expr = tree.body and isinstance(tree.body[-1], ast.Expr)

            # Wrap last expression to capture its value
            if last_is_expr:
                lines = code.rstrip().split("\n")
                code = "\n".join(lines[:-1] + [f"__result__ = {lines[-1]}"])

            # Execute code with single namespace for both globals and locals
            exec(code, exec_ns)

            # Extract return value
            return_value = exec_ns.get("__result__") if last_is_expr else None
            output = (stdout.getvalue() + stderr.getvalue()).strip()

            return output, return_value

    except Exception as e:
        raise ToolException(f"{type(e).__name__}: {e}\n{traceback.format_exc()}")


@tool
def bash_python(code: str) -> str:
    """Execute Python code in bash and return result"""

    output, return_value = execute_code(code, session)

    # Format result: prioritize return value over output
    if return_value is not None:
        result = str(return_value)
        if output:
            result = f"{output}\n{result}"
        return result

    return output