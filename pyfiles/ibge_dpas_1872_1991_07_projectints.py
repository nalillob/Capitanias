"""Description: This script takes the intersected feature classes created in step 6 and projects them so that the
Shape_Length and Shape_Area fields are measured in meters and squared meters, respectively.

Requirements:
setup_dirs_2x.py has to be in the same folder as this script.
"""

# NOTE: since this script uses arcpy, make sure that the Python interpreter is Python 2.x

import os
import arcpy
import setup_dirs_2x

# Preferences:
arcpy.env.overwriteOutput = False

# Load main directories and create them if they don't exist:
dir_dict = setup_dirs_2x.def_dirs()
setup_dirs_2x.create_dirs(directory_dict=dir_dict, report=True)

# Top dir:
top_dir = os.path.join(dir_dict['gis_data']['path'], "IBGE")

# GDB List:
arcpy.env.workspace = top_dir
gdblist = arcpy.ListWorkspaces(wild_card="*", workspace_type='FileGDB')

# Loop over geodatabases:
for gdb in gdblist:
    arcpy.env.workspace = gdb
    year = os.path.basename(gdb).replace(".gdb", "")
    orig_fc = "T05_malha_municipal_{0}".format(year)
    muni_fc = "T05_malha_municipal_{0}_GCS_WGS_1984".format(year)

    source_fc = os.path.join(gdb, "{0}_intcaps".format(muni_fc))
    source_spref = arcpy.Describe(source_fc).spatialReference
    destin_fc = os.path.join(gdb, "{0}_intcaps".format(orig_fc))

    if arcpy.Describe(orig_fc).spatialReference.type == u'Projected':
        destin_spref = arcpy.Describe(orig_fc).spatialReference
    else:
        destin_spref = arcpy.SpatialReference(4326)

    try:
        arcpy.Project_management(in_dataset=source_fc, out_dataset=destin_fc, out_coor_system=destin_spref)
        print arcpy.GetMessages()
    except arcpy.ExecuteError:
        print arcpy.GetMessages()
        continue
