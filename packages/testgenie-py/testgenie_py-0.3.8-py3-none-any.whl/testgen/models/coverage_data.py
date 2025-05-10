class CoverageData:
    def __init__(self, coverage_type: str, executed_lines: int, missed_lines: int, branch_coverage: float, source_file_id: int, function_id: int):
        self._coverage_type: str = coverage_type
        self._executed_lines: int = executed_lines
        self._missed_lines: int = missed_lines
        self._branch_coverage: float = branch_coverage
        self._source_file_id: int = source_file_id
        self._function_id: int = function_id

    @property
    def coverage_type(self) -> str:
        return self._coverage_type

    @coverage_type.setter
    def coverage_type(self, value: str) -> None:
        self._coverage_type = value

    @property
    def executed_lines(self) -> int:
        return self._executed_lines

    @executed_lines.setter
    def executed_lines(self, value: int) -> None:
        self._executed_lines = value

    @property
    def missed_lines(self) -> int:
        return self._missed_lines

    @missed_lines.setter
    def missed_lines(self, value: int) -> None:
        self._missed_lines = value

    @property
    def branch_coverage(self) -> float:
        return self._branch_coverage

    @branch_coverage.setter
    def branch_coverage(self, value: float) -> None:
        self._branch_coverage = value

    @property
    def source_file_id(self) -> int:
        return self._source_file_id

    @source_file_id.setter
    def source_file_id(self, value: int) -> None:
        self._source_file_id = value

    @property
    def function_id(self) -> int:
        return self._function_id

    @function_id.setter
    def function_id(self, value: int) -> None:
        self._function_id = value