"""Description: This script is step 04 in processing the 1872 to 1991 geographical data of IBGE and creates a list of
shapefiles in the top directory of the raw 1872 to 1991 DPAs and puts them in the geodatabases created in step 3.

Requirements:
setup_dirs_2x.py has to be in the same folder as this script.
"""

# NOTE: since this script uses arcpy, make sure that the Python interpreter is Python 2.x

import os
import setup_dirs_2x
import arcpy

# Preferences:
arcpy.env.overwriteOutput = True

# Load main directories and create them if they don't exist:
dir_dict = setup_dirs_2x.def_dirs()
setup_dirs_2x.create_dirs(directory_dict=dir_dict, report=True)

# Define raw data directory:
raw_data_dir = os.path.join(dir_dict['raw_data']['path'], 'IBGE')

# Define top source directory:
top_source_dir = os.path.join(raw_data_dir, "divisao_territorial_1872_1991")

# Define top destination directory:
top_destin_dir = os.path.join(dir_dict['gis_data']['path'], 'IBGE')

# Get list of destination gdbs:
arcpy.env.workspace = top_destin_dir
gdb_list = arcpy.ListWorkspaces(workspace_type='FileGDB')

# Loop over destination gdbs, look for shapefiles in the source directory that correspond to the gdb year, and
# add them to the gdb:
for gdb in gdb_list:
    year = os.path.basename(gdb).replace('.gdb', '')
    source_dir = os.path.join(top_source_dir, year)
    shp_list = [os.path.join(root, f) for root, dirs, files in os.walk(top=source_dir, topdown=True) for f in files if
                f.endswith('.shp')]

    try:
        arcpy.FeatureClassToGeodatabase_conversion(Input_Features=shp_list, Output_Geodatabase=gdb)
        print arcpy.GetMessages()
    except arcpy.ExecuteError:
        print arcpy.GetMessages()
        continue
