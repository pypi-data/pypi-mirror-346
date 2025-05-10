class Function:
    def __init__(self, name: str, params, start_line: int, end_line: int, num_lines: int, source_file_id: int):
        self._name = name
        self._params = params
        self._start_line = start_line
        self._end_line = end_line
        self._num_lines = num_lines
        self._source_file_id = source_file_id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def params(self) -> str:
        return self._params

    @params.setter
    def params(self, value: str) -> None:
        self._params = value

    @property
    def start_line(self) -> int:
        return self._start_line

    @start_line.setter
    def start_line(self, value: int) -> None:
        self._start_line = value

    @property
    def end_line(self) -> int:
        return self._end_line

    @end_line.setter
    def end_line(self, value: int) -> None:
        self._end_line = value

    @property
    def num_lines(self) -> int:
        return self._num_lines

    @num_lines.setter
    def num_lines(self, value: int) -> None:
        self._num_lines = value

    @property
    def source_file_id(self) -> int:
        return self._source_file_id

    @source_file_id.setter
    def source_file_id(self, value: int) -> None:
        self._source_file_id = value