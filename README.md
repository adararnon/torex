torex
=====

torex is an open source application for automatic torrent extraction.

Installation
------------

You can install through PyPi:

```bash
pip install torex
```

Or just download the sources (manually or clone from GitHub) and run:

```bash
python setup.py install
```

Running
-------

The command for running torex is just `torex`.

The command-line interface is:

```bash
torex <config_path> <torrent_path> <label>
```

Where:
* config_path: Configuration file path
* torrent_path: The path to the downloaded torrent
* label: The torrent's label (will be explained later on)

uTorrent Setup
--------------

The script is particularly easy to run from uTorrent. Under Preferences, go to Advanced -> Run Program.
Then, set the program to be run:

```bash
torex <config_path> "%D" "%L"
```

Finally, when you add a torrent that should be extracted, just make sure it is assigned the correct label in uTorrent.

Labels
------

Supported torrent labels:
* tv - A TV series torrent (Formatted like *Breaking Bad S01E01*)

Configuration
-------------

The configuration file is a YAML file, that tells `torex` where it should extract the torrents to.
You can take a look at `config_example.yaml` for an example of what a configuration file should look like.

Under the label, you can define a root `path` that the torrents will be extracted to.
Every torrent will be extracted to a subdirectory with the TV series' name.

You can define an array of `special` types, each containing two fields:
* title: A regex for matching a torrent's title
* path: The path that these torrents should be extracted to

The `special` configuration is particularly useful when you have a big drive that holds all your downloads,
but you want some specific torrents to be extracted somewhere else.

Torrent Types
-------------

Right now, the only supported torrents are torrents that are a single directory with a single `.rar`
file to be extracted.

Logs
----

`torex` writes logs to `~/.torex/logs.txt`
