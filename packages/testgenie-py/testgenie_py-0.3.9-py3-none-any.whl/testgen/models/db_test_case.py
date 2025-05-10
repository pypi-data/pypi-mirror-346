class DBTestCase:
    def __init__(self, expected_output, inputs, test_function: str, last_run_time, test_method_type: int, test_suite_id: int, function_id: int):
        self._expected_output = expected_output
        self._inputs = inputs
        self._test_function = test_function
        self._last_run_time = last_run_time
        self._test_method_type = test_method_type
        self._test_suite_id = test_suite_id
        self._function_id = function_id

    @property
    def expected_output(self):
        return self._expected_output

    @expected_output.setter
    def expected_output(self, value):
        self._expected_output = value

    @property
    def inputs(self):
        return self._inputs

    @inputs.setter
    def inputs(self, value):
        self._inputs = value

    @property
    def test_function(self) -> str:
        return self._test_function

    @test_function.setter
    def test_function(self, value: str) -> None:
        self._test_function = value

    @property
    def last_run_time(self):
        return self._last_run_time

    @last_run_time.setter
    def last_run_time(self, value) -> None:
        self._last_run_time = value

    @property
    def test_method_type(self) -> int:
        return self._test_method_type

    @test_method_type.setter
    def test_method_type(self, value: int) -> None:
        self._test_method_type = value

    @property
    def test_suite_id(self) -> int:
        return self._test_suite_id

    @test_suite_id.setter
    def test_suite_id(self, value: int) -> None:
        self._test_suite_id = value

    @property
    def function_id(self) -> int:
        return self._function_id

    @function_id.setter
    def function_id(self, value: int) -> None:
        self._function_id = value
