import codecs
import os
import re

from setuptools import setup
# noinspection PyPep8Naming
from setuptools.command.test import test as TestCommand


here = os.path.abspath(os.path.dirname(__file__))


class PyTest(TestCommand):

    # noinspection PyAttributeOutsideInit
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        pytest.main(self.test_args)


def read(*parts):
    # intentionally *not* adding an encoding option to open, See:
    #   https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    return codecs.open(os.path.join(here, *parts), 'r').read()


def get_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


def get_long_description():
    return read('README.md')


setup(
        name='torex',
        version=get_version('torex', '__init__.py'),
        url='',
        license='GPL',
        author='Adar',
        author_email='',
        description='Torrent extraction automation',
        long_description=get_long_description(),
        packages=['torex'],
        data_files=[('torex', [os.path.join('torex', 'config.ini')])],
        entry_points={
            'console_scripts': [
                'torex = torex.__main__:main'
            ]
        },
        install_requires=['rarfile'],
        tests_require=['pytest'],
        cmdclass={'test': PyTest},
)
