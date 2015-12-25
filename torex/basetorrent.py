import abc
import fnmatch
import logging
import os
import re

import rarfile
import yaml

from torex.exceptions import UnsupportedTorrentException

logger = logging.getLogger(__name__)


class Torrent(object):
    """
    A base torrent.

    :param args: The script's arguments
    :type args: :class:`ArgumentParser` arguments
    """

    # Should be overridden by concrete torrents
    label = None  # Should be lowercase
    extensions = []  # List of supported extensions

    def __init__(self, args):
        self.config = self._read_config(args)
        self.title = args.title
        self.download_dir = args.download_dir
        self.dst = self._decide_dst(self.config[self.label], self.title)

        self._rar_path = self._find_rar_file(self.download_dir)

        logger.debug('Destination: %s', self.dst)
        logger.debug('RAR path: %s', self._rar_path)

    def extract(self):
        """Performs the actual extraction."""
        with rarfile.RarFile(self._rar_path) as rf:
            files_to_extract = self._get_files_to_extract(rf.namelist())

            logger.info('Extracting to: %s', self.dst)
            rf.extractall(self.dst, files_to_extract)

    @staticmethod
    def _find_rar_file(dir_path):
        """
        Finds the .rar file in a directory.
        """
        rar_files = fnmatch.filter(os.listdir(dir_path), '*.rar')

        if len(rar_files) == 0:
            raise UnsupportedTorrentException("Unsupported torrent: no RAR archives found")
        elif len(rar_files) > 1:
            raise UnsupportedTorrentException("Unsupported torrent: more than one RAR archive found")

        return os.path.join(dir_path, rar_files[0])

    # noinspection PyMethodParameters
    @abc.abstractclassmethod
    def get_common_title(cls, title):
        """
        Get the torrent's common title.
        For example, this should be the movie's or the series' title.

        :param title: The torrent's title
        """
        raise NotImplementedError("This method should be implemented for every torrent label")

    @classmethod
    def _get_files_to_extract(cls, name_list):
        return [x for x in name_list if os.path.splitext(x)[1] in cls.extensions]

    @classmethod
    def _read_config(cls, args):
        with open(args.config_path, 'r') as configf:
            return yaml.load(configf)

    @classmethod
    def _decide_dst(cls, label_config, title):
        dst = label_config['path']
        # If there are specific configurations, check if we match
        if 'specific' in label_config:
            for special in label_config['specific']:
                if re.compile(special['title']).match(title):
                    dst = special['path']

        return os.path.join(dst, cls.get_common_title(title))
