"""Description: This script is step 6 in the processing of the 1872-1991 IBGE geographical data. It intersects the
DPAs with the Capitania feature classes to create a third polygon feature class.

Requirements:
setup_dirs_2x.py has to be in the same folder as this script.
"""

# NOTE: since this script uses arcpy, make sure that the Python interpreter is Python 2.x

import os
import arcpy
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

for gdb in gdblist:
    arcpy.env.workspace = gdb
    year = os.path.basename(gdb).replace(".gdb", "")
    muni_fc = "T05_malha_municipal_{0}_GCS_WGS_1984".format(year)
    int_fc = os.path.join(gdb, "{0}_intcaps".format(muni_fc))
    cap_fc = [fc for fc in arcpy.ListFeatureClasses(wild_card="capitanias_*", feature_type="POLYGON")
              if fc.find("ext") == -1][0]

    try:
        arcpy.Intersect_analysis(in_features=[muni_fc, cap_fc], out_feature_class=int_fc)
        print arcpy.GetMessages()
    except arcpy.ExecuteError:
        print arcpy.GetMessages()
        continue
