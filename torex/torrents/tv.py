import re

from torex.basetorrent import Torrent
from torex.exceptions import UnsupportedTorrentException


class TvTorrent(Torrent):
    """A torrent of a TV series."""

    label = 'tv'
    extensions = ['.mkv']

    series_title_regex = re.compile(r'(\w+(\.\w+)*)\.[Ss]\d\d?[Ee]\d\d?')

    @classmethod
    def get_common_title(cls, title):
        """
        Extracts the series' title.

        :param title: The torrent's title, e.g. 'Better.Call.Saul.S01E01.720p.HDTV.x264-KILLERS'
        """
        match = cls.series_title_regex.match(title)
        if match is None:
            raise UnsupportedTorrentException("Failed matching torrent name: %s" % (title,))
        return ' '.join(match.group(1).split('.'))
