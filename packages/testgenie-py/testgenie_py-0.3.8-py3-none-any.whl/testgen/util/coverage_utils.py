import ast
from typing import List, Any

import coverage

from testgen.models.analysis_context import AnalysisContext
from testgen.models.function_metadata import FunctionMetadata
from testgen.models.test_case import TestCase
from testgen.util.file_utils import load_and_parse_file_for_tree, load_module
from testgen.util.utils import get_function_boundaries
from testgen.util.z3_utils.constraint_extractor import extract_branch_conditions


def get_coverage_analysis(filepath: str, function_metadata: FunctionMetadata, args) -> tuple:
    func_node = function_metadata.func_def
    func_start = func_node.lineno
    func_end = max([node.lineno for node in ast.walk(func_node) if hasattr(node, 'lineno')], default=func_start)

    func = function_metadata.func

    analysis_list = _get_coverage_analysis_list(func, filepath, args)

    analysis_list[1] = [line for line in analysis_list[1] if func_start <= line <= func_end]
    analysis_list[3] = [line for line in analysis_list[3] if func_start <= line <= func_end]

    branch_lines = _get_branch_lines(func_node)

    for line in branch_lines:
        if func_start <= line <= func_end and line not in analysis_list[1]:
            analysis_list[1].append(line)
    analysis_list[1].sort()

    if func_start not in analysis_list[1]:
        analysis_list[1].append(func_start)
        analysis_list[1].sort()

    if func_start in analysis_list[3]:
        analysis_list[3].remove(func_start)

    return tuple(analysis_list)


def _get_coverage_analysis_list(func: Any, filepath: str, args) -> list:
    cov = coverage.Coverage(branch=True)
    cov.start()

    func(*args)

    cov.stop()
    cov.save()

    analysis = cov.analysis2(filepath)
    analysis_list = list(analysis)
    return analysis_list

def _get_branch_lines(func_node: ast.FunctionDef) -> list:
    branch_lines = []
    for node in ast.walk(func_node):
        if isinstance(node, ast.If):
            branch_lines.append(node.lineno)
            if node.orelse:
                for else_item in node.orelse:
                    if hasattr(else_item, 'lineno'):
                        else_line = else_item.lineno - 1
                        branch_lines.append(else_line)
                        break
    return branch_lines

def get_list_of_covered_statements(analysis: tuple) -> list:
    return [x for x in analysis[1] if x not in analysis[3]]

def get_uncovered_lines_for_func(file_name: str, class_name: str | None, func_node: ast.FunctionDef, test_cases: List[TestCase]) -> List[int]:
    # Get normal uncovered lines
    func_name = func_node.name

    function_test_cases = [tc for tc in test_cases if tc.func_name == func_name]
    if not function_test_cases:
        print(f"Warning: No test cases found for function {func_name}.")
        return []

    module = load_module(file_name)
    if class_name is not None:
        class_obj = getattr(module, class_name)
        instance = class_obj()
        func = getattr(instance, func_name)
    else:
        func = getattr(module, func_name)

    # Run coverage
    cov = coverage.Coverage(branch=True)  # Enable branch coverage
    cov.start()
    for test_case in function_test_cases:
        if test_case.func_name == func_name:
            try:
                func(*test_case.inputs)
            except Exception as e:
                print(f"Warning: Test Case {test_case.inputs} failed with error: {e}")
    cov.stop()

    analysis = cov.analysis2(file_name)

    # Extract branch conditions from the function
    branch_conditions, _ = extract_branch_conditions(func_node)
    condition_line_numbers = [bc.line_number for bc in branch_conditions]

    # Check which branch condition lines weren't exercised
    func_start, func_end = get_function_boundaries(file_name, func_name)
    missed_lines = [line for line in analysis[3] if func_start <= line <= func_end]

    # Find branch conditions that need to be tested (those near missed lines)
    uncovered_branch_lines = []
    for line in condition_line_numbers:
        # Check if the condition itself or its following line (likely the branch body) is uncovered
        if line in missed_lines or (line + 1) in missed_lines:
            uncovered_branch_lines.append(line)

    return uncovered_branch_lines

def get_all_executable_statements(filepath: str, func: FunctionMetadata, test_cases):
    import ast
    from testgen.util.randomizer import new_random_test_case

    if not test_cases:
        temp_case = new_random_test_case(filepath, func.class_name, func.func_def)
        analysis = get_coverage_analysis(filepath, func, temp_case.inputs)
    else:
        analysis = get_coverage_analysis(filepath, func, test_cases[0].inputs)

    executable_lines = list(analysis[1])

    with open(filepath, 'r') as f:
        source = f.read()

    tree = ast.parse(source)

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == func.func_def.name:
            for if_node in ast.walk(node):
                if isinstance(if_node, ast.If) and if_node.orelse:
                    if isinstance(if_node.orelse[0], ast.If):
                        continue
                    else_line = if_node.orelse[0].lineno - 1

                    with open(filepath, 'r') as f:
                        lines = f.readlines()
                        if else_line <= len(lines):
                            line_content = lines[else_line - 1].strip()
                            if line_content == "else:":
                                if else_line not in executable_lines:
                                    executable_lines.append(else_line)

    return sorted(executable_lines)