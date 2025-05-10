import os
import sqlite3
import json
from typing import List, Tuple, Any
from datetime import datetime

from testgen.db.dao import Dao
from testgen.models.function import Function
from testgen.models.test_case import TestCase
from testgen.db.db import create_database

class DaoImpl(Dao):
    def __init__(self, db_name="testgen.db"):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self._connect()

    def _connect(self):
        if not os.path.exists(self.db_name):
            create_database(self.db_name)
        self.conn = sqlite3.connect(self.db_name)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self.cursor.execute("PRAGMA foreign_keys = ON;")

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None

    def insert_test_suite(self, name: str) -> int:
        self.cursor.execute(
            "INSERT INTO TestSuite (name, creation_date) VALUES (?, ?)",
            (name, datetime.now())
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def insert_source_file(self, path: str, lines_of_code: int, last_modified) -> int:
        self.cursor.execute("SELECT id FROM SourceFile WHERE path = ?", (path,))
        existing = self.cursor.fetchone()
        if existing:
            return existing[0]
        self.cursor.execute(
            "INSERT INTO SourceFile (path, lines_of_code, last_modified) VALUES (?, ?, ?)",
            (path, lines_of_code, last_modified)
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def insert_function(self, name: str, params, start_line: int, end_line: int, source_file_id: int) -> int:
        print(f"INSERTING FUNCTION: {name}, {params}, {start_line}, {end_line}, {source_file_id}")

        num_lines = end_line - start_line + 1
        self.cursor.execute(
            "SELECT id FROM Function WHERE name = ? AND source_file_id = ? AND params = ?",
            (name, source_file_id, params)
        )
        existing = self.cursor.fetchone()
        if existing:
            return existing[0]
        self.cursor.execute(
            "INSERT INTO Function (name, params, start_line, end_line, num_lines, source_file_id) VALUES (?, ?, ?, ?, ?, ?)",
            (name, params, start_line, end_line, num_lines, source_file_id)
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def insert_test_case(self, test_case: TestCase, test_suite_id: int, function_id: int, test_method_type: int) -> int:
        inputs_json = json.dumps(test_case.inputs, sort_keys=True)
        expected_json = json.dumps(test_case.expected, sort_keys=True)

        print(f"INSERTING TEST CASE: {test_case.func_name}, {test_case.inputs}, {test_case.expected}, {test_suite_id}, {function_id}, {test_method_type}")

        # Check for existing test case with same function_id, inputs, and expected_output
        self.cursor.execute(
            "SELECT id FROM TestCase WHERE function_id = ? AND input = ? AND expected_output = ?",
            (function_id, inputs_json, expected_json)
        )
        existing = self.cursor.fetchone()
        if existing:
            return existing[0]

        self.cursor.execute(
            "INSERT INTO TestCase (expected_output, input, test_function, last_run_time, test_method_type, test_suite_id, function_id) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                expected_json,
                inputs_json,
                test_case.func_name,
                datetime.now(),
                test_method_type,
                test_suite_id,
                function_id
            )
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def insert_test_result(self, test_case_id: int, status: bool, error: str = None) -> int:
        self.cursor.execute(
            "INSERT INTO TestResult (test_case_id, status, error, execution_time) VALUES (?, ?, ?, ?)",
            (test_case_id, status, error, datetime.now())
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def insert_coverage_data(self, file_name: str, executed_lines: int, missed_lines: int,
                             branch_coverage: float, source_file_id: int, function_id: int | None) -> int:
        coverage_type = "file" if function_id is None else "function"
        self.cursor.execute(
            "INSERT INTO CoverageData (coverage_type, executed_lines, missed_lines, branch_coverage, source_file_id, function_id) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (coverage_type, executed_lines, missed_lines, branch_coverage, source_file_id, function_id)
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def get_test_suites(self) -> List[Any]:
        self.cursor.execute("SELECT * FROM TestSuite ORDER BY creation_date DESC")
        return self.cursor.fetchall()

    def get_test_cases_by_function(self, function_name: str) -> List[Any]:
        self.cursor.execute(
            "SELECT tc.* FROM TestCase tc JOIN Function f ON tc.function_id = f.id WHERE f.name = ?",
            (function_name,)
        )
        return self.cursor.fetchall()

    def get_coverage_by_file(self, file_path: str) -> List[Any]:
        self.cursor.execute(
            "SELECT cd.* FROM CoverageData cd JOIN SourceFile sf ON cd.source_file_id = sf.id WHERE sf.path = ?",
            (file_path,)
        )
        return self.cursor.fetchall()

    def get_test_file_data(self, file_path: str) -> List[Any]:
        query = """
            SELECT
                tc.id AS test_case_id,
                tc.name AS test_case_name,
                tc.test_function AS test_case_test_function,
                tc.test_method_type AS test_case_method_type,
                COALESCE(cd.missed_lines, 'None') AS coverage_data_missed_lines
            FROM SourceFile sf
            LEFT JOIN Function f ON sf.id = f.source_file_id
            LEFT JOIN TestCase tc ON f.id = tc.function_id
            LEFT JOIN TestResult tr ON tc.id = tr.test_case_id
            LEFT JOIN CoverageData cd ON sf.id = cd.source_file_id
            WHERE sf.path = ?;
        """
        self.cursor.execute(query, (file_path,))
        return self.cursor.fetchall()

    def get_function_by_name_file_id_start(self, name: str, source_file_id: int, start_line: int) -> int:
        print(f"GETTING FUNCTION ID FOR {name}, {source_file_id}, {start_line}")
        self.cursor.execute(
            """
            SELECT id FROM Function
            WHERE name = ? AND source_file_id = ? AND start_line = ?
            """,
            (name, source_file_id, start_line)
        )
        result = self.cursor.fetchone()
        return result["id"] if result else -1

    def get_functions_by_file(self, filepath: str) -> List[Function]:
        self.cursor.execute(
            """
            SELECT id, name, params, start_line, end_line, num_lines, source_file_id
            FROM Function
            WHERE source_file_id = (
                SELECT id FROM SourceFile WHERE path = ?
            )
            """,
            (filepath,)
        )
        rows = self.cursor.fetchall()
        return [
            Function(
                name=row["name"],
                params=row["params"],
                start_line=row["start_line"],
                end_line=row["end_line"],
                num_lines=row["num_lines"],
                source_file_id=row["source_file_id"]
            )
            for row in rows
        ]

    def get_test_suite_id_by_name(self, name: str) -> int:
        self.cursor.execute(
            """
            SELECT id FROM TestSuite
            WHERE name = ?
            """,
            (name,)
        )
        result = self.cursor.fetchone()
        return result["id"] if result else -1

    def get_source_file_id_by_path(self, filepath: str) -> int:
        self.cursor.execute(
            """
            SELECT id FROM SourceFile
            WHERE path = ?
            """,
            (filepath,)
        )
        result = self.cursor.fetchone()
        return result["id"] if result else -1

    def get_test_case_id_by_func_id_input_expected(self, function_id: int, inputs: str, expected: str) -> int:
        self.cursor.execute(
            """
            SELECT id FROM TestCase
            WHERE function_id = ? 
            AND input = ? 
            AND expected_output = ?
            """,
            (function_id, inputs, expected)
        )
        result = self.cursor.fetchone()
        return result["id"] if result else -1