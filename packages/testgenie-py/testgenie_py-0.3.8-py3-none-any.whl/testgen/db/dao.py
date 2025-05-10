from abc import ABC, abstractmethod
from typing import List, Tuple, Any

from testgen.models.function import Function


class Dao(ABC):
    @abstractmethod
    def insert_test_suite(self, name: str) -> int:
        pass

    @abstractmethod
    def insert_source_file(self, path: str, lines_of_code: int, last_modified) -> int:
        pass

    @abstractmethod
    def insert_function(self, name: str, params, start_line: int, end_line: int, source_file_id: int) -> int:
        pass

    @abstractmethod
    def insert_test_case(self, test_case: Any, test_suite_id: int, function_id: int, test_method_type: int) -> int:
        pass

    @abstractmethod
    def insert_test_result(self, test_case_id: int, status: bool, error: str = None) -> int:
        pass

    @abstractmethod
    def insert_coverage_data(self, file_name: str, executed_lines: int, missed_lines: int,
                             branch_coverage: float, source_file_id: int, function_id: int = None) -> int:
        pass

    @abstractmethod
    def get_test_suites(self) -> List[Any]:
        pass

    @abstractmethod
    def get_test_cases_by_function(self, function_name: str) -> List[Any]:
        pass

    @abstractmethod
    def get_source_file_id_by_path(self, filepath: str) -> int:
        pass

    @abstractmethod
    def get_coverage_by_file(self, file_path: str) -> List[Any]:
        pass

    @abstractmethod
    def get_test_file_data(self, file_path: str) -> List[Any]:
        pass

    @abstractmethod
    def get_function_by_name_file_id_start(self, name: str, source_file_id: int, start_line: int)-> int:
        pass

    @abstractmethod
    def get_functions_by_file(self, filepath: str) -> List[Function]:
        pass

    @abstractmethod
    def get_test_suite_id_by_name(self, name: str) -> int:
        pass

    @abstractmethod
    def get_test_case_id_by_func_id_input_expected(self, function_id: int, inputs: str, expected: str) -> int:
        pass

