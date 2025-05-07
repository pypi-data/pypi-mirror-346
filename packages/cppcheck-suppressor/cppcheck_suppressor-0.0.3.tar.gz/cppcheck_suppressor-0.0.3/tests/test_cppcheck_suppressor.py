import os
import pytest
from cppcheck_suppressor.suppressions import write_suppressions
from cppcheck_suppressor.results import (
    cppcheck_errors_to_suppressions,
    get_cppcheck_errors,
)


class TestLoadCppcheckOutputFile:
    def test_load_no_errors(self):
        errors = get_cppcheck_errors("tests/data/no_errors.xml")
        assert len(errors) == 0

    def test_load_one_errors(self):
        errors = get_cppcheck_errors("tests/data/one_error.xml")
        assert len(errors) == 1

    def test_load_two_errors(self):
        errors = get_cppcheck_errors("tests/data/two_errors.xml")
        assert len(errors) == 2

    @pytest.mark.xfail(strict=True)
    def test_load_malformed(self):
        get_cppcheck_errors("tests/data/malformed.xml")


class TestParsingSuppressions:
    def test_no_suppressions(self):
        errors = get_cppcheck_errors("tests/data/no_errors.xml")
        suppressions = cppcheck_errors_to_suppressions(errors)
        assert len(suppressions) == 0

    def test_one_suppressions(self):
        errors = get_cppcheck_errors("tests/data/one_error.xml")
        suppressions = cppcheck_errors_to_suppressions(errors)
        assert len(suppressions) == 1

    def test_three_suppressions(self):
        errors = get_cppcheck_errors("tests/data/two_errors.xml")
        suppressions = cppcheck_errors_to_suppressions(errors)
        assert len(suppressions) == 2


class TestSavingSuppressions:
    @pytest.fixture(scope="class", autouse=True)
    def setup(self):
        if not os.path.isdir("tests/output"):
            os.makedirs("tests/output")

    def test_no_suppressions(self):
        if os.path.exists("tests/output/no_errors.xml"):
            os.remove("tests/output/no_errors.xml")
        errors = get_cppcheck_errors("tests/data/no_errors.xml")
        suppressions = cppcheck_errors_to_suppressions(errors)
        write_suppressions(suppressions, "tests/output/no_errors.xml")
        assert os.path.isfile("tests/output/no_errors.xml")

    def test_one_suppressions(self):
        if os.path.exists("tests/output/one_suppression.xml"):
            os.remove("tests/output/one_suppression.xml")
        errors = get_cppcheck_errors("tests/data/one_error.xml")
        suppressions = cppcheck_errors_to_suppressions(errors)
        write_suppressions(suppressions, "tests/output/one_suppression.xml")
        assert os.path.isfile("tests/output/one_suppression.xml")

    def test_three_suppressions(self):
        if os.path.exists("tests/output/three_suppressions.xml"):
            os.remove("tests/output/three_suppressions.xml")
        errors = get_cppcheck_errors("tests/data/two_errors.xml")
        suppressions = cppcheck_errors_to_suppressions(errors)
        write_suppressions(suppressions, "tests/output/three_suppressions.xml")
        assert os.path.isfile("tests/output/three_suppressions.xml")
