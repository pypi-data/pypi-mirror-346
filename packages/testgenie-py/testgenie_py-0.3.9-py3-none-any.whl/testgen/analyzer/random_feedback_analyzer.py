import random
import time
import traceback
from typing import List, Dict, Set
import testgen.util.coverage_utils as coverage_utils
from testgen.analyzer.contracts.contract import Contract
from testgen.analyzer.contracts.no_exception_contract import NoExceptionContract
from testgen.analyzer.contracts.nonnull_contract import NonNullContract
from testgen.models.test_case import TestCase
from testgen.analyzer.test_case_analyzer import TestCaseAnalyzerStrategy
from abc import ABC

from testgen.models.function_metadata import FunctionMetadata


# Citation in which this method and algorithm were taken from:
# C. Pacheco, S. K. Lahiri, M. D. Ernst and T. Ball, "Feedback-Directed Random Test Generation," 29th International
# Conference on Software Engineering (ICSE'07), Minneapolis, MN, USA, 2007, pp. 75-84, doi: 10.1109/ICSE.2007.37.
# keywords: {System testing;Contracts;Object oriented modeling;Law;Legal factors;Open source software;Software
# testing;Feedback;Filters;Error correction codes},

class RandomFeedbackAnalyzer(TestCaseAnalyzerStrategy, ABC):
    def __init__(self, analysis_context=None):
        super().__init__(analysis_context)
        self.test_cases = []
        self.covered_lines: Dict[str, Set[int]] = {}
        self.covered_functions: Set[str] = set()

    def collect_test_cases(self, function_metadata: FunctionMetadata, time_limit: int = 5) -> List[TestCase]:
        self.test_cases = []
        start_time = time.time()
        
        while (time.time() - start_time) < time_limit:
            
            try:
                param_values = self.generate_random_inputs(function_metadata.params)
                func_name = function_metadata.function_name
                function = function_metadata.func
                
                param_names = function_metadata.params.keys()
                
                ordered_args = [param_values.get(name, None) for name in param_names]
                
                result = function(*ordered_args)
                test_case = TestCase(func_name, tuple(ordered_args), result)

                if not self.is_duplicate_test_case(test_case):
                    self.test_cases.append(test_case)
                
                    covered = self.covered(function_metadata)
                    if covered:
                        break
                else:
                    # Optionally log duplicate detection
                    self.logger.debug(f"Skipping duplicate test case: {func_name}{test_case.inputs}")
                            
            except Exception as e:
                print(f"Error testing {function_metadata.function_name}: {e}")

        return self.test_cases
    
    def is_duplicate_test_case(self, new_test_case: TestCase) -> bool:
        for existing_test_case in self.test_cases:
            if (existing_test_case.func_name == new_test_case.func_name and
                existing_test_case.inputs == new_test_case.inputs):
                return True
        return False

    def covered(self, func: FunctionMetadata) -> bool:
        if func.function_name not in self.covered_lines:
            self.covered_lines[func.function_name] = set()

        test_cases = [tc for tc in self.test_cases if tc.func_name == func.function_name]

        for test_case in test_cases:
            analysis = coverage_utils.get_coverage_analysis(self._analysis_context.filepath, func, test_case.inputs)
            covered = coverage_utils.get_list_of_covered_statements(analysis)
            self.covered_lines[func.function_name].update(covered)
            self.logger.debug(f"Covered lines for {func.function_name}: {self.covered_lines[func.function_name]}")


        executable_statements = set(coverage_utils.get_all_executable_statements(self._analysis_context.filepath, func, test_cases))
        self.logger.debug(f"Executable statements for {func.function_name}: {executable_statements}")

        return self.covered_lines[func.function_name] == executable_statements

    def execute_sequence(self, sequence, contracts: List[Contract]):
        """Execute a sequence and check contract violations"""
        func_name, args_dict = sequence

        try:
            # Use module from analysis context if available
            function_metadata = self.get_function_metadata(func_name)
            func = function_metadata.func
            param_names = function_metadata.params.keys()

            ordered_args = [args_dict.get(name, None) for name in param_names]

            # Check preconditions
            for contract in contracts:
                if not contract.check_preconditions(tuple(ordered_args)):
                    print(f"Preconditions failed for {func_name} with {tuple(ordered_args)}")
                    return None, True

            # Execute function with properly ordered arguments
            output = func(*ordered_args)
            exception = None

        except Exception as e:
            print(f"EXCEPTION IN RANDOM FEEDBACK: {e}")
            print(traceback.format_exc())
            output = None
            exception = e

        # Check postconditions
        for contract in contracts:
            if not contract.check_postconditions(tuple(ordered_args), output, exception):
                print(f"Postcondition failed for {func_name} with {tuple(ordered_args)}")
                return output, True

        return output, False

    def get_function_metadata(self, func_name: str) -> FunctionMetadata | None:
        for function_data in self._analysis_context.function_data:
            if function_data.function_name == func_name:
                return function_data
        return None

    # TODO: Currently only getting random vals of primitives, extend to sequences
    def random_seqs_and_vals(self, param_types, non_error_seqs=None):
        return self.generate_random_inputs(param_types)

    @staticmethod
    def generate_random_inputs(param_types):
        """Generate inputs for fuzzing based on parameter types."""
        inputs = {}
        for param, param_type in param_types.items():
            if param_type == "int":
                random_integer = random.randint(-500, 500)  # Wider range for better edge cases
                inputs[param] = random_integer
            elif param_type == "bool":
                random_choice = random.choice([True, False])
                inputs[param] = random_choice
            elif param_type == "float":
                random_float = random.uniform(-500.0, 500.0)  # Wider range for better edge cases
                inputs[param] = random_float
            elif param_type == "str":
                # Generate diverse strings instead of always "abc"
                string_type = random.choice([
                    "empty", "short", "medium", "long", "special", "numeric", "whitespace"
                ])
                
                if string_type == "empty":
                    inputs[param] = ""
                elif string_type == "short":
                    inputs[param] = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=random.randint(1, 3)))
                elif string_type == "medium":
                    inputs[param] = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', k=random.randint(4, 10)))
                elif string_type == "long":
                    inputs[param] = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=random.randint(11, 30)))
                elif string_type == "special":
                    inputs[param] = ''.join(random.choices('!@#$%^&*()_+-=[]{}|;:,./<>?', k=random.randint(1, 8)))
                elif string_type == "numeric":
                    inputs[param] = ''.join(random.choices('0123456789', k=random.randint(1, 10)))
                else:  # whitespace
                    inputs[param] = ' ' * random.randint(1, 5)
            else:
                # For unknown types, try a default value
                inputs[param] = None
                
        return inputs
    
    # Algorithm described in above article
    # Classes is the classes for which we want to generate sequences
    # Contracts express invariant properties that hold both at entry and exit from a call
        # Contract takes as input the current state of the system (runtime values created in the sequence so far, and any exception thrown by the last call), and returns satisfied or violated
        # Output is the runtime values and boolean flag violated
    # Filters determine which values of a sequence are extensible and should be used as inputs
    def generate_sequences(self, function_metadata: List[FunctionMetadata], classes=None, contracts: List[Contract] = None, filters=None, time_limit=20):
        contracts = [NonNullContract(), NoExceptionContract()]
        error_seqs = [] # execution violates a contract
        non_error_seqs = [] # execution does not violate a contract

        functions = self._analysis_context.function_data
        start_time = time.time()
        while(time.time() - start_time) >= time_limit:
            # Get random function
            func = random.choice(functions)
            param_types: dict = func.params
            vals: dict = self.random_seqs_and_vals(param_types)
            new_seq = (func.function_name, vals)
            if new_seq in error_seqs or new_seq in non_error_seqs:
                continue
            outs_violated: tuple = self.execute_sequence(new_seq, contracts)
            violated: bool = outs_violated[1]
            # Create tuple of sequence ((func name, args), output)
            new_seq_out = (new_seq, outs_violated[0])
            if violated:
                error_seqs.append(new_seq_out)
            else:
                # Question: Should I use the failed contract to be the assertion in unit test??
                non_error_seqs.append(new_seq_out)
        return error_seqs, non_error_seqs

    def generate_sequences_new(self, contracts: List[Contract] = None, filters=None, time_limit=20):
        contracts = [NonNullContract(), NoExceptionContract()]
        error_seqs = []  # execution violates a contract
        non_error_seqs = []  # execution does not violate a contract

        functions = self._analysis_context.function_data.copy()
        start_time = time.time()

        while (time.time() - start_time) < time_limit:
            # Get random function
            func = random.choice(functions)
            param_types: dict = func.params
            vals: dict = self.random_seqs_and_vals(param_types)
            new_seq = (func.function_name, vals)

            if new_seq in [seq[0] for seq in error_seqs] or new_seq in [seq[0] for seq in non_error_seqs]:
                continue

            outs_violated: tuple = self.execute_sequence(new_seq, contracts)
            violated: bool = outs_violated[1]

            # Create tuple of sequence ((func name, args), output)
            new_seq_out = (new_seq, outs_violated[0])

            if violated:
                error_seqs.append(new_seq_out)

            else:
                non_error_seqs.append(new_seq_out)

            test_case = TestCase(new_seq_out[0][0], tuple(new_seq_out[0][1].values()), new_seq_out[1])
            self.test_cases.append(test_case)
            fully_covered = self.covered(func)
            if fully_covered:
                print(f"Function {func.function_name} is fully covered")
                functions.remove(func)

            if not functions:
                self.test_cases.sort(key=lambda tc: tc.func_name)
                print("All functions covered")
                break

        self.test_cases.sort(key=lambda tc: tc.func_name)
        return error_seqs, non_error_seqs