# NOTE: since this script uses arcpy, make sure that the Python interpreter is Python 2.x

import os
import arcpy
import setup_dirs_2x
import cintra2013

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

for gdb in gdblist:
    arcpy.env.workspace = gdb
    year = os.path.basename(gdb).replace(".gdb", "")
    muni_fc = "T05_malha_municipal_{0}".format(year)
    print muni_fc

    cintra2013.create_capitanias(os.path.join(gdb, muni_fc))
