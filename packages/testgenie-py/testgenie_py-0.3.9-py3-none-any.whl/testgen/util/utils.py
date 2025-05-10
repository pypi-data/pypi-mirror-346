
import ast
import os
import string
import sys
import random
from typing import List

from atheris import FuzzedDataProvider

import testgen.util.file_utils
from testgen.models.function import Function
from testgen.models.test_case import TestCase
from testgen.util.file_utils import load_and_parse_file_for_tree

def extract_parameter_types(func_node):
    """Extract parameter types from a function node."""
    param_types = {}
    for arg in func_node.args.args:
        param_name = arg.arg
        if arg.annotation:
            param_type = ast.unparse(arg.annotation)
            param_types[param_name] = param_type
        else:
            if param_name != 'self':
                param_types[param_name] = None
    return param_types

def generate_random_inputs(param_types):
    """Generate inputs for fuzzing based on parameter types."""
    inputs = {}
    for param, param_type in param_types.items():
        if param_type == "int":
            # Try using sys.maxsize for minsize and maxsize
            minsize = -sys.maxsize - 1
            maxsize = sys.maxsize
            random_integer = random.randint(minsize, maxsize)
            inputs[param] = random_integer
        elif param_type == "bool":
            random_choice = random.choice([True, False])
            inputs[param] = random_choice
        elif param_type == "float":
            random_float = random.random()
            inputs[param] = random_float
        # TODO: Random String and Random bytes; Random objects?
        elif param_type == "str":
            inputs[param] = "abc"
        #elif param_type == "bytes":
        #    inputs[param] = fdp.ConsumeBytes(10)
        else:
            inputs[param] = None
    return inputs

def get_functions(tree) -> List[ast.FunctionDef]:
    functions = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            functions.append(node)
        if isinstance(node, ast.ClassDef):
            for class_node in node.body:
                if isinstance(class_node, ast.FunctionDef):
                    functions.append(class_node)
    return functions

def get_list_of_functions(filepath: str) -> List[Function]:
    tree = load_and_parse_file_for_tree(filepath)
    functions = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            params = extract_parameter_types(node)
            start_line = node.lineno
            end_line = max(
                [line.lineno for line in ast.walk(node) if hasattr(line, 'lineno') and line.lineno],
                default=start_line
            )
            num_lines = end_line - start_line + 1
            name = node.name
            source_file_id = -1  # Placeholder
            functions.append(Function(name, str(params), start_line, end_line, num_lines, source_file_id))
        if isinstance(node, ast.ClassDef):
            for method in node.body:
                if isinstance(method, ast.FunctionDef):
                    params = extract_parameter_types(method)
                    start_line = method.lineno
                    end_line = max(
                        [line.lineno for line in ast.walk(method) if hasattr(line, 'lineno') and line.lineno],
                        default=start_line
                    )
                    num_lines = end_line - start_line + 1

                    # Method name (prefixed with class name for clarity)
                    name = f"{node.name}.{method.name}"

                    # Source file ID will be set when adding to database
                    source_file_id = -1  # Placeholder

                    functions.append(Function(name, str(params), start_line, end_line, num_lines, source_file_id))
    return functions

def get_function_boundaries(file_name: str, func_name: str) -> tuple:
    tree = load_and_parse_file_for_tree(file_name)
    for i, node in enumerate(tree.body):
        if isinstance(node, ast.FunctionDef) and node.name == func_name:
            func_start = node.lineno

            if i == len(tree.body) - 1:
                max_lines = [line.lineno for line in ast.walk(node) if hasattr(line, 'lineno') and line.lineno]
                func_end = max(max_lines) if max_lines else func_start
            else:
                next_node = tree.body[i + 1]
                if hasattr(next_node, 'lineno'):
                    func_end = next_node.lineno - 1
                else:
                    max_lines = [line.lineno for line in ast.walk(node) if hasattr(line, 'lineno') and line.lineno]
                    func_end = max(max_lines) if max_lines else func_start

            return func_start, func_end
        
    # For classes
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            for i, method in enumerate(node.body):
                if isinstance(method, ast.FunctionDef) and method.name == func_name:
                    func_start = method.lineno
                    
                    # Find end of method
                    if i == len(node.body) - 1:
                        max_lines = [line.lineno for line in ast.walk(method) 
                                     if hasattr(line, 'lineno') and line.lineno]
                        func_end = max(max_lines) if max_lines else func_start
                    else:
                        next_method = node.body[i + 1]
                        if hasattr(next_method, 'lineno'):
                            func_end = next_method.lineno - 1
                        else:
                            max_lines = [line.lineno for line in ast.walk(method)
                                         if hasattr(line, 'lineno') and line.lineno]
                            func_end = max(max_lines) if max_lines else func_start
                    
                    return func_start, func_end
    
    raise ValueError(f"Function {func_name} not found in {file_name}")

