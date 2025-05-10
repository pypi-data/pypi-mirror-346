class TestResult:
    def __init__(self, test_case_id: int, status: bool, error: str, execution_time):
        self._test_case_id = test_case_id
        self._status = status
        self._error = error
        self._execution_time = execution_time

    @property
    def test_case_id(self) -> int:
        return self._test_case_id

    @test_case_id.setter
    def test_case_id(self, value: int) -> None:
        self._test_case_id = value

    @property
    def status(self) -> bool:
        return self._status

    @status.setter
    def status(self, value: bool) -> None:
        self._status = value

    @property
    def error(self) -> str:
        return self._error

    @error.setter
    def error(self, value: str) -> None:
        self._error = value

    @property
    def execution_time(self):
        return self._execution_time

    @execution_time.setter
    def execution_time(self, value) -> None:
        self._execution_time = value