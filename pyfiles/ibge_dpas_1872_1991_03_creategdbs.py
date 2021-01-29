"""DESCRIPTION: This script is step 03 in the processing of IBGE geographical data. This script creates a geodatabase
for all years between 1872 and 1991 that have GIS data that has been downloaded in step 1.

Requirements:
setup_dirs_2x.py has to be in the same folder as this script.
"""

# NOTE: since this script uses arcpy, make sure that the Python interpreter is Python 2.x

import os
import setup_dirs_2x
import arcpy
import re

# Preferences:
arcpy.env.overwriteOutput = False

# Load main directories and create them if they don't exist:
dir_dict = setup_dirs_2x.def_dirs()
setup_dirs_2x.create_dirs(directory_dict=dir_dict, report=True)

# Define raw data directory:
raw_data_dir = os.path.join(dir_dict['raw_data']['path'], 'IBGE')

# Define top source directory:
top_source_dir = os.path.join(raw_data_dir, "divisao_territorial_1872_1991")

# Define gis destination directory and create it if it doesn't exist:
gis_data_dir = os.path.join(dir_dict['gis_data']['path'], 'IBGE')
if not os.path.exists(gis_data_dir):
    os.mkdir(gis_data_dir)

# Create a list of subdirectories of the source directories that match 4-digit year format between 1872 and 1991:
year_re = re.compile(r'^1[89]\d{2}$')
year_subdirs = [item for item in os.listdir(top_source_dir)
                if os.path.isdir(os.path.join(top_source_dir, item))
                and re.match(year_re, item)
                and 1872 <= int(item) <= 1991]

# Get list of existing geodatabases:
arcpy.env.workspace = gis_data_dir
existing_gdbs = arcpy.ListWorkspaces(workspace_type='FileGDB')

# Create list of geodatabases to create based on overwrite settings:
if arcpy.env.overwriteOutput:
    gdbs_to_create = [os.path.join(gis_data_dir, "{0}.gdb".format(year)) for year in year_subdirs]
else:
    gdbs_to_create = [os.path.join(gis_data_dir, "{0}.gdb".format(year)) for year in year_subdirs if
                      os.path.join(gis_data_dir, "{0}.gdb".format(year)) not in existing_gdbs]

# Loop over to-do list and create geodatabases:
if len(gdbs_to_create) > 0:
    for gdb in gdbs_to_create:
        try:
            arcpy.CreateFileGDB_management(out_folder_path=os.path.dirname(gdb),
                                           out_name=os.path.basename(gdb).replace(".gdb", ""))
            print arcpy.GetMessages()
        except arcpy.ExecuteError:
            print arcpy.GetMessages()
            continue
else:
    print 'There are no geodatabases to create.'
