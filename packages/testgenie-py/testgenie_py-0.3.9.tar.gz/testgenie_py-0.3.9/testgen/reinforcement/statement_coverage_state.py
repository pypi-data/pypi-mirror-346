from typing import Tuple

from testgen.service.logging_service import get_logger
import testgen.util.coverage_utils
from testgen.reinforcement.abstract_state import AbstractState
from testgen.util import utils

class StatementCoverageState(AbstractState):
    def __init__(self, environment):
        self.logger = get_logger()
        self.environment = environment

    def get_state(self) -> Tuple[float, int]:
        """Returns calculated coverage and length of test cases in a tuple"""
        all_covered_statements = set()
        for test_case in self.environment.test_cases:
            analysis = testgen.util.coverage_utils.get_coverage_analysis(self.environment.filepath, self.environment.function_data, test_case.inputs)
            covered = testgen.util.coverage_utils.get_list_of_covered_statements(analysis)
            all_covered_statements.update(covered)

        executable_statements = testgen.util.coverage_utils.get_all_executable_statements(self.environment.filepath, self.environment.function_data, self.environment.test_cases)

        if not executable_statements or executable_statements == 0:
            calc_coverage = 0.0
        else:
            calc_coverage: float = (len(all_covered_statements) / len(executable_statements)) * 100

        self.logger.debug(f"GET STATE ALL COVERED STATEMENTS: {all_covered_statements}")
        self.logger.debug(f"GET STATE ALL EXECUTABLE STATEMENTS: {executable_statements}")
        self.logger.debug(f"GET STATE FLOAT COVERAGE: {calc_coverage}")

        if calc_coverage >= 100:
            print(f"!!!!!!!!FULLY COVERED FUNCTION: {self.environment.function_data.function_name}!!!!!!!!")

        return calc_coverage, len(self.environment.test_cases)
            