"""cppcheck-suppressor initialization module"""

from os import path

__version__: str = "0.0.3"
schema_directory: str = path.join(
    path.dirname(path.abspath(__file__)), "data", "cppcheck.xsd"
)
