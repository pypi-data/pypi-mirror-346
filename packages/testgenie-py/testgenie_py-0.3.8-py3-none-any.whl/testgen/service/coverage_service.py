import os
import subprocess
import time

from testgen.models.coverage_data import CoverageData
from testgen.service.logging_service import get_logger
from testgen.service.db_service import DBService

class CoverageService:
    UNITTEST_FORMAT = 1
    PYTEST_FORMAT = 2
    DOCTEST_FORMAT = 3

    def __init__(self):
        self.logger = get_logger()

    def run_coverage(self, test_file: str, source_file: str) -> CoverageData:
        #self.wait_for_file(test_file)
        self.logger.info(f"Running coverage on test file: {test_file}")
        self.logger.info(f"Source file to measure: {source_file}")

        try:
            cov_data = self.collect_coverage(test_file, source_file)
            return cov_data
        except Exception as e:
            self.logger.error(f"Error running coverage: {str(e)}")
            raise RuntimeError(f"Error running coverage subprocess: {e}")

    def collect_coverage(self, test_file: str, source_file: str) -> CoverageData:
        try:
            subprocess.run(["python", "-m", "coverage", "run", "--source=.", test_file], check=True)
            result = subprocess.run(
                ["python", "-m", "coverage", "report", source_file],
                check=True,
                capture_output=True,
                text=True
            )
            coverage_output = result.stdout
            subprocess.run(["python", "-m", "coverage", "json"], check=True)
            return self.parse_coverage_data(coverage_output, source_file)
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Error collecting coverage: {str(e)}")
            return CoverageData(
                coverage_type="file",
                executed_lines=0,
                missed_lines=0,
                branch_coverage=0.0,
                source_file_id=-1,
                function_id=None
            )

    def parse_coverage_data(self, coverage_output: str, file_path: str) -> CoverageData:
        lines = coverage_output.strip().split('\n')
        executed_lines = missed_lines = total_lines = 0
        branch_coverage = 0.0

        if lines:
            for line in lines:
                if file_path in line:
                    parts = line.split()
                    if len(parts) >= 4:
                        try:
                            total_lines = int(parts[-3])
                            missed_lines = int(parts[-2])
                            executed_lines = total_lines - missed_lines
                            coverage_str = parts[-1].strip('%')
                            branch_coverage = float(coverage_str) / 100
                            break
                        except (ValueError, IndexError) as e:
                            self.logger.error(f"Error parsing coverage data: {e}")

        # You may want to look up the source_file_id here if needed
        source_file_id = -1  # Set this appropriately in your context

        return CoverageData(
            coverage_type="file",
            executed_lines=executed_lines,
            missed_lines=missed_lines,
            branch_coverage=branch_coverage,
            source_file_id=source_file_id,
            function_id=None
        )

    # Save coverage data to database currently not working
    """"
    def save_coverage_data(self, db_service: DBService, coverage_data: CoverageData, file_path: str) -> None:
        if db_service is None:
            self.logger.debug("Skipping database operations - no DB service provided")
            return

        try:
            source_file_id = db_service.get_source_file_id_by_path(file_path)
            if source_file_id == -1:
                self.logger.error(f"Source file not found in database: {file_path}")
                return

            db_service.insert_coverage_data(
                file_name=file_path,
                executed_lines=coverage_data.executed_lines,
                missed_lines=coverage_data.missed_lines,
                branch_coverage=coverage_data.branch_coverage,
                source_file_id=source_file_id
            )
        except Exception as e:
            self.logger.error(f"Error saving coverage data to database: {e}")
    """

    @staticmethod
    def wait_for_file(file_path, retries=5, delay=1):
        """Wait for the generated file to appear."""
        while retries > 0 and not os.path.exists(file_path):
            time.sleep(delay)
            retries -= 1
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File '{file_path}' not found after waiting.")