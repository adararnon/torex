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
