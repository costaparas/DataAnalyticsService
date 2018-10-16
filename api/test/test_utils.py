import datetime
from resources.utils import release_date_to_datetime
import pytest
def test_parse_release_date():
    assert release_date_to_datetime("06 Oct 1978") == datetime.datetime(year=1978,month=10,day=6)
    assert release_date_to_datetime("31 Jan 2018") == datetime.datetime(year=2018,month=1,day=31)

if __name__ == '__main__':
    pytest.main(["test_utils.py"])
