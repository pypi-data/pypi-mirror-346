import inspect
import json
import os
import re
import time
import subprocess

from types import ModuleType
from typing import Any, Dict, List

import testgen.util.file_utils as file_utils
import testgen.util.utils
from testgen.models.coverage_data import CoverageData
from testgen.models.function import Function

from testgen.models.test_case import TestCase
from testgen.service.analysis_service import AnalysisService
from testgen.service.generator_service import GeneratorService
from testgen.service.coverage_service import CoverageService
from testgen.service.db_service import DBService
from testgen.models.analysis_context import AnalysisContext
from testgen.service.logging_service import get_logger
from testgen.service.test_executor_service import TestExecutorService

# Constants for test strategies
AST_STRAT = 1
FUZZ_STRAT = 2
RANDOM_STRAT = 3
REINFORCE_STRAT = 4

# Constants for test formats
UNITTEST_FORMAT = 1
PYTEST_FORMAT = 2
DOCTEST_FORMAT = 3

class Service:
    def __init__(self):
        self.test_strategy: int = 0
        self.test_format: int = 0
        self.file_path = None
        self.generated_file_path = None
        self.class_name = None
        self.test_cases = []
        self.logger = get_logger()
        self.reinforcement_mode = "train"
        
        # Initialize specialized services
        self.analysis_service = AnalysisService()
        self.generator_service = GeneratorService(None, None, None)
        self.coverage_service = CoverageService()
        self.test_executor_service = TestExecutorService()
        self.coverage_service = CoverageService()
        # Only initialize DB service if not running in Docker
        if os.environ.get("RUNNING_IN_DOCKER") is None:
            self.db_service = DBService()
        else:
            # Create a dummy DB service that doesn't do anything
            self.db_service = None

    def generate_test_cases(self) -> List[TestCase] | None:
        module = file_utils.load_module(self.file_path)
        class_name = self.analysis_service.get_class_name(module)

        if self.test_strategy == AST_STRAT:
            self.generated_file_path = self.generate_function_code()
            Service.wait_for_file(self.generated_file_path)
            self.analysis_service.set_file_path(self.generated_file_path)
            module = file_utils.load_module(self.generated_file_path)
            class_name = self.analysis_service.get_class_name(module)
            self.analysis_service.set_test_strategy(self.test_strategy, module.__name__, self.class_name)

        else:
            self.analysis_service.set_test_strategy(self.test_strategy, module.__name__, self.class_name)

        test_cases: List[TestCase] = []
        if self.test_strategy == REINFORCE_STRAT:
            test_cases = self.analysis_service.do_reinforcement_learning(self.file_path, class_name, self.reinforcement_mode)
        else:
            test_cases = self.analysis_service.generate_test_cases()

        if os.environ.get("RUNNING_IN_DOCKER") is not None:
            self.logger.debug(f"Serializing test cases {test_cases}")
            self.serialize_test_cases(test_cases)
            return None  # Exit early in analysis-only mode
        
        return test_cases

    def generate_tests(self, output_path=None):
        module = file_utils.load_module(self.file_path)
        class_name = self.analysis_service.get_class_name(module)

        test_cases = self.generate_test_cases()
        
        # Only process if we have test cases
        if test_cases is None:
            return None
            
        self.test_cases = test_cases

        # Only save to DB if not running in Docker
        if os.environ.get("RUNNING_IN_DOCKER") is None:
            file_path_to_use = self.generated_file_path if self.test_strategy == AST_STRAT else self.file_path
            # Don't save test to db foreign key constraint violation error
            """self.db_service.save_test_generation_data(
                file_path_to_use,
                test_cases,
                self.test_strategy,
                module,
                class_name
            )"""

        test_file = self.generate_test_file(test_cases, output_path, module, class_name)

        # Ensure the test file is ready
        Service.wait_for_file(test_file)
        return test_file

    def generate_test_file(self, test_cases: List[TestCase], output_path: str | None = None,
                           module: ModuleType | None = None, class_name: str | None = None) -> str:
        if module is None:
            module = file_utils.load_module(self.file_path)
            class_name = self.analysis_service.get_class_name(module)

        if self.test_strategy == AST_STRAT:
            self.generator_service = GeneratorService(self.generated_file_path, output_path, self.test_format)
            self.generator_service.set_test_format(self.test_format)
            module = file_utils.load_module(self.generated_file_path)
        else:
            # Create the correct instance of the generator service
            self.generator_service = GeneratorService(self.file_path, output_path, self.test_format)
            self.generator_service.set_test_format(self.test_format)

        test_file = self.generator_service.generate_test_file(
            module,
            class_name,
            test_cases,
            output_path
        )

        print(f"Generated test file: {test_file}")

        # Ensure the test file is ready
        Service.wait_for_file(test_file)
        return test_file

    def generate_function_code(self):
        """Generate function code for a given class or module."""
        module = file_utils.load_module(self.file_path)
        class_name = self.analysis_service.get_class_name(module)
        functions = self.inspect_class(class_name)
        return self.generator_service.generate_function_code(self.file_path, class_name, functions)

    def run_tests(self, test_file: str):
        # Run execute tests, would collect results but currently not saving them to db
        _ = self.test_executor_service.execute_tests(test_file, self.test_format)
        """
        if results is None:
            raise RuntimeError("No test results returned from the test executor service.")
        else:
            if self.db_service:
                self.test_executor_service.save_test_results(self.db_service, results, self.file_path, self.test_format)
        """

    def run_coverage(self, test_file: str):
        file_path_to_use = self.generated_file_path if self.test_strategy == AST_STRAT else self.file_path

        self.logger.debug(f"Running coverage on: {test_file}")
        coverage_data = self.coverage_service.run_coverage(test_file, file_path_to_use)

        if os.environ.get("RUNNING_IN_DOCKER") is not None or self.db_service is None:
            self.logger.debug("Skipping database operations - running in Docker or no DB service")
            return

        # Save test results and coverage data
        """self.coverage_service.save_coverage_data(
            db_service=self.db_service,
            coverage_data=coverage_data,
            file_path=file_path_to_use
        )"""

        self._print_coverage_summary(file_path_to_use, coverage_data)

    @staticmethod
    def _print_coverage_summary(file_path: str, coverage_data: CoverageData):
        print("\nCoverage Summary:")
        print(f"File: {file_path}")
        total_lines = coverage_data.missed_lines + coverage_data.executed_lines
        print(f"Total lines: {total_lines}")
        print(f"Executed lines: {coverage_data.executed_lines}")
        print(f"Missed lines: {coverage_data.missed_lines}")
        
        if total_lines > 0:
            percentage = (coverage_data.executed_lines / total_lines) * 100
            print(f"Coverage: {percentage:.2f}%")
        else:
            print("Coverage: N/A (no lines to cover)")

    def serialize_test_cases(self, test_cases):
        """Serialize input arguments ot JSON-compatible format"""
        print("##TEST_CASES_BEGIN##")
        serialized = []
        for tc in test_cases:
            case_data = {
                "func_name": tc.func_name,
                "inputs": self.serialize_value(tc.inputs),
                "expected": self.serialize_value(tc.expected)
            }
            serialized.append(case_data)
        print(json.dumps(serialized))
        print("##TEST_CASES_END##")

    def serialize_value(self, value):
        """Serialize a single value to a JSON-compatible format"""
        if value is None or isinstance(value, (bool, int, float, str)):
            return value
        elif isinstance(value, (list, tuple)):
            return [self.serialize_value(v) for v in value]
        else:
            return str(value)

    @staticmethod
    def parse_test_cases_from_logs(logs_output):
        """Extract and parse test cases from container logs"""
        pattern = r"##TEST_CASES_BEGIN##\n(.*?)\n##TEST_CASES_END##"
        match = re.search(pattern, logs_output, re.DOTALL)

        if not match:
            raise ValueError("Could not find test cases in the container logs")

        test_cases_json = match.group(1).strip()
        test_cases_data = json.loads(test_cases_json)

        test_cases: List[TestCase] = []
        for tc_data in test_cases_data:
            test_case = TestCase(
                func_name=tc_data["func_name"],
                inputs=tc_data["inputs"],
                expected=tc_data["expected"]
            )
            test_cases.append(test_case)

        return test_cases

    def set_file_path(self, path: str):
        """Set the file path for analysis and validate it."""
        print(f"Setting file path: {path}")
        if os.path.isfile(path) and path.endswith(".py"):
            self.file_path = path
            self.analysis_service.set_file_path(path)
        else:
            raise ValueError("Invalid file path! Please provide a valid Python file path.")

    def set_class_name(self, class_name: str):
        """Set the class name to analyze."""
        self.class_name = class_name

    def set_test_generator_format(self, test_format: int):
        """Set the test generator format."""
        self.test_format = test_format
        self.generator_service.set_test_format(test_format)

    def set_test_analysis_strategy(self, strategy: int):
        """Set the test analysis strategy."""
        self.test_strategy = strategy
        module = file_utils.load_module(self.file_path)
        self.analysis_service.set_test_strategy(strategy, module.__name__, self.class_name)
    
    def get_analysis_context(self, filepath: str) -> AnalysisContext:
        """Create an analysis context for the given file."""
        return self.analysis_service.create_analysis_context(filepath)

    @staticmethod
    def wait_for_file(file_path, retries=5, delay=1):
        """Wait for the generated file to appear."""
        while retries > 0 and not os.path.exists(file_path):
            time.sleep(delay)
            retries -= 1
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File '{file_path}' not found after waiting.")

    def find_package_root(self):
        """Find the package root directory."""
        current_dir = os.path.abspath(os.path.dirname(self.file_path))
        last_valid = None

        while current_dir:
            if "__init__.py" in os.listdir(current_dir):
                last_valid = current_dir
            else:
                break

            parent_dir = os.path.dirname(current_dir)
            if parent_dir == current_dir:
                break
            current_dir = parent_dir

        return last_valid

    def inspect_class(self, class_name):
        """Inspect a class or module and return its functions."""
        module = file_utils.load_module(self.file_path)

        # Handle module-level functions when class_name is None
        if not class_name:
            # Get module-level functions
            functions = inspect.getmembers(module, inspect.isfunction)
            return functions

        # Handle class functions
        cls = getattr(module, class_name, None)
        if cls is None:
            raise ValueError(f"Class '{class_name}' not found in module '{module.__name__}'.")

        functions = inspect.getmembers(cls, inspect.isfunction)
        return functions

    def resolve_module_path(self, module_name):
        """Resolve a module name to its file path by checking multiple locations."""
        direct_path = f"/controller/{module_name}.py"
        if os.path.exists(direct_path):
            self.logger.debug(f"Found module at {direct_path}")
            return direct_path

        testgen_path = f"/controller/testgen/{module_name}.py"
        if os.path.exists(testgen_path):
            self.logger.debug(f"Found module at {testgen_path}")
            return testgen_path

        if '.' in module_name:
            parts = module_name.split('.')
            potential_path = os.path.join('/controller', *parts) + '.py'
            if os.path.exists(potential_path):
                self.logger.debug(f"Found module at {potential_path}")
                return potential_path

        self.logger.debug(f"Could not find module: {module_name}")
        return None

    def visualize_test_coverage(self):
        from testgen.service.cfg_service import CFGService
        cfg_service = CFGService()
        cfg_service.initialize_visualizer(self)

        return cfg_service.visualize_test_coverage(
            file_path=self.file_path,
            test_cases=self.test_cases,
        )

    def set_reinforcement_mode(self, mode: str):
        self.reinforcement_mode = mode
        if hasattr(self ,'analysis_service'):
            self.analysis_service.set_reinforcement_mode(mode)

    def query_test_file_data(self, test_file_name: str):
        if self.db_service is None:
            raise RuntimeError("Database service is not initialized.")

        results = self.db_service.get_test_file_data(test_file_name)
        if not results:
            self.logger.debug(f"No data found for file: {test_file_name}")
            return

        from tabulate import tabulate
        rows = [dict(row) for row in results]

        print(f"Results for file: {test_file_name}")
        print(tabulate(rows, headers="keys", tablefmt="grid"))

    def get_all_functions(self, file_path: str):
        functions = testgen.util.utils.get_list_of_functions(file_path)
        for func in functions:
            print(f"Function: {func.name}")
            for attr, value in vars(func).items():
                if attr == "_source_file_id":
                    continue
                else:
                    print(f"  {attr}: {value}")
        return

    def select_all_from_db(self) -> None:
        rows = self.db_service.get_test_suites()
        for row in rows:
            print(repr(dict(row)))
