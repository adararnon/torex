import os

from setuptools import setup

setup(
        name='torex',
        version='1.0.0',
        packages=['torex'],
        url='',
        license='',
        author='Adar',
        author_email='',
        description='',
        install_requires=['rarfile'],
        entry_points={
            'console_scripts': [
                'torex = torex.__main__:main'
            ]
        },
        data_files=[('torex', [os.path.join('torex', 'config.ini')])],
)
