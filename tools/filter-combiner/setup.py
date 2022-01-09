from os import path
from setuptools import setup
from distutils.util import convert_path

main_ns = {}
ver_path = convert_path('filter_combiner/config.py')
with open(ver_path) as ver_file:
    exec(ver_file.read(), main_ns)

setup(
    name='AdBlockID Filter Combiner',
    version=main_ns['__version__'],
    description='A library for combining ad blocker filter lists.',
    long_description_content_type='text/x-rst',
    author='Realodix',
    url='https://github.com/realodix/AdBlockFilterTools',
    packages=['filter_combiner'],
    entry_points={
        'console_scripts': ['flcombine=filter_combiner.combiner:main'],
    },
    include_package_data=True,
    license='GPLv3',
)
