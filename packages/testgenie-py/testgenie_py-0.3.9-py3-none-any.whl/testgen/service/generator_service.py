import os
import inspect
from types import ModuleType
from typing import List

from testgen.models.test_case import TestCase
from testgen.generator.code_generator import CodeGenerator
from testgen.generator.doctest_generator import DocTestGenerator
from testgen.generator.pytest_generator import PyTestGenerator
from testgen.generator.unit_test_generator import UnitTestGenerator
from testgen.service.logging_service import get_logger
from testgen.tree.node import Node
from testgen.tree.tree_utils import build_binary_tree
from testgen.models.generator_context import GeneratorContext
from testgen.util.file_utils import find_project_root

# Constants for test formats
UNITTEST_FORMAT = 1
PYTEST_FORMAT = 2
DOCTEST_FORMAT = 3

class GeneratorService:
    def __init__(self, filepath: str, output_path: str, test_format: int = UNITTEST_FORMAT):
        self.filepath = filepath
        self.output_path = output_path
        self.test_format = test_format
        self.code_generator = CodeGenerator()
        self.test_generator = UnitTestGenerator(generator_context=None)
        self.generated_file_path = None
        self.logger = get_logger()

    def set_test_format(self, test_format: int):
        """Set the test generator format."""
        self.test_format = test_format
        if test_format == UNITTEST_FORMAT:
            self.logger.debug("SETTING TEST FORMAT TO UNITTEST")
            self.test_generator = UnitTestGenerator(generator_context=None)
        elif test_format == PYTEST_FORMAT:
            self.logger.debug("SETTING TEST FORMAT TO PYTEST")
            self.test_generator = PyTestGenerator(generator_context=None)
        elif test_format == DOCTEST_FORMAT:
            self.logger.debug("SETTING TEST FORMAT TO DOCTEST")
            self.test_generator = DocTestGenerator(generator_context=None)
        else:
            raise NotImplementedError(f"Test format {test_format} not implemented")

    def generate_test_file(self, module: ModuleType, class_name: str | None, test_cases: List[TestCase], output_path=None) -> str:
        """Generate a test file for the given test cases."""
        filename = self.get_filename(self.filepath)
        output_path = self.get_test_file_path(module.__name__, output_path)
        
        actual_class_name = self.resolve_class_name(module, class_name)
        
        context = self.get_generator_context(self.filepath, module, actual_class_name, test_cases, output_path)

        self.test_generator.generator_context = context
        
        self.test_generator.generate_test_header()

        self.generate_function_tests(test_cases)

        if self.test_format == DOCTEST_FORMAT:
            self.logger.debug("SAVING DOCT TEST FILE")
            self.test_generator.save_file()
            return self.filepath
        else:
            self.test_generator.save_file()
            return output_path

    def generate_function_tests(self, test_cases: List[TestCase]) -> None:
        """Generate test functions for the given test cases."""
        for i, test_case in enumerate(test_cases):
            unique_func_name = f"{test_case.func_name}_{i}"
            cases = [(test_case.inputs, test_case.expected)]
            self.test_generator.generate_test_function(unique_func_name, test_case.func_name, cases)

    def get_test_file_path(self, module_name: str, specified_path=None) -> str:
        """Determine the path for the generated test file."""
        if specified_path is not None:
            if os.path.exists(specified_path):
                if os.path.isdir(specified_path):
                    self.ensure_init_py(specified_path)
                    return os.path.join(specified_path, f"test_{module_name.lower()}.py")
                else:
                    print(f"Specified directory path: {specified_path} is not a directory.")
            else:
                print(f"Specified directory path: {specified_path} does not exist.")

        current_dir = os.getcwd()
        test_dir = os.path.join(current_dir, "tests")

        if os.path.exists(test_dir):
            if os.path.isdir(test_dir):
                self.ensure_init_py(test_dir)
                return os.path.join(test_dir, f"test_{module_name.lower()}.py")
            else:
                print(f"Test directory path: {test_dir} is not a directory.")
        else:
            print(f"Test directory path: {test_dir} does not exist, creating it.")
            os.mkdir(test_dir)
            self.ensure_init_py(test_dir)

        return os.path.join(test_dir, f"test_{module_name.lower()}.py")

    def ensure_init_py(self, directory: str):
        """Ensures that an __init__.py file exists in the given directory."""
        init_file = os.path.join(directory, "__init__.py")
        if not os.path.exists(init_file):
            with open(init_file, "w") as f:
                pass  # Create an empty __init__.py file
            print(f"Created __init__.py in {directory}")

    def generate_function_code(self, file_path: str, class_name: str | None, functions: list) -> str:
        """Generate function code for a given class and its functions."""
        trees = self.build_func_trees(functions)
        if class_name:
            print(class_name)
            self.generated_file_path = f"generated_{class_name.lower()}.py"
        else:
            print(self.get_filename(file_path))
            self.generated_file_path = f"generated_{self.get_filename(file_path)}"

        # Create the class file
        if class_name:
            file = self.code_generator.generate_class(class_name)
            file.close()
        else:
            file = open(self.generated_file_path, "w")
            file.close()

        # Append function implementations
        with open(self.generated_file_path, "a") as file:
            for func, root, params in trees:
                is_class_method = True if class_name else False
                
                # Get parameter types
                param_types = {}
                sig = inspect.signature(func)
                for param_name, param in sig.parameters.items():
                    if param_name != 'self':  # Skip self for class methods
                        # Extract type annotation if available
                        if param.annotation != inspect.Parameter.empty:
                            param_types[param_name] = param.annotation.__name__
                        else:
                            param_types[param_name] = 'object'  # Default to object if no annotation
                
                code = self.code_generator.generate_code_from_tree(
                    func.__name__, root, params, func, is_class_method, param_types
                )
                
                if class_name:
                    for line in code.split("\n"):
                        file.write(f"    {line}\n")
                else:
                    file.write(code)
                file.write("\n")

        return self.generated_file_path

    def get_generator_context(self, filepath: str, module: ModuleType, class_name: str | None, test_cases: List[TestCase], output_path: str) -> GeneratorContext:
        file_dir = os.path.dirname(os.path.abspath(filepath))
        is_package = os.path.exists(os.path.join(file_dir, '__init__.py'))

        package_name, import_path = self._resolve_package_name_and_import_path(filepath)

        generator_context = GeneratorContext(
            filepath=filepath,
            filename=self.get_filename(filepath),
            class_name=class_name,
            module=module,
            output_path=output_path,
            test_cases=test_cases,
            is_package=is_package,
            package_name=package_name,
            import_path=import_path
        )

        print(f"Generator Context: {generator_context.filepath} {generator_context.filename} {generator_context.class_name} {generator_context.is_package} {generator_context.package_name} {generator_context.import_path}")

        return generator_context

    @staticmethod
    def _resolve_package_name_and_import_path(filepath: str) -> tuple:
        if not os.path.exists(filepath) or not filepath.endswith('.py'):
            raise ValueError(f"Invalid Python file: {filepath}")

        # Get the directory and filename
        file_dir = os.path.dirname(os.path.abspath(filepath))
        module_name = os.path.splitext(os.path.basename(filepath))[0]

        # Find the project root by looking for setup.py or a .git directory
        project_root = find_project_root(file_dir)

        # Build the import path based on the file's location relative to the project root
        if project_root:
            rel_path = os.path.relpath(file_dir, project_root)
            if rel_path == '.':
                # File is directly in the project root
                import_path = module_name
                package_name = ''
            else:
                # File is in a subdirectory
                path_parts = rel_path.replace('\\', '/').split('/')
                # Filter out any empty parts
                path_parts = [part for part in path_parts if part]

                if path_parts:
                    package_name = path_parts[0]
                    # Construct the full import path
                    import_path = '.'.join(path_parts) + '.' + module_name
                else:
                    package_name = ''
                    import_path = module_name
        else:
            # Fallback if we can't find a project root
            package_name = ''
            import_path = module_name

        return package_name, import_path

    def build_func_trees(self, functions: list):
        """Build binary trees for function signatures."""
        tree_list = []
        for name, func in functions:
            signature = inspect.signature(func)
            params = [param for param, value in signature.parameters.items() if param != 'self']
            root = Node(None)
            build_binary_tree(root, 0, len(params))
            tree_list.append((func, root, params))
        return tree_list

    def resolve_class_name(self, module: ModuleType, class_name: str):
        # Determine the actual class name used in the module
        actual_class_name = class_name
        if 'generated_' in self.filepath and class_name:
            # For generated classes, find the actual class name in the module
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj):
                    actual_class_name = name
                    break
        return actual_class_name

    @staticmethod
    def get_filename(filepath: str) -> str:
        """Get filename from filepath."""
        return os.path.basename(filepath)