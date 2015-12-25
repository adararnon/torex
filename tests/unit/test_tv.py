import pytest

from torex.exceptions import UnsupportedTorrentException
from torex.torrents.tv import TvTorrent


def test_common_title_simple():
    assert TvTorrent.get_common_title('Better.Call.Saul.S01E02.720p.HDTV.X264-DIMENSION') == 'Better Call Saul'


def test_common_title_wtf():
    with pytest.raises(UnsupportedTorrentException):
        TvTorrent.get_common_title('ABC')
