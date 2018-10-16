from datetime import datetime

import pytest

from resources.utils import release_date_to_datetime, release_date_and_year_strings_to_datetime


def test_parse_release_date_and_year_pair():
    assert release_date_and_year_strings_to_datetime("N/A", "1951") == datetime(year=1951, month=1, day=1)


def test_parse_release_date():
    assert release_date_to_datetime("06 Oct 1978") == datetime(year=1978, month=10, day=6)
    assert release_date_to_datetime("31 Jan 2018") == datetime(year=2018, month=1, day=31)


if __name__ == '__main__':
    pytest.main(["test_utils.py"])
