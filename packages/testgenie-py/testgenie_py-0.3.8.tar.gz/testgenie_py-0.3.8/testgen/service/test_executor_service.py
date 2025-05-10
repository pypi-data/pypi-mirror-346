import doctest
import unittest
import subprocess
import sys
import os
from typing import Dict, List, Any

import pytest
from _pytest.reports import TestReport

from testgen.service.logging_service import get_logger
from testgen.util import utils
from testgen.service.db_service import DBService


class TestExecutorService:
    UNITTEST_FORMAT = 1
    PYTEST_FORMAT = 2
    DOCTEST_FORMAT = 3

    def __init__(self):
        self.logger = get_logger()

    def execute_tests(self, test_file: str, test_format: int) -> List[Dict[str, Any]]:

        test_file = os.path.abspath(test_file)
        if not os.path.exists(test_file):
            self.logger.error(f"Test file not found: {test_file}")
            return [{"name": f"{test_file}::file_not_found", "status": False, "error": "Test file not found"}]

        try:
            if test_format == self.UNITTEST_FORMAT:
                return self.execute_unittest(test_file)
            elif test_format == self.PYTEST_FORMAT:
                return self.execute_pytest(test_file)
            elif test_format == self.DOCTEST_FORMAT:
                return self.execute_doctest(test_file)
            else:
                self.logger.error(f"Unsupported test format: {test_format}")
                return [{"name": f"{test_file}::invalid_format", "status": False,
                         "error": f"Unsupported test format: {test_format}"}]

        except Exception as e:
            self.logger.error(f"Error executing tests: {str(e)}")
            return [{"name": f"{test_file}::execution_error", "status": False, "error": str(e)}]

    # Currently not collecting results
    def execute_unittest(self, test_file: str) -> List[Dict[str, Any]]:
        print(f"Running unittest on: {test_file}")
        result = subprocess.run(
            [sys.executable, "-m", "unittest", test_file],
            capture_output=True,
            text=True
        )
        print(result.stdout)
        print(result.stderr)
        # Would be used to return results
        return []

    def execute_pytest(self, test_file: str) -> List[Dict[str, Any]]:
        print(f"Executing pytest file: {test_file}")
        results = []

        try:
            # Custom plugin to collect results
            class PytestResultCollector:
                def __init__(self):
                    self.results = []

                def pytest_runtest_logreport(self, report: TestReport):
                    if report.when == "call":
                        self.results.append({
                            "name": report.nodeid,
                            "status": report.outcome == "passed",
                            "error": report.longreprtext if report.outcome != "passed" else None
                        })

            # Run pytest and collect results
            collector = PytestResultCollector()
            pytest.main([test_file], plugins=[collector])
            results = collector.results

        except Exception as e:
            self.logger.error(f"Error running pytest: {e}")
            results.append({
                "name": f"{test_file}::pytest_execution",
                "status": False,
                "error": str(e)
            })

        return results

    # Currently not collecting results
    def execute_doctest(self, test_file: str) -> List[Dict[str, Any]]:
        print(f"Running doctest on: {test_file}")
        #failed, attempted = doctest.testfile(test_file, module_relative=False, verbose=False)
        # doctest prints results by itself when verbose=True

        # Would be used to collect and return results
        return []

    # Currently not in use and not working to save the test results since I am having difficulty
    # getting the test case ID for each method and ran out of time :(
    def save_test_results(self, db_service: DBService, test_results: List[Dict[str, Any]],
                          file_path: str, test_format: int) -> None:
        if db_service is None:
            self.logger.debug("Skipping database operations - no DB service provided")
            return

        try:
            source_file_id = db_service.get_source_file_id_by_path(file_path)

            if source_file_id == -1:
                self.logger.error(f"Source file not found in database: {file_path}")
                return

            functions = db_service.get_functions_by_file(file_path)

            for result in test_results:
                name = result["name"]
                test_case = utils.parse_test_case_from_result_name(name, test_format)
                print(f"SAVE TEST RESULTS TEST CASE {test_case}")
                function_id = db_service.match_test_case_to_function_for_id(source_file_id, test_case, functions)
                print(f"SAVE TEST RESULTS FUNCTION ID {function_id}")

                if function_id == -1:
                    self.logger.warning(f"Could not match test case {name} to a function")
                    continue

                inputs_str = str(test_case.inputs)
                print(f"Inputs str {inputs_str}")
                expected_str = str(test_case.expected)
                print(f"Expected str {expected_str}")

                test_case_id = db_service.get_test_case_id_by_func_id_input_expected(
                    function_id, inputs_str, expected_str)

                if test_case_id == -1:
                    self.logger.warning(f"Test case not found in database: {name}")
                    continue

                db_service.insert_test_result(test_case_id, result["status"], result["error"])

        except Exception as e:
            self.logger.error(f"Error saving test results to database: {e}")