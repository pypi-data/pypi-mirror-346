import pytest
from unittest.mock import patch, MagicMock
import argparse
from report_of_monaco_2018.racing import RaceData
from report_of_monaco_2018.main import main
import sys
from io import StringIO
from contextlib import redirect_stderr


def test_main_with_file_and_asc_sort():
    """
    Test main function with --file and --asc arguments
    """
    with patch(
        "argparse.ArgumentParser.parse_args",
        return_value=argparse.Namespace(
            file="data.txt", driver=None, asc=True, desc=False
        ),
    ):
        with patch.object(RaceData, "print_report") as mock_print_report:
            main()

    mock_print_report.assert_called_once_with(
        file="data.txt", driver=None, sort_order="asc"
    )


def test_main_with_file_and_desc_sort():
    """
    Test main function with --file and --desc arguments
    """
    with patch(
        "argparse.ArgumentParser.parse_args",
        return_value=argparse.Namespace(
            file="data.txt", driver=None, asc=False, desc=True
        ),
    ):
        with patch.object(RaceData, "print_report") as mock_print_report:
            main()

    mock_print_report.assert_called_once_with(
        file="data.txt", driver=None, sort_order="desc"
    )


def test_main_with_driver_filter():
    """
    Test main function with --driver argument
    """
    with patch(
        "argparse.ArgumentParser.parse_args",
        return_value=argparse.Namespace(
            file="data.txt", driver="Lewis Hamilton", asc=False, desc=False
        ),
    ):
        with patch.object(RaceData, "print_report") as mock_print_report:
            main()

    mock_print_report.assert_called_once_with(file="data.txt", driver="Lewis Hamilton")


def test_main_file_not_found_exception():
    """
    Test main function when file not found
    """
    with patch(
        "argparse.ArgumentParser.parse_args",
        return_value=argparse.Namespace(
            file="nonexistent.txt", driver=None, asc=False, desc=False
        ),
    ):
        with patch.object(
            RaceData, "print_report", side_effect=FileNotFoundError("File not found")
        ):
            with pytest.raises(
                FileNotFoundError, match=r"\n\[ERROR\] File not found\n"
            ):
                main()


def test_main_value_error():
    """
    Test main function when ValueError occurs
    """
    with patch(
        "argparse.ArgumentParser.parse_args",
        return_value=argparse.Namespace(
            file="data.txt", driver=None, asc=False, desc=False
        ),
    ):
        with patch.object(
            RaceData, "print_report", side_effect=ValueError("Invalid data")
        ):
            with pytest.raises(ValueError, match=r"\n\[ERROR\] Invalid data\n"):
                main()


def test_main_default_sort_order():
    """
    Test main function with default sort order (asc when neither --asc nor --desc is specified)
    """
    with patch(
        "argparse.ArgumentParser.parse_args",
        return_value=argparse.Namespace(
            file="data.txt", driver=None, asc=False, desc=False
        ),
    ):
        with patch.object(RaceData, "print_report") as mock_print_report:
            main()

    mock_print_report.assert_called_once_with(
        file="data.txt", driver=None, sort_order="asc"
    )


def test_mutually_exclusive_group():
    """
    Test that --asc and --desc are mutually exclusive
    """

    test_args = ["--file", "data.txt", "--asc", "--desc"]
    with patch.object(sys, "argv", ["script.py"] + test_args):
        f = StringIO()
        with redirect_stderr(f):
            with pytest.raises(SystemExit):
                main()
        assert "argument --desc: not allowed with argument --asc" in f.getvalue()


def test_main_with_only_file_argument():
    """
    Test main function with only required --file argument
    """
    with patch(
        "argparse.ArgumentParser.parse_args",
        return_value=argparse.Namespace(
            file="data.txt", driver=None, asc=False, desc=False
        ),
    ):
        with patch.object(RaceData, "print_report") as mock_print_report:
            main()
