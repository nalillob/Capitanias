"""Description: This script assigns capitanias (polygon feature class) to municipality and state seats (point feature
classes).

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
gdblist = arcpy.ListWorkspaces(wild_card="*.gdb", workspace_type='FileGDB')

for gdb in gdblist:
    arcpy.env.workspace = gdb
    year = os.path.basename(gdb).replace(".gdb", "")
    cap_poly_fc = [fc for fc in arcpy.ListFeatureClasses(wild_card="capitanias_*", feature_type="POLYGON")
                   if fc.find("ext") == -1][0]

    muni_seat_fc = "T03_sede_municipal_{0}".format(year)
    prov_capital_fc = \
        [fc for fc in arcpy.ListFeatureClasses(wild_card="T02_*", feature_type="POINT") if fc.endswith(year)][0]

    muni_seat_fc_spj_cap_poly = "{0}_spj_caps_poly".format(muni_seat_fc)
    prov_capital_fc_spj_cap_poly = "{0}_spj_caps_poly".format(prov_capital_fc)

    # Spatially join capitania polygons (join features) to municipality seats (target features):
    try:
        arcpy.SpatialJoin_analysis(target_features=muni_seat_fc, join_features=cap_poly_fc,
                                   out_feature_class=muni_seat_fc_spj_cap_poly)
        print arcpy.GetMessages()
    except arcpy.ExecuteError:
        print arcpy.GetMessages()
        continue

    # Spatially join capitania polygons (join features) to state/province capitals (target features):
    try:
        arcpy.SpatialJoin_analysis(target_features=prov_capital_fc, join_features=cap_poly_fc,
                                   out_feature_class=prov_capital_fc_spj_cap_poly)
        print arcpy.GetMessages()
    except arcpy.ExecuteError:
        print arcpy.GetMessages()
        continue
