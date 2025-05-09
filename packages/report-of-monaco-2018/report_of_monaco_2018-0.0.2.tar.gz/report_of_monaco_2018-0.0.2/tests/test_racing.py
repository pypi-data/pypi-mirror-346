from datetime import datetime, timedelta
from io import StringIO
from pathlib import Path
from unittest.mock import Mock, patch, mock_open

import pytest


from report_of_monaco_2018.racing import RaceData


class TestRaceData:

    @pytest.fixture
    def race_instance(self):
        return RaceData()

    @pytest.mark.parametrize(
        "path, exception",
        [
            (("srb/", "nonexistent.txt"), FileNotFoundError),
            ((None, None), TypeError),
        ],
    )
    def test_read_file_errors(self, race_instance, path, exception):
        """Checking the function read_file to handle errors"""
        with pytest.raises(exception):
            folder, file = path
            race_instance.read_file(Path(folder), Path(file))

    @pytest.mark.parametrize(
        "path, content",
        [
            (("src/", "text.txt"), "Hello, World!"),
            (("src/", "ather.txt"), "KRF_Kimi Räikkönen_FERRARI"),
            (("src/", "text.txt"), "FAM2018-05-24_12:13:04.512"),
        ],
    )
    def test_read_file_return_result(self, race_instance, path, content):
        """Checking successful read file"""
        with patch("builtins.open", mock_open(read_data=content)) as mocked_open:
            folder, file = path
            full_path = Path(folder) / Path(file)
            result = race_instance.read_file(
                Path(folder) if folder is not None else None,
                Path(file) if file is not None else None,
            )
        assert result == content
        mocked_open.assert_called_once_with(full_path)

    @pytest.mark.parametrize(
        "data_start, expected_abbr, expected_start",
        [
            (
                "MES2018-05-24_12:05:58.778",
                "MES",
                datetime(2018, 5, 24, 12, 5, 58, 778000),
            ),
        ],
    )
    def test_create_race_instance_valid_data(
        self, data_start, expected_abbr, expected_start
    ):
        """Checking create RaceData instance with valid data"""
        race = RaceData.create_race_instance(data_start, start=True)
        assert race.abbreviation == expected_abbr
        assert race.start == expected_start
        assert race.end is None

    @pytest.mark.parametrize(
        "data",
        [
            "",
            "MAL",
            "123abc",
        ],
    )
    def test_create_race_instance_invalid_data_raises(self, data, race_instance):
        """Checking create RaceData instance with invalid data and raise errors"""
        with pytest.raises(ValueError):
            race_instance.create_race_instance(data, start=True)

    @patch.object(RaceData, "read_file")
    def test_create_race_list_basic(self, mock_read_file):
        """Checking to create raceData list"""
        mock_start_log = "DRR2018-05-24_12:00:00.000"
        mock_end_log = "DRR2018-05-24_12:01:00.000"

        mock_read_file.side_effect = [mock_start_log, mock_end_log]
        result = RaceData.create_race_list(
            folder=Path("/fake/path"),
            file_start=Path("start.log"),
            file_stop=Path("end.log"),
        )

        assert "DRR" in result
        race = result["DRR"]
        assert race.abbreviation == "DRR"
        assert race.start == datetime(2018, 5, 24, 12, 0, 0, 0)
        assert race.end == datetime(2018, 5, 24, 12, 1, 0, 0)
        assert race.duration == timedelta(minutes=1)
        assert race.recordErrors == []

    def test_sorted_asc_desc(self, race_instance):
        """Checking sorting function to sort RaceData dict by duration"""
        r1 = RaceData("Daniel Riccardo", "RED BULL RACING TAG HEUER", "DRR")
        r1.duration = timedelta(seconds=60)
        r2 = RaceData("Sebastian Vettel", "FERRARI", "SVF")
        r2.duration = timedelta(seconds=120)
        data = {"DRR": r1, "SVF": r2}

        sorted_asc = RaceData.sorted_asc_desc(data, "asc")
        assert list(sorted_asc.keys()), ["DRR", "SVF"]

        sorted_desc = RaceData.sorted_asc_desc(data, "desc")
        assert list(sorted_desc.keys()), ["SVF", "DRR"]

    @patch("report_of_monaco_2018.racing.RaceData.read_file")
    @patch("report_of_monaco_2018.racing.RaceData.create_race_list")
    def test_read_abbreviation(
        self, mock_create_race_list, mock_read_file, race_instance
    ):
        """Testing the read_abbreviation function"""
        mock_read_file.return_value = (
            "SVF_Sebastian Vettel_FERRARI\nLHM_Lewis Hamilton_MERCEDES"
        )
        mock_create_race_list.return_value = {
            "SVF": RaceData(
                abbreviation="SVF", driver="Sebastian Vettel", team="FERRARI"
            ),
            "LHM": RaceData(
                abbreviation="LHM", driver="Lewis Hamilton", team="MERCEDES"
            ),
        }

        record = race_instance.read_abbreviation(Path("data"))
        assert record["SVF"].abbreviation == "SVF"
        assert record["SVF"].driver == "Sebastian Vettel"
        assert record["SVF"].team == "FERRARI"

        assert record["LHM"].abbreviation == "LHM"
        assert record["LHM"].driver == "Lewis Hamilton"
        assert record["LHM"].team == "MERCEDES"

    @patch("report_of_monaco_2018.racing.RaceData.read_abbreviation")
    def test_build_report(self, mock_read_abbreviation, race_instance):
        """Testing build report function"""
        race_with_duration_none = RaceData(
            abbreviation="SVF",
            driver="Sebastian Vettel",
            team="FERRARI",
            start=datetime(2020, 5, 1, 12, 0, 0),
            end=None,
        )
        race_with_duration_none.duration = None

        race_with_duration = RaceData(
            abbreviation="LHM",
            driver="Lewis Hamilton",
            team="MERCEDES",
            start=datetime(2020, 1, 1, 12, 0, 0),
            end=datetime(2020, 1, 1, 12, 2, 0),
        )

        race_with_duration.duration = timedelta(minutes=2)

        mock_read_abbreviation.return_value = {
            "SVF": race_with_duration_none,
            "LHM": race_with_duration,
        }

        result, errors = race_instance.build_report(
            "some_folder", driver=None, sort_order="asc"
        )

        assert "LHM" in result
        assert result["LHM"].driver == "Lewis Hamilton"
        assert "SVF" in errors
        assert errors["SVF"].duration is None

    @patch("report_of_monaco_2018.racing.RaceData.build_report")
    def test_print_report_all(self, mock_build_report, race_instance):
        """Test print report for all instances if '--driver' didn't passed"""
        r1 = RaceData(driver="Sebastian Vettel", team="FERRARI", abbreviation="SVF")
        r1.duration = timedelta(minutes=1, seconds=30)

        r2 = RaceData(driver="Lewis Hamilton", team="MERCEDES", abbreviation="LHM")
        r2.duration = None
        r2.recordErrors = ["LHM duration is invalid"]

        mock_build_report.return_value = ({"SVF": r1}, {"LHM": r2})

        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            race_instance.print_report(file="folder", sort_order="asc")

        output = mock_stdout.getvalue()
        assert "1. Sebastian Vettel | FERRARI | 1" in output
        assert "This is lines with some error" in output
        assert "The driver Lewis Hamilton has some issues" in output

    @patch("report_of_monaco_2018.racing.RaceData.build_report")
    def test_print_report_driver(self, mock_build_report, race_instance):
        """Test print report if '--driver' have passed"""
        r1 = RaceData(driver="Max Verstappen", team="Red Bull", abbreviation="VER")
        r1.duration = timedelta(seconds=72)
        mock_build_report.return_value = {"VER": r1}

        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            race_instance.print_report(file="folder", driver="Max Verstappen")

        output = mock_stdout.getvalue()
        assert "Max Verstappen | Red Bull | 1" in output

    def test_duration_check_getter(self, race_instance):
        """Test property getter works"""
        assert race_instance.duration is None
        race_instance.duration = timedelta(2018, 5, 24, 12, 13)
        assert race_instance.duration == timedelta(2018, 5, 24, 12, 13)

    def test_duration_check_setter_successes(self, race_instance):
        """Test property setter works"""
        race_instance.duration = None
        assert race_instance.duration is None
        race_instance.duration = timedelta(2018, 5, 24, 12, 13)
        assert race_instance.duration == timedelta(2018, 5, 24, 12, 13)

    def test_duration_check_setter_errors(self, race_instance):
        """Test property setter works with negative value"""
        start_errors_len = len(race_instance.recordErrors)
        race_instance.abbreviation = "ABC"
        race_instance.duration = timedelta(days=-1)
        assert race_instance.duration is None
        assert len(race_instance.recordErrors) == start_errors_len + 1
        assert race_instance.abbreviation in race_instance.recordErrors[-1]
        assert "duration is negative" in race_instance.recordErrors[-1]
