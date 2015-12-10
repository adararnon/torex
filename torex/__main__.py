import sys
import os
import argparse
import fnmatch
import re
import logging
import traceback
from configparser import ConfigParser
import rarfile


# The logger
logger = logging.getLogger(__name__)

# Directories etc.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILENAME = os.path.join(SCRIPT_DIR, r'log.txt')
LOG_FORMAT = '%(asctime)s %(levelname)s %(name)s %(message)s'
DEFAULT_CONFIG_FILENAME = os.path.join(SCRIPT_DIR, 'config.ini')


class UnsupportedTorrentError(RuntimeError):
    """An exception thrown when the torrent is unsupported."""
    pass


class AbstractTorrent(object):
    """
    An abstract torrent.
    
    :param dest_dir: the destination root directory
    :type dest_dir: str
    :param name: the torrent's name
    :type name: str
    :param download_dir: the directory to which the torrent was downloaded
    :type download_dir: str
    """
    
    # Should be overridden by concrete torrent
    LABEL = None
    LABEL_DIR = None
    
    def __init__(self, dest_dir, name, download_dir):
        self.dest_dir = dest_dir
        self.name = name
        self.download_dir = download_dir
        
        self._rar_path = self._find_rar_file(self.download_dir)
        self._subdir = self._get_torrent_subdir(self.name)
        
        logger.debug('RAR path: %s', self._rar_path)
        logger.debug('Specific download_dir: %s', self._subdir)
    
    @property
    def full_dest_path(self):
        return os.path.join(self.dest_dir, self.LABEL_DIR, self._subdir)
    
    def extract(self):
        """Performs the actual extraction."""
        with rarfile.RarFile(self._rar_path) as rf:
            files_to_extract = self._get_files_to_extract(rf.namelist())
            
            logger.info('Extracting to: %s', self.full_dest_path)
            rf.extractall(self.full_dest_path, files_to_extract)
    
    @staticmethod
    def _find_rar_file(dir_path):
        """
        Finds the .rar file in a directory.
        """
        files = os.listdir(dir_path)
        rar_files = fnmatch.filter(files, '*.rar')
        
        if len(rar_files) == 0:
            raise UnsupportedTorrentError("Unsupported torrent: no RAR archives found")
        elif len(rar_files) > 1:
            raise UnsupportedTorrentError("Unsupported torrent: more than one RAR archive found")
        
        return os.path.join(dir_path, rar_files[0])
    
    @classmethod
    def _get_torrent_subdir(cls, name):
        """
        Get the torrent's specific directory name.
        For example, this should be the name of the movie or the TV series.
        """
        raise NotImplementedError("This method should be implemented for every torrent label")
    
    @classmethod
    def _get_files_to_extract(cls, name_list):
        return fnmatch.filter(name_list, '*.mkv')


class TvTorrent(AbstractTorrent):
    """A torrent of a TV series."""
    
    LABEL = 'TV'
    LABEL_DIR = 'TV Series'
    
    SERIES_NAME_REGEX = re.compile(r'(\w+(\.\w+)*)\.[Ss]\d\d?[Ee]\d\d?')
    
    @classmethod
    def _get_torrent_subdir(cls, name):
        match = cls.SERIES_NAME_REGEX.match(name)
        if match is None:
            raise UnsupportedTorrentError("Failed matching torrent name: %s" % (name,))
        return ' '.join(match.group(1).split('.'))


TORRENT_TYPES = {
    'TV': TvTorrent,
}


def setup_logging(**kwargs):
    """
    Setup logging.
    :param kwargs: Logging parameters
    :see: :mod:`logging`
    """
    logging.basicConfig(**kwargs)


def has_config_file(args):
    return args.config_file and os.path.isfile(args.config_file)


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    # Parse arguments
    parser = argparse.ArgumentParser(
        description="Extract a torrent to a central destination directory.\n"
                    "The torrent should be exactly one RAR archive (possibly split to multiple files).\n"
                    "Support for different types of torrents will be added in the future.\n"
                    "Default command-line options may be set using a configuration file,\n"
                    "in a \"Defaults\" section.")
    
    parser.add_argument('-c', '--config_file', metavar='CONFIG_FILE',
                        default=DEFAULT_CONFIG_FILENAME,
                        help="Configuration file.")
    
    args, remaining_argv = parser.parse_known_args(args)
    
    if has_config_file(args):
        config = ConfigParser()
        config.read(args.config_file)
        defaults = dict(config.items('Defaults'))
    else:
        defaults = {
            'destination_dir': '.',
        }
    
    parser.set_defaults(**defaults)
    
    parser.add_argument('torrent_name',
                        help="The torrent's name.")
    
    parser.add_argument('torrent_download_dir',
                        help="The torrent's download directory.")
    
    parser.add_argument('label', metavar='label',
                        choices=TORRENT_TYPES.keys(),
                        help="The torrent's label.")
    
    parser.add_argument('--destination_dir',
                        help="Destination directory.")
    
    parser.add_argument('--log_filename',
                        default=LOG_FILENAME,
                        help="Log file path.")
    
    parser.add_argument('--log_level',
                        default=logging.DEBUG,
                        help="Log level.")
    
    args = parser.parse_args(remaining_argv)
    
    # Initialize logging
    setup_logging(filename=args.log_filename, level=args.log_level, format=LOG_FORMAT)
    if has_config_file(args):
        logger.debug('Running WITH a config file')
    else:
        logger.debug('Running WITHOUT a config file')
    
    # Create a torrent instance and extract it
    # noinspection PyBroadException
    try:
        logger.info('Handling torrent: %s (%s), directory: %s',
                    args.torrent_name, args.label, args.torrent_download_dir)
        torrent = TORRENT_TYPES[args.label](args.destination_dir, args.torrent_name, args.torrent_download_dir)
        torrent.extract()
        logger.info('Done: %s', args.torrent_name)
    except Exception:
        traceback.print_exc()
        logger.exception('Exception occurred while handling torrent')
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
