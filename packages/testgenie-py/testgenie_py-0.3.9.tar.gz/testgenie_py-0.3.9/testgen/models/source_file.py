class SourceFile:
    def __init__(self, path: str, lines_of_code: int, last_modified):
        self._path = path
        self._lines_of_code = lines_of_code
        self._last_modified = last_modified

    @property
    def path(self) -> str:
        return self._path

    @path.setter
    def path(self, value: str) -> None:
        self._path = value

    @property
    def lines_of_code(self) -> int:
        return self._lines_of_code

    @lines_of_code.setter
    def lines_of_code(self, value: int) -> None:
        self._lines_of_code = value

    @property
    def last_modified(self):
        return self._last_modified

    @last_modified.setter
    def last_modified(self, value) -> None:
        self._last_modified = value