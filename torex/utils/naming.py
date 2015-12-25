"""Torrent naming utils"""
import os
import re

from torex.exceptions import InvalidSeriesTitleException

SERIES_TITLE_REGEX = re.compile(r'(\w+(\.\w+)*)\.[Ss]\d\d?[Ee]\d\d?')


def get_series_title(title):
    """
    Gets a series' title.

    :param title: The torrent's title, e.g. 'Better.Call.Saul.S01E01.720p.HDTV.x264-KILLERS'
    :return: The series' title
    """
    match = SERIES_TITLE_REGEX.match(title)
    if match is None:
        raise InvalidSeriesTitleException("Failed matching torrent name: {0}".format(title))
    return ' '.join(match.group(1).split('.'))


def get_torrent_title(torrent_path):
    """
    Gets a torrent's title from its path.
    Currently it is assumed that torrents are downloaded into a directory -
    torrents that are just single files are not supported.

    :param torrent_path: The torrent's path
    :return: The torrent's title
    """
    return os.path.split(torrent_path)[1]
