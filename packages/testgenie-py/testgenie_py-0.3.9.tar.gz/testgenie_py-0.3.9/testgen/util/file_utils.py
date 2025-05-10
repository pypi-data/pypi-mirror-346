import ast
import importlib.util
import os
from _ast import Module
from types import ModuleType

def find_project_root(start_dir: str) -> str | None:
    current_dir = start_dir
    
    # Walk up the directory tree
    while current_dir:
        # Check for common project root indicators
        if (os.path.exists(os.path.join(current_dir, 'setup.py')) or
            os.path.exists(os.path.join(current_dir, '.git')) or
            os.path.exists(os.path.join(current_dir, 'pyproject.toml'))):
            return current_dir
            
        if os.path.exists(os.path.join(current_dir, '__main__.py')):
            return current_dir
        
        # Check for 'testgen' directory which is your project name
        if os.path.basename(current_dir) == 'testgen':
            parent_dir = os.path.dirname(current_dir)
            return parent_dir
            
        parent_dir = os.path.dirname(current_dir)
        if parent_dir == current_dir:  # Reached the root
            break
        current_dir = parent_dir
    
    return None


def load_module(file_path: str) -> ModuleType:
    # Load a Python module from a file path.
    if file_path is None:
        raise ValueError("File path not set! Use set_file_path() to specify the path of the file")

    module_name = os.path.splitext(os.path.basename(file_path))[0]
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def get_filename(filepath: str) -> str:
    """Get filename from filepath."""
    return os.path.basename(filepath)


def load_and_parse_file_for_tree(file) -> Module:
    with open(file) as f:
        code = f.read()
    tree = ast.parse(code)
    return tree

def adjust_file_path_for_docker(file_path: str) -> str:
    """Adjust the file path to be valid inside the Docker container."""
    print(f"Docker - adjusting path: {file_path}")

    # If already absolute to /controller, return as-is
    if file_path.startswith("/controller/"):
        print(f"Docker - already adjusted: {file_path}")
        return file_path

    # If relative, make absolute
    adjusted_path = f"/controller/{file_path.lstrip('/')}"
    print(f"Docker - adjusted to: {adjusted_path}")
    return adjusted_path

def get_project_root_in_docker(script_path) -> str:
    # Try to find project root by looking for pyproject.toml or similar
    current_dir = os.path.dirname(os.path.abspath(script_path))
    while current_dir != '/':
        if os.path.exists(os.path.join(current_dir, 'pyproject.toml')) or \
           os.path.exists(os.path.join(current_dir, 'setup.py')):
            project_root = current_dir
            break
        current_dir = os.path.dirname(current_dir)
    else:
        # Fallback - use parent of script dir
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(script_path)))
    
    print(f"Project root directory: {project_root}")
    return project_root