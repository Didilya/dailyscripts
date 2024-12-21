import ast
import astunparse
import os
from typing import Any, List, Dict, Tuple, Union


def infer_type(node: ast.AST) -> str:
    """
    Infer the type of a given AST node with more specificity.

    Args:
        node (ast.AST): The AST node.

    Returns:
        str: The inferred type as a string.
    """
    if isinstance(node, ast.Constant):
        if isinstance(node.value, int):
            return "int"
        elif isinstance(node.value, float):
            return "float"
        elif isinstance(node.value, str):
            return "str"
        elif isinstance(node.value, bool):
            return "bool"
        elif node.value is None:
            return "None"
    elif isinstance(node, ast.List):
        if node.elts:
            element_type = infer_type(node.elts[0])
            return f"List[{element_type}]"
        return "List[Any]"
    elif isinstance(node, ast.Dict):
        if node.keys and node.values:
            key_type = infer_type(node.keys[0])
            value_type = infer_type(node.values[0])
            return f"Dict[{key_type}, {value_type}]"
        return "Dict[Any, Any]"
    elif isinstance(node, ast.Tuple):
        if node.elts:
            element_types = ", ".join(infer_type(elt) for elt in node.elts)
            return f"Tuple[{element_types}]"
        return "Tuple[Any, ...]"
    elif isinstance(node, ast.Name):
        return node.id  # May be a variable name
    elif isinstance(node, ast.Call):
        return "Any"  # Calls cannot be inferred without context
    return "Any"


def infer_function_return_type(func: ast.FunctionDef) -> str:
    """
    Infer the return type of a function based on its return statements.

    Args:
        func (ast.FunctionDef): The function definition.

    Returns:
        str: The inferred return type as a string.
    """
    return_types = set()
    for node in ast.walk(func):
        if isinstance(node, ast.Return) and node.value:
            return_types.add(infer_type(node.value))
    if not return_types:
        return "None"
    if len(return_types) == 1:
        return return_types.pop()
    return f"Union[{', '.join(return_types)}]"  # Handle multiple return types


def add_type_hints_to_function(func: ast.FunctionDef) -> ast.FunctionDef:
    """
    Add type hints to a function based on its arguments and return type.

    Args:
        func (ast.FunctionDef): The function definition.

    Returns:
        ast.FunctionDef: The modified function definition with added type hints.
    """
    num_defaults = len(func.args.defaults)
    default_offset = len(func.args.args) - num_defaults

    for i, arg in enumerate(func.args.args):
        if arg.annotation is None:  # Only add if not already annotated
            if i >= default_offset:  # Argument has a default value
                default_value = func.args.defaults[i - default_offset]
                arg.annotation = ast.Name(id=infer_type(default_value), ctx=ast.Load())
            else:
                arg.annotation = ast.Name(id="Any", ctx=ast.Load())

    if func.returns is None:
        func.returns = ast.Name(id=infer_function_return_type(func), ctx=ast.Load())

    return func


def process_file(file_path: str) -> None:
    """
    Process a Python file and add type hints to its functions.

    Args:
        file_path (str): Path to the Python file.
    """
    if not os.path.isfile(file_path):
        print(f"Error: The file '{file_path}' does not exist.")
        return

    with open(file_path, "r") as file:
        source_code = file.read()

    tree = ast.parse(source_code)
    modified = False

    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            original_node = ast.dump(node)
            add_type_hints_to_function(node)
            if original_node != ast.dump(node):
                modified = True

    if modified:
        with open(file_path, "w") as file:
            file.write(astunparse.unparse(tree))
        print(f"Type hints added to '{file_path}'.")
    else:
        print(f"No changes made to '{file_path}'.")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Add type hints to a Python file.")
    parser.add_argument("file", help="Path to the Python file to process.")
    args = parser.parse_args()

    try:
        process_file(args.file)
    except Exception as e:
        print(f"An error occurred: {e}")
