import ast
import io
from typing import List, Tuple

import coverage

from testgen.models.function_metadata import FunctionMetadata
from testgen.service.logging_service import get_logger
import testgen.util.coverage_utils
import testgen.util.file_utils
from testgen.reinforcement.abstract_state import AbstractState
import testgen.util.randomizer as randomizer
from testgen.models.test_case import TestCase


class ReinforcementEnvironment:
    def __init__(self, filepath: str, function_data: FunctionMetadata, initial_test_cases: List[TestCase], state: AbstractState):
        self.filepath = filepath
        self.function_data = function_data
        self.initial_test_cases = initial_test_cases
        self.test_cases = initial_test_cases.copy()
        self.state = state
        self.cov = coverage.Coverage()
        self.logger = get_logger()

    # State represented by covered_statements, test_count
    def get_state(self) -> Tuple:
        return self.state.get_state()

    def step(self, action) -> Tuple[Tuple, float]:
        prev_coverage = self.state.get_state()[0]  # Get actual coverage before action
        prev_test_cases = self.state.get_state()[1]
        self.logger.debug(f"STEP: Previous coverage: {prev_coverage} before action: {action}")

        # Execute action
        if action == "add":
            self.test_cases.append(randomizer.new_random_test_case(self.filepath, self.function_data.class_name, self.function_data.func_def))
        elif action == "merge" and len(self.test_cases) > 1:
            self.test_cases.append(randomizer.combine_cases(self.function_data.module, self.test_cases))
        elif action == "remove" and len(self.test_cases) > 1:
            self.test_cases = randomizer.remove_case(self.test_cases)
        elif action == "z3":
            self.test_cases = randomizer.get_z3_test_cases(self.filepath, self.function_data.class_name, self.function_data.func_def, self.test_cases)
        else:
            raise ValueError("Invalid action")

        # Update state with new coverage
        new_coverage = self.state.get_state()[0]
        num_test_cases = self.state.get_state()[1]

        # Calculate reward
        coverage_delta = new_coverage - prev_coverage
        num_test_cases_delta = num_test_cases - prev_test_cases
        reward = self.get_reward(coverage_delta, num_test_cases_delta)

        print(f"Action: {action}, Previous coverage: {prev_coverage}, New coverage: {new_coverage}, Reward: {reward}")

        return self.get_state(), reward

    def reset(self) -> None:
        self.test_cases = self.initial_test_cases.copy()

    def render(self):
        pass

    def get_reward(self, coverage_delta, num_test_cases_delta) -> float:
        reward: float
        """
        Reward of 1.0 for increasing coverage
        No reward for no change
        Penalty of -1.0 for decreasing coverage
        """
        if coverage_delta > 0:
            reward = 1.0
        elif coverage_delta == 0:
            reward = 0.0
        else:
            reward = -1.0

        self.logger.debug(f"Coverage delta reward: {reward}")

        """
        If new test cases are added, subtract a small penalty
        If test cases are removed, add a small bonus
        If test cases are the same, no change
        """
        test_cases_factor = (num_test_cases_delta * -0.1)
        reward = reward + test_cases_factor
        self.logger.debug(f"Reward or penalty added to coverage delta reward: {test_cases_factor}")

        print(f"Final reward {reward}")
        return reward
        
        return sorted(executable_lines)
    
    def run_tests(self) -> float:
        """Run all tests and calculate coverage with branch awareness"""
        import os
        
        # Create a coverage object with branch tracking
        self.cov = coverage.Coverage(branch=True)
        self.cov.start()
        
        # Execute all test cases
        for test_case in self.test_cases:
            try:
                func = self.function_data.func
                _ = func(*test_case.inputs)
            except Exception as e:
                import traceback
                print(f"[ERROR]: {traceback.format_exc()}")
        
        self.cov.stop()
        
        # Get detailed coverage data including branches
        file_path = os.path.abspath(self.filepath)
        data = self.cov.get_data()
        
        # Extract function-specific coverage
        function_range = self._get_function_line_range()
        if function_range:
            start_line, end_line = function_range
            
            # Calculate function-specific coverage
            analysis = self.cov.analysis2(file_path)
            
            if len(analysis) >= 4:
                executable_in_func = [line for line in analysis[1] if start_line <= line <= end_line]
                missed_in_func = [line for line in analysis[3] if start_line <= line <= end_line]
                
                if executable_in_func:
                    func_coverage = (len(executable_in_func) - len(missed_in_func)) / len(executable_in_func) * 100
                    return func_coverage
        
        # Fall back to standard coverage calculation
        fake_file = io.StringIO()
        total_coverage = self.cov.report(file=fake_file)
        self.cov.save()
        return total_coverage

    def _get_function_line_range(self):
        """Get the line range of the current function"""
        import ast
        
        try:
            with open(self.filepath, 'r') as f:
                source = f.read()
            
            tree = ast.parse(source)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.name == self.function_data.function_name:
                    # Find the first line of the function
                    start_line = node.lineno
                    
                    # Find the last line by getting the maximum line number of any node in this function
                    max_line = start_line
                    for child in ast.walk(node):
                        if hasattr(child, 'lineno'):
                            max_line = max(max_line, child.lineno)
                    
                    return (start_line, max_line)
        except Exception as e:
            print(f"Error getting function range: {e}")
        
        return None
