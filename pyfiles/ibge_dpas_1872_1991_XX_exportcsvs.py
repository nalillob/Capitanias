"""Description: This script loops over feature classes in the geodatabases created in step 3 and exports all feature
classes as .csv files.

Requirements:
setup_dirs_2x.py has to be in the same folder as this script.
utility_ibge_csvexporter.py has to be in the same folder as this script.
"""

# NOTE: since this script uses arcpy, make sure that the Python interpreter is Python 2.x

import os
import arcpy
import setup_dirs_2x
import utility_ibge_csvexporter

# Preferences:
arcpy.env.overwriteOutput = False
overwrite_csvs = False

# Load main directories and create them if they don't exist:
dir_dict = setup_dirs_2x.def_dirs()
setup_dirs_2x.create_dirs(directory_dict=dir_dict, report=True)

# Destination path:
top_destin = os.path.join(dir_dict['csv_data']['path'], "IBGE")
if not os.path.exists(top_destin):
    os.mkdir(top_destin)

# Top source dir:
top_source = os.path.join(dir_dict['gis_data']['path'], "IBGE")

# GDB List:
arcpy.env.workspace = top_source
gdblist = arcpy.ListWorkspaces(wild_card="*.gdb", workspace_type='FileGDB')

# Loop over GDB List, exporting feature classes to csv:
for gdb in gdblist:
    arcpy.env.workspace = gdb
    year = os.path.basename(gdb).replace(".gdb", "")
    fc_list = arcpy.ListFeatureClasses()
    tbl_list = arcpy.ListTables()
    destin_path = os.path.join(top_destin, year)
    if not os.path.exists(destin_path):
        os.mkdir(destin_path)
    for fc in fc_list:
        utility_ibge_csvexporter.fc2csv(fc=fc, overwrite=overwrite_csvs, out_path=destin_path)
    for tbl in tbl_list:
        utility_ibge_csvexporter.fc2csv(fc=tbl, overwrite=overwrite_csvs, out_path=destin_path)
