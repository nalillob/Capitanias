"""
Description: This script is step 7 in the processing of the 1872-1991 IBGE geographical data. Calculates de
distance of each municipality polygon to all capitania borders.

Step 1: Convert capitania polygons to lines, and remove lines that are not the border between one capitania and
another. Also, dissolve line fragments into single features.

Step 2: Calculate near table for the municipality polygon feature class.

Step 3: Calculate near table for the municipality seat point feature class.

Requirements:
setup_dirs_2x.py has to be in the same folder as this script.
"""

# NOTE: since this script uses arcpy, make sure that the Python interpreter is Python 2.x

import os
import arcpy
import setup_dirs_2x


def cap_2_line(cap_fc, clean=False):
    if not arcpy.env.workspace.endswith(".gdb"):
        return "Exited because current workspace is not a geodatabase"

    try:
        arcpy.PolygonToLine_management(in_features=cap_fc,
                                       out_feature_class="{0}_line1".format(cap_fc),
                                       neighbor_option="IDENTIFY_NEIGHBORS")
        print arcpy.GetMessages()
    except arcpy.ExecuteError:
        print arcpy.GetMessages()
        return "Exited step1 because of ExecuteError in PolygonToLine_management."

    try:
        arcpy.Select_analysis(in_features=os.path.join(arcpy.env.workspace, "{0}_line1".format(cap_fc)),
                              out_feature_class=os.path.join(arcpy.env.workspace, "{0}_line2".format(cap_fc)),
                              where_clause="LEFT_FID <> -1 AND LEFT_FID <> RIGHT_FID")
        print arcpy.GetMessages()
    except arcpy.ExecuteError:
        print arcpy.GetMessages()
        return "Exited step1 because of ExecuteError in Select_analysis."

    try:
        arcpy.Dissolve_management(in_features=os.path.join(arcpy.env.workspace, "{0}_line2".format(cap_fc)),
                                  out_feature_class=os.path.join(arcpy.env.workspace, "{0}_line".format(cap_fc)),
                                  dissolve_field="LEFT_FID;RIGHT_FID",
                                  statistics_fields="",
                                  multi_part="MULTI_PART",
                                  unsplit_lines="DISSOLVE_LINES")
        print arcpy.GetMessages()
    except arcpy.ExecuteError:
        print arcpy.GetMessages()
        return "Exited step1 because of ExecuteError in Dissolve_management."

    if clean:
        try:
            arcpy.Delete_management(in_data="{0}_line1".format(cap_fc))
            print arcpy.GetMessages()
        except arcpy.ExecuteError:
            print arcpy.GetMessages()

        try:
            arcpy.Delete_management(in_data="{0}_line2".format(cap_fc))
            print arcpy.GetMessages()
        except arcpy.ExecuteError:
            print arcpy.GetMessages()

    return "{0}_line".format(cap_fc)


# Preferences:
arcpy.env.overwriteOutput = True

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
    # Step 1:
    cap_line_fc = cap_2_line(cap_fc=cap_poly_fc, clean=True)

    # Step 2:
    muni_fc = "T05_malha_municipal_{0}".format(year)
    try:
        arcpy.GenerateNearTable_analysis(in_features=muni_fc,
                                         near_features=cap_line_fc,
                                         out_table="ntable_muni_brdr_to_cap_brdr_{0}".format(year),
                                         search_radius="",
                                         location="LOCATION",
                                         angle="ANGLE",
                                         closest="ALL",
                                         closest_count="0",
                                         method="PLANAR")
        print arcpy.GetMessages()
    except arcpy.ExecuteError:
        print arcpy.GetMessages()
        continue

    # Step 3:
    seat_fc = "T03_sede_municipal_{0}".format(year)
    try:
        arcpy.GenerateNearTable_analysis(in_features=seat_fc,
                                         near_features=cap_line_fc,
                                         out_table="ntable_muni_seat_to_cap_brdr_{0}".format(year),
                                         search_radius="",
                                         location="LOCATION",
                                         angle="ANGLE",
                                         closest="ALL",
                                         closest_count="0",
                                         method="PLANAR")
        print arcpy.GetMessages()
    except arcpy.ExecuteError:
        print arcpy.GetMessages()
        continue
