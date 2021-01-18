# NOTE: since this script uses arcpy, make sure that the Python interpreter is Python 2.x

import os
import arcpy
import csv

import setup_dirs_2x

# Preferences:
arcpy.env.overwriteOutput = True

# Load main directories and create them if they don't exist:
dir_dict = setup_dirs_2x.def_dirs()
setup_dirs_2x.create_dirs(directory_dict=dir_dict, report=True)

# Top dir:
top_dir = os.path.join(dir_dict['gis_data']['path'], "IBGE")

# GDB List:
arcpy.env.workspace = top_dir
gdblist = arcpy.ListWorkspaces(wild_card="*", workspace_type='FileGDB')

