from os import path
from setuptools import setup
from distutils.util import convert_path

main_ns = {}
ver_path = convert_path('afc/version.py')
with open(ver_path) as ver_file:
    exec(ver_file.read(), main_ns)

setup(
    name='AdBlockID Filters Compiler',
    version=main_ns['__version__'],
    description='A tool that compiles filters',
    long_description_content_type='text/x-rst',
    author='Realodix',
    url='https://github.com/realodix/AdBlockFilterTools',
    packages=['afc'],
    entry_points={
        'console_scripts': ['flrender=afc.renderer:main'],
    },
    include_package_data=True,
    license='GPLv3',
)
