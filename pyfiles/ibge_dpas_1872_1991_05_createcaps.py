# coding=utf-8
"""DESCRIPTION: This script is step 05 in the processing of IBGE geographical data. Creates a polygon feature class
that corresponds to the capitania boundaries as defined by Cintra (2013). It does this for each DPA feature class for
1872 to 1991 downloaded from IBGE's ftp server.

Requirements:
setup_dirs_2x.py has to be in the same folder as this script.
cintra2013.py has to be in the same folder as this script.

Reference: Cintra, Jorge Pimentel. 2013. “Reconstruindo o Mapa Das Capitanias Hereditárias.” Anais Do Museu Paulista:
História e Cultura Material 21 (2): 11–45. https://doi.org/10.1590/S0101-47142013000200002.
"""

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
