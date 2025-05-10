import os
from datetime import datetime
from types import ModuleType
from typing import List, Dict, Any
import testgen.util.utils as utils
from testgen.models.db_test_case import DBTestCase
from testgen.models.function import Function
from testgen.models.source_file import SourceFile
from testgen.models.test_case import TestCase

from testgen.db.dao_impl import DaoImpl

class DBService:
    def __init__(self, db_name="testgen.db"):
        self.dao = DaoImpl(db_name)

    def close(self):
        """Close the database connection."""
        self.dao.close()

    def insert_test_suite(self, name: str) -> int:
        return self.dao.insert_test_suite(name)

    def insert_source_file(self, path: str, lines_of_code: int, last_modified) -> int:
        return self.dao.insert_source_file(path, lines_of_code, last_modified)

    def insert_function(self, name: str, params, start_line: int, end_line: int, source_file_id: int) -> int:
        return self.dao.insert_function(name, params, start_line, end_line, source_file_id)

    def insert_test_case(self, test_case: TestCase, test_suite_id: int, function_id: int, test_method_type: int) -> int:
        return self.dao.insert_test_case(test_case, test_suite_id, function_id, test_method_type)

    def insert_test_result(self, test_case_id: int, status: bool, error: str = None) -> int:
        return self.dao.insert_test_result(test_case_id, status, error)

    # TODO: Add support for function_id
    def insert_coverage_data(self, file_name: str, executed_lines: int, missed_lines: int,
                             branch_coverage: float, source_file_id: int, function_id=None) -> int:
        return self.dao.insert_coverage_data(file_name, executed_lines, missed_lines, branch_coverage, source_file_id, function_id=None)

    def get_test_suites(self):
        return self.dao.get_test_suites()

    def get_source_file_id_by_path(self, filepath: str) -> int:
        return self.dao.get_source_file_id_by_path(filepath)

    def get_test_suite_id_by_name(self, name: str) -> int:
        return self.dao.get_test_suite_id_by_name(name)

    def get_functions_by_file(self, filepath: str) -> List[Function]:
        return self.dao.get_functions_by_file(filepath)

    def get_function_id_by_name_file_id_start(self, name: str, source_file_id: int, start_line: int) -> int:
        return self.dao.get_function_by_name_file_id_start(name, source_file_id, start_line)

    def get_test_cases_by_function(self, function_name):
        return self.dao.get_test_cases_by_function(function_name)

    def get_coverage_by_file(self, file_path):
        return self.dao.get_coverage_by_file(file_path)

    def get_test_file_data(self, file_path: str):
        return self.dao.get_test_file_data(file_path)

    def get_test_case_id_by_func_id_input_expected(self, function_id: int, inputs: str, expected: str) -> int:
        return self.dao.get_test_case_id_by_func_id_input_expected(function_id, inputs, expected)

    def save_test_generation_data(self, file_path: str, test_cases: list, test_strategy: int, module: ModuleType, class_name: str | None):
        """Save test generation data to the database."""
        source_file_data = self._get_source_file_data(file_path)
        source_file_id = self.insert_source_file(source_file_data.path, source_file_data.lines_of_code, source_file_data.last_modified)

        test_suite_name = class_name if class_name else module.__name__
        test_suite_id = self.insert_test_suite(test_suite_name)

        function_data = self._get_function_data(file_path)
        for function in function_data:
            self.insert_function(function.name, function.params, function.start_line, function.end_line, source_file_id)

        test_cases_data = self._get_test_cases_data(source_file_id, test_suite_id, function_data, test_cases, test_strategy)
        for test_case in test_cases_data:
            self.insert_test_case(TestCase(test_case.test_function, test_case.inputs, test_case.expected_output), test_case.test_suite_id, test_case.function_id, test_strategy)

    def _get_source_file_data(self, file_path: str) -> SourceFile:
        lines_of_code = sum(1 for _ in open(file_path, 'r')) # Count lines in file
        last_modified_time = os.path.getmtime(file_path)
        return SourceFile(file_path, lines_of_code, last_modified_time)

    def _get_function_data(self, file_path: str) -> List[Function]:
        return utils.get_list_of_functions(file_path)

    def _get_test_cases_data(self, source_file_id: int, test_suite_id: int, function_data: List[Function], test_cases: List[TestCase], test_strategy: int) -> List[DBTestCase]:
        db_test_cases = []
        for test_case in test_cases:
            function_id = self.match_test_case_to_function_for_id(source_file_id, test_case, function_data)
            db_test_case = DBTestCase(test_case.expected, test_case.inputs, test_case.func_name, datetime.now(), test_strategy, test_suite_id, function_id)
            db_test_cases.append(db_test_case)
        return db_test_cases

    def match_test_case_to_function_for_id(self, source_file_id: int, test_case: TestCase, functions: List[Function]) -> int:
        func_name = test_case.func_name
        if "." in func_name:
            func_name = func_name.split(".")[-1]

        candidate_functions = [f for f in functions if f.name.endswith(func_name)]

        if not candidate_functions:
            return -1

        if len(candidate_functions) == 1:
            return self.get_function_id_by_name_file_id_start(candidate_functions[0].name, source_file_id, candidate_functions[0].start_line)

        # Match by parameter count
        input_param_count = len(test_case.inputs) if isinstance(test_case.inputs, dict) else 1

        for function in candidate_functions:
            # Parse params from string representation to dict if needed
            params = function.params
            if isinstance(params, str):
                try:
                    params = eval(params)  # Convert string representation to dict
                except (SyntaxError, NameError):
                    continue

            param_count = len(params) if isinstance(params, dict) else 0

            if param_count == input_param_count:
                return self.get_function_id_by_name_file_id_start(function.name, source_file_id, function.start_line)

        return -1

    def _get_test_results(self, filepath: str, execution_results, test_format: int):
        source_file_id = self.get_source_file_id_by_path(filepath)
        functions = self.get_functions_by_file(filepath)
        for result in execution_results:
            name = result.name
            test_case = utils.parse_test_case_from_result_name(name, test_format)
            function_id = self.match_test_case_to_function_for_id(source_file_id, test_case, functions)
            test_case_id = self.get_test_case_id_by_func_id_input_expected(function_id, str(test_case.inputs), test_case.expected)
            self.insert_test_result(test_case_id, result.status, result.error)