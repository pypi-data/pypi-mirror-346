"""Pytest plugin for generating Xray JSON reports."""
import base64
import json
from datetime import datetime, timezone
from pathlib import Path
import platform

import pytest


class XrayReporter:
    """Pytest plugin that generates Xray JSON reports."""

    def __init__(self, config):
        self.config = config
        self.results = {
            "tests": [],
            "info": {
                "summary": {
                    "total": 0,
                    "passed": 0,
                    "failed": 0,
                    "errors": 0,
                    "skipped": 0,
                    "duration": 0.0
                },
                "testEnvironments": [],
                "project": None,
                "testPlanKey": None,
                "testExecutionKey": None
            }
        }
        self.start_time = datetime.now(timezone.utc)
        self._current_test = None

    def pytest_runtest_logstart(self, nodeid):
        """Record test start time."""
        self._current_test = {
            "testKey": nodeid,
            "start": datetime.now(timezone.utc).isoformat(),
            "evidence": [],
            "steps": [],
            "defects": [],
            "customFields": {}
        }

    def pytest_runtest_logreport(self, report):
        """Process test results and collect evidence."""
        if report.when == "call" or (report.when == "setup" and report.outcome == "skipped"):
            if not self._current_test:
                return
                
            # Get captured output
            evidence = []
            
            # Add stdout if present
            if report.capstdout:
                evidence.append({
                    "data": base64.b64encode(report.capstdout.encode()).decode(),
                    "filename": "stdout.txt",
                    "contentType": "text/plain"
                })
            
            # Add stderr if present
            if report.capstderr:
                evidence.append({
                    "data": base64.b64encode(report.capstderr.encode()).decode(),
                    "filename": "stderr.txt",
                    "contentType": "text/plain"
                })
            
            # Add stack trace for failures/errors
            if report.longrepr:
                evidence.append({
                    "data": base64.b64encode(str(report.longrepr).encode()).decode(),
                    "filename": "stacktrace.txt",
                    "contentType": "text/plain"
                })

            # Add captured log if available
            if hasattr(report, "caplog"):
                evidence.append({
                    "data": base64.b64encode(report.caplog.encode()).decode(),
                    "filename": "test.log",
                    "contentType": "text/plain"
                })

            # Calculate test duration
            finish_time = datetime.now(timezone.utc)
            duration = (finish_time - self.start_time).total_seconds()

            # Add test metadata
            if hasattr(report, "keywords"):
                for marker in report.keywords:
                    if marker.startswith("test_"):
                        continue
                    self._current_test["customFields"][marker] = str(report.keywords[marker])

            # Create test result in Xray format
            self._current_test.update({
                "finish": finish_time.isoformat(),
                "status": self._get_status(report.outcome),
                "comment": str(report.longrepr) if report.longrepr else "",
                "evidence": evidence,
                "duration": duration
            })

            self.results["tests"].append(self._current_test)
            
            # Update summary
            self.results["info"]["summary"]["total"] += 1
            if report.outcome == "passed":
                self.results["info"]["summary"]["passed"] += 1
            elif report.outcome == "failed":
                self.results["info"]["summary"]["failed"] += 1
            elif report.outcome == "error":
                self.results["info"]["summary"]["errors"] += 1
            elif report.outcome == "skipped":
                self.results["info"]["summary"]["skipped"] += 1
            
            # Update duration
            self.results["info"]["summary"]["duration"] += duration
            
            # Reset current test
            self._current_test = None

    def _get_status(self, outcome: str) -> str:
        """Convert pytest outcome to Xray status."""
        return {
            "passed": "PASSED",
            "failed": "FAILED",
            "error": "ERROR",
            "skipped": "SKIPPED"
        }.get(outcome, "UNKNOWN")

    def pytest_sessionfinish(self, session):
        """Write results to file when test session ends."""
        # Add test environment info
        self.results["info"]["testEnvironments"] = [
            platform.system(),
            platform.release(),
            platform.python_version()
        ]

        # Get optional info from config
        self.results["info"].update({
            "project": self.config.getoption("--xray-project", default=None),
            "testPlanKey": self.config.getoption("--xray-test-plan", default=None),
            "testExecutionKey": self.config.getoption("--xray-test-execution", default=None)
        })

        output_file = self.config.getoption("--xray-output")
        if output_file:
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "w") as f:
                json.dump(self.results, f, indent=2)


def pytest_addoption(parser):
    """Add command line options."""
    group = parser.getgroup("xray-reporter")
    group.addoption(
        "--xray-output",
        action="store",
        default="xray-results.json",
        help="Path to output Xray JSON report",
    )
    group.addoption(
        "--xray-project",
        action="store",
        help="Xray project key",
    )
    group.addoption(
        "--xray-test-plan",
        action="store",
        help="Xray Test Plan key",
    )
    group.addoption(
        "--xray-test-execution",
        action="store",
        help="Xray Test Execution key",
    )


def pytest_configure(config):
    """Register the plugin."""
    config.pluginmanager.register(XrayReporter(config)) 