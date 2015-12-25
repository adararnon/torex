from torex.basetorrent import Torrent
from torex.utils.naming import get_series_title


class TvTorrent(Torrent):
    """A torrent of a TV series."""

    label = 'tv'
    extensions = ['.mkv']

    @classmethod
    def _get_common_title(cls, title):
        """
        Extracts the series' title.

        :param title: The torrent's title, e.g. 'Better.Call.Saul.S01E01.720p.HDTV.x264-KILLERS'
        """
        return get_series_title(title)