def parse_test_case_from_result_name(name: str, format: int) -> TestCase:
    test_case = TestCase(None, (), None)
    if format == 3:
        test_case = parse_test_case_from_result_name_doctest(name)
    elif format == 2:
        test_case = parse_test_case_from_result_name_pytest(name, format)
    elif format == 1:
        test_case = parse_test_case_from_result_name_unittest(name, format)
    else:
        raise ValueError(f"Unsupported format: {format}")
    return test_case

def parse_test_case_from_result_name_pytest(name: str, format: int) -> TestCase:
    parts_name = name.split("::")
    test_filepath = parts_name[0]
    print(f"Parse test case from result name pytest: {test_filepath}")
    test_filepath = os.path.abspath(os.path.join(os.getcwd(), test_filepath))
    test_function_name = parts_name[1]

    if test_function_name.startswith("test_"):
        function_name_with_int = test_function_name[5:]
    else:
        function_name_with_int = test_function_name

    parts = function_name_with_int.rsplit('_', 1)
    if len(parts) > 1 and parts[1].isdigit():
        function_name = parts[0]
    else:
        function_name = function_name_with_int

    args, expected = extract_test_case_data(test_filepath, test_function_name, format)

    return TestCase(function_name, args, expected)

def parse_test_case_from_result_name_unittest(name: str, format: int) -> TestCase:
    parts_name = name.split("::")
    test_filepath = parts_name[0]
    test_function_name_with_mod = parts_name[1]
    test_function_name = test_function_name_with_mod.split('.')[1]

    args, expected = extract_test_case_data(test_filepath, test_function_name, format)

    parts = test_function_name.rsplit('_', 1)
    if len(parts) > 1 and parts[1].isdigit():
        function_name = parts[0]
    else:
        function_name = test_function_name

    return TestCase(function_name, args, expected)

# TODO: Find a way to associate doctest results to the actual test case
def parse_test_case_from_result_name_doctest(name: str) -> TestCase:
    function_name = name.split("::")[1]
    return TestCase(function_name, (), None)

def extract_test_case_data(test_file_path: str, function_name: str, test_format: int):
    if not os.path.exists(test_file_path):
        print(f"Error: Test file not found: {test_file_path}")
        return {}, None

    try:
        with open(test_file_path, 'r') as f:
            file_content = f.read()

        # For doctests, just return empty data since we can't easily extract it
        if test_format == 3:  # Doctest format
            return {}, None

        # Parse the file using ast
        tree = ast.parse(file_content)

        # Look for test function definition based on format
        if test_format == 1:  # Unittest
            return _extract_unittest_data(tree, function_name)
        elif test_format == 2:  # Pytest
            return _extract_pytest_data(tree, function_name)
        else:
            return None

    except Exception as e:
        print(f"Error extracting test case data: {e}")
        return None

def _extract_unittest_data(tree: ast.AST, function_name: str):
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            # Look for test method within the class
            for class_node in node.body:
                if isinstance(class_node, ast.FunctionDef) and class_node.name == f"test_{function_name}":
                    # Find 'args =' and 'expected =' assignments in the function body
                    args_value = None
                    expected_value = None

                    for stmt in class_node.body:
                        if isinstance(stmt, ast.Assign):
                            if isinstance(stmt.targets[0], ast.Name):
                                if stmt.targets[0].id == "args":
                                    args_value = _extract_value(stmt.value)
                                elif stmt.targets[0].id == "expected":
                                    expected_value = _extract_value(stmt.value)

                    if args_value is not None:
                        # Convert args to dict for consistency
                        if isinstance(args_value, tuple):
                            return args_value, expected_value
                        else:
                            return (args_value,), expected_value

    return None

def _extract_pytest_data(tree: ast.AST, function_name: str):
    """Extract args and expected output from pytest-style test file"""
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == f"test_{function_name}":
            # Find 'args =' and 'expected =' assignments in the function body
            args_value = None
            expected_value = None

            for stmt in node.body:
                if isinstance(stmt, ast.Assign):
                    if isinstance(stmt.targets[0], ast.Name):
                        if stmt.targets[0].id == "args":
                            args_value = _extract_value(stmt.value)
                        elif stmt.targets[0].id == "expected":
                            expected_value = _extract_value(stmt.value)

            if args_value is not None:
                # Convert args to dict for consistency
                if isinstance(args_value, tuple):
                    return args_value, expected_value
                else:
                    return (args_value,), expected_value

    return None

def _extract_value(node: ast.AST):
    """Convert an AST node to its Python value"""
    if isinstance(node, ast.Tuple):
        return tuple(_extract_value(elt) for elt in node.elts)
    elif isinstance(node, ast.List):
        return [_extract_value(elt) for elt in node.elts]
    elif isinstance(node, ast.Dict):
        return {_extract_value(key): _extract_value(value) for key, value in zip(node.keys, node.values)}
    elif isinstance(node, ast.Constant):
        return node.value


    # If we can't determine the value, try using ast.unparse (Python 3.9+)
    try:
        return eval(ast.unparse(node))
    except:
        try:
            # Fallback for older Python versions
            code = compile(ast.Expression(node), '<string>', 'eval')
            return eval(code)
        except:
            return None


