#!/usr/bin/env python
import argparse
import logging
import os
import sys
import traceback

from torex.torrents import torrent_dict
from torex.torrents.tv import TvTorrent

logger = logging.getLogger(__name__)

# Version
__version__ = '0.1.0'

# Directories etc.
LOG_FILENAME = os.path.expanduser(os.path.join('~', '.torex', 'log.txt'))
LOG_FORMAT = '%(asctime)s %(levelname)s %(name)s %(message)s'


def existingfile(x):
    """argparse type that makes sure the file exists."""
    if not os.path.isfile(x):
        raise argparse.ArgumentTypeError("File does not exist: {0}".format(x))
    return x


def setup_logging(**kwargs):
    """
    Setup logging.
    :param kwargs: Logging parameters
    :see: :mod:`logging`
    """
    os.makedirs(os.path.dirname(kwargs['filename']), exist_ok=True)
    logging.basicConfig(**kwargs)


def create_parser():
    parser = argparse.ArgumentParser(
            description="Extracts a torrent, following a specific configuration.")

    parser.add_argument('config_path',
                        type=existingfile,
                        help="Configuration YAML file.")

    parser.add_argument('title',
                        help="The torrent's title.")

    parser.add_argument('download_dir',
                        help="The torrent's directory.")

    parser.add_argument('label', metavar='label',
                        choices=torrent_dict.keys(),
                        type=str.lower,  # Case-insensitive choices
                        help="The torrent's label.")

    parser.add_argument('--log_filename',
                        default=LOG_FILENAME,
                        help="Log file path.")

    parser.add_argument('--log_level',
                        default=logging.INFO,
                        help="Log level.")

    return parser


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    parser = create_parser()
    args = parser.parse_args(argv)

    # Initialize logging
    setup_logging(filename=args.log_filename, level=args.log_level, format=LOG_FORMAT)
    logger.debug('Started, destination dir: %s', args.destination_dir)

    # Create a torrent instance and extract it
    # noinspection PyBroadException
    try:
        logger.info('Handling torrent: %s (%s), directory: %s',
                    args.torrent_name, args.label, args.torrent_download_dir)
        torrent = torrent_dict[args.label](args)
        torrent.extract()
        logger.info('Done: %s', args.torrent_name)
    except Exception:
        traceback.print_exc()
        logger.exception('Exception occurred while handling torrent')

    return 0


if __name__ == '__main__':
    sys.exit(main())
