""" Konfigurasi
"""

config = {
    'libName'      : 'AdBlockID Filter Combiner',
    'libVersion'   : '1.0.0',
    'revisedTarget': './output/adblockid.txt'
}


# Store the version here so:
# 1) we don't load dependencies by storing it in __init__.py
# 2) we can import it in setup.py for the same reason
# 3) we can import it into module
__version__   = config['libVersion']
