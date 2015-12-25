"""Exceptions used in the package"""


class TorexException(Exception):
    """Base exception class."""
    pass


class UnsupportedTorrentException(TorexException):
    """Raised when the torrent is unsupported."""
    pass


class InvalidConfigurationException(TorexException):
    """Raised when the configuration file is invalid."""
    pass


class InvalidSeriesTitleException(TorexException):
    """Raised when a TV torrent has a name that could not be parsed into the series' title."""
    pass
