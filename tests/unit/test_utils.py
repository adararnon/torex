import pytest

from torex.exceptions import InvalidSeriesTitleException
from torex.utils.naming import get_series_title, get_torrent_title


def test_series_title_simple():
    assert get_series_title('Better.Call.Saul.S01E02.720p.HDTV.X264-DIMENSION') == 'Better Call Saul'


def test_series_title_wtf():
    with pytest.raises(InvalidSeriesTitleException):
        get_series_title('ABC')


def test_torrent_title():
    assert get_torrent_title(r'C:\Torrents\Better.Call.Saul.S01E02.720p.HDTV.X264-DIMENSION') == \
           r'Better.Call.Saul.S01E02.720p.HDTV.X264-DIMENSION'
