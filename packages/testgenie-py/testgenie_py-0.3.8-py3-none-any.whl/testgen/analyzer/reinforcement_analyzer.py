
import ast
from abc import ABC
import random
from typing import List

import testgen.util.randomizer
from testgen.models.function_metadata import FunctionMetadata
from testgen.models.test_case import TestCase
from testgen.analyzer.test_case_analyzer import TestCaseAnalyzerStrategy
from testgen.reinforcement.environment import ReinforcementEnvironment


# Goal: Learn a policy to generate a set of test cases with optimal code coverage, and minimum number of test cases
# Environment: FUT (Function Under Test)
# Agent: System
# Actions: Create new test case, combine test cases, delete test cases
# Rewards:

from typing import List, Optional
from testgen.models.test_case import TestCase
from testgen.models.analysis_context import AnalysisContext
from testgen.analyzer.test_case_analyzer import TestCaseAnalyzerStrategy
from testgen.reinforcement.agent import ReinforcementAgent
from testgen.reinforcement.environment import ReinforcementEnvironment
from testgen.reinforcement.statement_coverage_state import StatementCoverageState


class ReinforcementAnalyzer(TestCaseAnalyzerStrategy):
    def __init__(self, analysis_context: AnalysisContext, mode: str = "train"):
        super().__init__(analysis_context)
        self.analysis_context = analysis_context
        self.mode = mode

    def collect_test_cases(self, function_metadata: FunctionMetadata):
        # Implement or delegate as needed
        return self.analyze(function_metadata)

    def analyze(self, function_metadata: FunctionMetadata) -> List[TestCase]:
        from testgen.service.analysis_service import AnalysisService

        q_table = AnalysisService._load_q_table()
        function_test_cases: List[TestCase] = []


        environment = ReinforcementEnvironment(
            self.analysis_context.filepath,
            function_metadata,
            function_test_cases,
            state=StatementCoverageState(None)
        )
        environment.state = StatementCoverageState(environment)
        agent = ReinforcementAgent(
            self.analysis_context.filepath,
            environment,
            function_test_cases,
            q_table
        )
        episodes = 10 if self.mode == "train" else 1
        for _ in range(episodes):
            if self.mode == "train":
                new_test_cases = agent.do_q_learning()
            else:
                new_test_cases = agent.collect_test_cases()
            function_test_cases.extend(new_test_cases)

        seen = set()
        unique_test_cases = []
        for case in function_test_cases:
            case_inputs = tuple(case.inputs) if isinstance(case.inputs, list) else case.inputs
            case_key = (case.func_name, case_inputs)
            if case_key not in seen:
                seen.add(case_key)
                unique_test_cases.append(case)

        AnalysisService._save_q_table(q_table)
        return unique_test_cases