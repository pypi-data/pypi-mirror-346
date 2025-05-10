class TestSuite:
    def __init__(self, name: str, creation_date):
        self._name = name
        self._creation_date = creation_date

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def creation_date(self):
        return self._creation_date

    @creation_date.setter
    def creation_date(self, value) -> None:
        self._creation_date = value