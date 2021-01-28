"""DESCRIPTION: This script is step 02 in the processing of IBGE geographical data. This script unzips the downloaded
GIS files from step 1.

Requirements:
setup_dirs.py has to be in the same folder as this script.
utility_ibge_unzipper.py has to be in the same folder as this script.
"""

import os
import setup_dirs
import utility_ibge_unzipper

# Preferences:
overwrite_stuff = True

# Load directories and create them if they don't exist:
dir_dict = setup_dirs.def_dirs()
setup_dirs.create_dirs(directory_dict=dir_dict, report=True)

# Define raw data directory:
raw_data_dir = os.path.join(dir_dict['raw_data']['path'], 'IBGE')

# Define top directory to search for zip files:
topdir = [os.path.join(raw_data_dir, path) for path in os.listdir(path=raw_data_dir)
          if path.find("1872") > -1 and path.find("1991") > -1][0]

# Unzip all zip files in top directory:
utility_ibge_unzipper.unzipper(topdir=topdir, children=True, overwrite=overwrite_stuff, flatten=False)
