"""Tests for the pytest-xray-reporter plugin."""
import json
import pytest
from pathlib import Path
import sys


def test_success():
    """A test that should pass."""
    assert True


def test_failure():
    """A test that should fail."""
    assert False, "This test is expected to fail"


@pytest.mark.skip(reason="This test is skipped")
def test_skipped():
    """A test that should be skipped."""
    assert True


def test_with_output(capsys):
    """A test that produces output."""
    print("This is stdout")
    print("This is stderr", file=sys.stderr)
    assert True


def test_plugin_output(tmp_path):
    """Verify the plugin generates correct Xray JSON output."""
    output_file = tmp_path / "xray-results.json"
    
    # Run pytest with our plugin
    result = pytest.main([
        "-v",
        "--xray-output", str(output_file),
        __file__  # Plugin is loaded automatically
    ])
    
    # Read and verify the output
    with open(output_file) as f:
        results = json.load(f)
    
    # Check summary
    summary = results["info"]["summary"]
    assert summary["total"] == 4  # Total number of tests
    assert summary["passed"] == 2  # test_success and test_with_output
    assert summary["failed"] == 1  # test_failure
    assert summary["skipped"] == 1  # test_skipped
    
    # Check test results
    tests = results["tests"]
    assert len(tests) == 4
    
    # Verify test keys and statuses
    test_map = {t["testKey"]: t for t in tests}
    
    # Success test
    success_test = test_map["test_plugin.py::test_success"]
    assert success_test["status"] == "PASSED"
    
    # Failure test
    failure_test = test_map["test_plugin.py::test_failure"]
    assert failure_test["status"] == "FAILED"
    assert "This test is expected to fail" in failure_test["comment"]
    
    # Skipped test
    skipped_test = test_map["test_plugin.py::test_skipped"]
    assert skipped_test["status"] == "SKIPPED"
    
    # Output test
    output_test = test_map["test_plugin.py::test_with_output"]
    assert output_test["status"] == "PASSED"
    assert any(e["filename"] == "stdout.txt" for e in output_test["evidence"])
    assert any(e["filename"] == "stderr.txt" for e in output_test["evidence"]) 