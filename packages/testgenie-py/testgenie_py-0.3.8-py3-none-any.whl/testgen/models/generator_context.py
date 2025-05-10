from types import ModuleType
from typing import List

from pyasn1_modules.rfc6031 import id_ct_KP_sKeyPackage

from testgen.models.test_case import TestCase


class GeneratorContext:
    def __init__(self, filepath: str, filename: str, class_name:str | None, module: ModuleType, output_path: str,
                 test_cases: List[TestCase], is_package: bool, package_name: str, import_path: str):
        self._filepath: str = filepath
        self._filename: str = filename
        self._class_name: str = class_name
        self._module: ModuleType = module
        self._output_path: str = output_path
        self._test_cases: List[TestCase] = test_cases
        self._is_package: bool = is_package
        self._package_name: str = package_name
        self._import_path: str = import_path

    @property
    def filepath(self) -> str:
        return self._filepath
    
    @filepath.setter
    def filepath(self, value: str) -> None:
        self._filepath = value
    
    @property
    def filename(self) -> str:
        return self._filename
    
    @filename.setter
    def filename(self, value: str) -> None:
        self._filename = value
    
    @property
    def class_name(self) -> str | None:
        return self._class_name
    
    @class_name.setter
    def class_name(self, value: str | None) -> None:
        self._class_name = value
    
    @property
    def module(self) -> ModuleType:
        return self._module
    
    @module.setter
    def module(self, value: ModuleType) -> None:
        self._module = value
    
    @property
    def output_path(self) -> str:
        return self._output_path
    
    @output_path.setter
    def output_path(self, value: str) -> None:
        self._output_path = value
    
    @property
    def test_cases(self) -> List[TestCase]:
        return self._test_cases
    
    @test_cases.setter
    def test_cases(self, value: List[TestCase]) -> None:
        self._test_cases = value

    @property
    def is_package(self) -> bool:
        return self._is_package

    @is_package.setter
    def is_package(self, value: bool) -> None:
        self._is_package = value

    @property
    def package_name(self) -> str:
        return self._package_name

    @package_name.setter
    def package_name(self, value: str) -> None:
        self._package_name = value

    @property
    def import_path(self) -> str:
        return self._import_path

    @import_path.setter
    def import_path(self, value: str) -> None:
        self._import_path = value

