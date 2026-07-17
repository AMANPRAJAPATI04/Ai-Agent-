"""
Calculator Tool
---------------
Safely evaluates math expressions.
Uses Python's 'ast' module for safe parsing - never raw eval() (important
for security, otherwise arbitrary code could be executed).
"""

import ast
import operator
import math

TOOL_SCHEMA = {
    "name": "calculate",
    "description": "Calculates a math expression. Supports basic arithmetic (+, -, *, /, **, %) and functions (sqrt, sin, cos, log, etc.).",
    "input_schema": {
        "type": "object",
        "properties": {
            "expression": {
                "type": "string",
                "description": "The math expression, e.g. '25 * 4 + 10', 'sqrt(144)', '(15 + 5) / 2'"
            }
        },
        "required": ["expression"]
    }
}

ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
    ast.FloorDiv: operator.floordiv,
}

ALLOWED_FUNCTIONS = {
    "sqrt": math.sqrt,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "log": math.log,
    "log10": math.log10,
    "exp": math.exp,
    "factorial": math.factorial,
    "abs": abs,
    "round": round,
    "pi": math.pi,
    "e": math.e,
}


def _eval_node(node):
    if isinstance(node, ast.Constant):
        return node.value
    elif isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type not in ALLOWED_OPERATORS:
            raise ValueError(f"Operator not allowed: {op_type}")
        return ALLOWED_OPERATORS[op_type](_eval_node(node.left), _eval_node(node.right))
    elif isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type not in ALLOWED_OPERATORS:
            raise ValueError(f"Operator not allowed: {op_type}")
        return ALLOWED_OPERATORS[op_type](_eval_node(node.operand))
    elif isinstance(node, ast.Call):
        func_name = node.func.id
        if func_name not in ALLOWED_FUNCTIONS:
            raise ValueError(f"Function not allowed: {func_name}")
        args = [_eval_node(arg) for arg in node.args]
        return ALLOWED_FUNCTIONS[func_name](*args)
    elif isinstance(node, ast.Name):
        if node.id in ALLOWED_FUNCTIONS:
            return ALLOWED_FUNCTIONS[node.id]
        raise ValueError(f"Unknown name: {node.id}")
    else:
        raise ValueError(f"Expression type not allowed: {type(node)}")


def calculate(expression: str) -> str:
    try:
        tree = ast.parse(expression, mode="eval")
        result = _eval_node(tree.body)
        return f"{expression} = {result}"
    except ZeroDivisionError:
        return "Error: Cannot divide by zero."
    except Exception as e:
        return f"Error in calculation: {str(e)}"


if __name__ == "__main__":
    print(calculate("25 * 4 + sqrt(144)"))
