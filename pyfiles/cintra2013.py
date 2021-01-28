# coding=utf-8
"""Description: This script is a utility that has a function that takes as input any polygon feature class that
covers Brazil, and with it creates another polygon feature class that corresponds to the Capitanias according to
Cintra (2013).

Reference: Cintra, Jorge Pimentel. 2013. “Reconstruindo o Mapa Das Capitanias Hereditárias.” Anais Do Museu Paulista:
História e Cultura Material 21 (2): 11–45. https://doi.org/10.1590/S0101-47142013000200002.

"""

# NOTE: since this script uses arcpy, make sure that the Python interpreter is Python 2.x

import arcpy
import os


def create_capitanias(path_to_fc, out_spref=None):
    # Parse input:
    if os.path.isabs(path_to_fc):
        source_gdb = os.path.dirname(path_to_fc)
        fc_name = os.path.basename(path_to_fc)
    else:
        source_gdb = os.getcwd()
        fc_name = os.path.basename(path_to_fc)

    if out_spref is None:
        out_spref = arcpy.SpatialReference(4326)

    # Declare working environment:
    arcpy.env.workspace = source_gdb

    # Project input feature class to output spatial reference:
    fc_name_prj = "{0}_{1}".format(fc_name, out_spref.name)
    arcpy.Project_management(in_dataset=fc_name, out_dataset=fc_name_prj, out_coor_system=out_spref)

    # Get projected input feature class properties:
    fc_prj_desc = arcpy.Describe(fc_name_prj)

    # Get projected feature class extent:
    fc_xmin = fc_prj_desc.extent.XMin
    fc_xmax = fc_prj_desc.extent.XMax
    fc_ymin = fc_prj_desc.extent.YMin
    fc_ymax = fc_prj_desc.extent.YMax

    # Create feature class for the Tordesillas Line:
    tordesillas_fc = os.path.join(source_gdb, "tordesillas_{0}".format(out_spref.name))

    if not arcpy.Exists(tordesillas_fc) or (arcpy.Exists(tordesillas_fc) and arcpy.env.overwriteOutput):
        cursor = None
        try:
            # Create empty feature class:
            arcpy.CreateFeatureclass_management(out_path=source_gdb,
                                                out_name="tordesillas_{0}".format(out_spref.name),
                                                geometry_type="POLYLINE",
                                                spatial_reference=out_spref)

            # Create cursor:
            cursor = arcpy.da.InsertCursor(tordesillas_fc, ["SHAPE@"])

            # Fill in points in an array:
            array = arcpy.Array()
            top = arcpy.Point(X=-48.7, Y=fc_ymax * 1.05, ID=1)
            bottom = arcpy.Point(X=-48.7, Y=fc_ymin * 1.05, ID=1)
            array.add(top)
            array.add(bottom)

            # Create line between top and bottom:
            polyline = arcpy.Polyline(array, out_spref)
            cursor.insertRow([polyline])

            print "Tordesillas line created."

        except Exception as e:
            print(e)
        finally:
            # Cleanup the cursor if necessary
            if cursor:
                del cursor
    else:
        print "Tordesillas Line already exists in GDB and no overwrite allowed."

    # Create capitanias feature class:
    capitanias_fc = os.path.join(source_gdb, "capitanias_{0}".format(out_spref.name))
    capitanias_ext = os.path.join(source_gdb, "capitanias_extended_{0}".format(out_spref.name))

    if not arcpy.Exists(capitanias_fc) or (arcpy.Exists(capitanias_fc) and arcpy.env.overwriteOutput):
        print "Capitanias FC does not exist or overwrite is set to True: Creating..."
        if not arcpy.Exists(capitanias_ext) or (arcpy.Exists(capitanias_ext) and arcpy.env.overwriteOutput):
            print "Capitanias FC extended does not exist or overwrite is set to True: Creating..."
            cursor = None
            try:
                # Create empty feature class:
                arcpy.CreateFeatureclass_management(out_path=source_gdb,
                                                    out_name="capitanias_extended_{0}".format(out_spref.name),
                                                    geometry_type="POLYGON",
                                                    spatial_reference=out_spref)

                # Add the relevant fields:
                arcpy.AddField_management(in_table=capitanias_ext, field_name="Name_ascii", field_type="TEXT",
                                          field_length=25)
                arcpy.AddField_management(in_table=capitanias_ext, field_name="Code", field_type="TEXT",
                                          field_length=5)
                arcpy.AddField_management(in_table=capitanias_ext, field_name="Abbrev", field_type="TEXT",
                                          field_length=5)
                arcpy.AddField_management(in_table=capitanias_ext, field_name="Donatario", field_type="TEXT",
                                          field_length=50)
                arcpy.AddField_management(in_table=capitanias_ext, field_name="Limite", field_type="TEXT",
                                          field_length=25)
                arcpy.AddField_management(in_table=capitanias_ext, field_name="Category", field_type="TEXT",
                                          field_length=25)

                fields = ["SHAPE@", "Name_ascii", "Code", "Abbrev", "Donatario", "Limite", "Category"]
                cursor = arcpy.da.InsertCursor(capitanias_ext, fields)

                # Go capitania by capitania, inputing the data:
                # 12A - IT - Pero Lopes de Sousa - Baia da Traicao
                array = arcpy.Array()
                point1 = arcpy.Point(X=-48.7, Y=-6.68, ID=1)
                point2 = arcpy.Point(X=fc_xmax, Y=-6.68, ID=1)
                point3 = arcpy.Point(X=fc_xmax, Y=-7.81, ID=1)
                point4 = arcpy.Point(X=-48.7, Y=-7.81, ID=1)
                array.add(point1)
                array.add(point2)
                array.add(point3)
                array.add(point4)
                polygon = arcpy.Polygon(array, out_spref)
                cursor.insertRow(
                    (polygon, "Itamaraca", "12A", "IT", "Pero Lopes de Sousa", "Baia da Traicao", "Actual"))

                # 5 - PE - Duarte Coelho [Pereira] - Sul da I. de Itamaraca
                array = arcpy.Array()
                point1 = arcpy.Point(X=-48.7, Y=-7.81, ID=2)
                point2 = arcpy.Point(X=fc_xmax, Y=-7.81, ID=2)
                point3 = arcpy.Point(X=fc_xmax, Y=-10.50, ID=2)
                point4 = arcpy.Point(X=-48.7, Y=-10.50, ID=2)
                array.add(point1)
                array.add(point2)
                array.add(point3)
                array.add(point4)
                polygon = arcpy.Polygon(array, out_spref)
                cursor.insertRow(
                    (polygon, "Pernambuco", "5", "PE", "Duarte Coelho [Pereira]", "Sul da I. de Itamaraca", "Actual"))

                # 6 - BA - Francisco Pereira Coutinho - Rio de Sao Francisco
                array = arcpy.Array()
                point1 = arcpy.Point(X=-48.7, Y=-10.50, ID=3)
                point2 = arcpy.Point(X=fc_xmax, Y=-10.50, ID=3)
                point3 = arcpy.Point(X=fc_xmax, Y=-13.14, ID=3)
                point4 = arcpy.Point(X=-48.7, Y=-13.14, ID=3)
                array.add(point1)
                array.add(point2)
                array.add(point3)
                array.add(point4)
                polygon = arcpy.Polygon(array, out_spref)
                cursor.insertRow(
                    (polygon, "Bahia", "6", "BA", "Francisco Pereira Coutinho", "Rio de Sao Francisco", "Actual"))

                # 7 - IL - Jorge de Figueiredo Correia - Sul da Baia de TS
                array = arcpy.Array()
                point1 = arcpy.Point(X=-48.7, Y=-13.14, ID=4)
                point2 = arcpy.Point(X=fc_xmax, Y=-13.14, ID=4)
                point3 = arcpy.Point(X=fc_xmax, Y=-15.65, ID=4)
                point4 = arcpy.Point(X=-48.7, Y=-15.65, ID=4)
                array.add(point1)
                array.add(point2)
                array.add(point3)
                array.add(point4)
                polygon = arcpy.Polygon(array, out_spref)
                cursor.insertRow(
                    (polygon, "Ilheus", "7", "IL", "Jorge de Figueiredo Correia", "Sul da Baia de TS", "Actual"))

                # 8 - PS - Pedro do Campo Tourinho - Rio Pardo
                array = arcpy.Array()
                point1 = arcpy.Point(X=-48.7, Y=-15.65, ID=5)
                point2 = arcpy.Point(X=fc_xmax, Y=-15.65, ID=5)
                point3 = arcpy.Point(X=fc_xmax, Y=-18.09, ID=5)
                point4 = arcpy.Point(X=-48.7, Y=-18.09, ID=5)
                array.add(point1)
                array.add(point2)
                array.add(point3)
                array.add(point4)
                polygon = arcpy.Polygon(array, out_spref)
                cursor.insertRow(
                    (polygon, "Porto Seguro", "8", "PS", "Pedro do Campo Tourinho", "Rio Pardo", "Actual"))

                # 9 - ES - Vasco Fernandes Coutinho - Rio Mucuri
                array = arcpy.Array()
                point1 = arcpy.Point(X=-48.7, Y=-18.09, ID=6)
                point2 = arcpy.Point(X=fc_xmax, Y=-18.09, ID=6)
                point3 = arcpy.Point(X=fc_xmax, Y=-21.00, ID=6)
                point4 = arcpy.Point(X=-48.7, Y=-21.00, ID=6)
                array.add(point1)
                array.add(point2)
                array.add(point3)
                array.add(point4)
                polygon = arcpy.Polygon(array, out_spref)
                cursor.insertRow(
                    (polygon, "Espirito Santo", "9", "ES", "Vasco Fernandes Coutinho", "Rio Mucuri", "Actual"))

                # 9 - ES - Vasco Fernandes Coutinho - Rio Mucuri
                array = arcpy.Array()
                point1 = arcpy.Point(X=-48.7, Y=-18.09, ID=6)
                point2 = arcpy.Point(X=fc_xmax, Y=-18.09, ID=6)
                point3 = arcpy.Point(X=fc_xmax, Y=-21.00, ID=6)
                point4 = arcpy.Point(X=-48.7, Y=-21.00, ID=6)
                array.add(point1)
                array.add(point2)
                array.add(point3)
                array.add(point4)
                polygon = arcpy.Polygon(array, out_spref)
                cursor.insertRow(
                    (polygon, "Espirito Santo", "9", "ES", "Vasco Fernandes Coutinho", "Rio Mucuri", "Actual"))

                # 10 - ST - Pero de Gois [da Silveira] - Rio Itapemirim
                array = arcpy.Array()
                point1 = arcpy.Point(X=-43.16, Y=-21.00, ID=7)
                point2 = arcpy.Point(X=fc_xmax, Y=-21.00, ID=7)
                point3 = arcpy.Point(X=-41.78 + max(abs(fc_xmax - -41.78), abs(fc_ymin - -22.38)),
                                     Y=-22.38 - min(abs(fc_xmax - -41.78), abs(fc_ymin - -22.38)), ID=7)
                point4 = arcpy.Point(X=-41.78 + min(abs(fc_xmax - -41.78), abs(fc_ymin - -22.38)),
                                     Y=-22.38 - min(abs(fc_xmax - -41.78), abs(fc_ymin - -22.38)), ID=7)
                point5 = arcpy.Point(X=-41.78, Y=-22.38, ID=7)
                array.add(point1)
                array.add(point2)
                array.add(point3)
                array.add(point4)
                array.add(point5)
                polygon = arcpy.Polygon(array, out_spref)
                cursor.insertRow(
                    (polygon, "Sao Tome", "10", "ST", "Pero de Gois [da Silveira]", "Rio Itapemirim", "Actual"))

                # 11A - SV1 - Martim Afonso de Sousa - Rio Macae
                array = arcpy.Array()
                point1 = arcpy.Point(X=-48.70, Y=-21.00, ID=8)
                point2 = arcpy.Point(X=-43.16, Y=-21.00, ID=8)
                point3 = arcpy.Point(X=-41.78, Y=-22.38, ID=8)
                point4 = arcpy.Point(X=-41.78 + min(abs(fc_xmax - -41.78), abs(fc_ymin - -22.38)),
                                     Y=-22.38 - min(abs(fc_xmax - -41.78), abs(fc_ymin - -22.38)), ID=8)
                point5 = arcpy.Point(X=-45.43 + min(abs(fc_xmax - -45.43), abs(fc_ymin - -23.71)),
                                     Y=-23.71 - min(abs(fc_xmax - -45.43), abs(fc_ymin - -23.71)), ID=8)
                point6 = arcpy.Point(X=-45.43, Y=-23.71, ID=8)
                point7 = arcpy.Point(X=-46.14, Y=-23.00, ID=8)
                point8 = arcpy.Point(X=-48.70, Y=-23.00, ID=8)

                array.add(point1)
                array.add(point2)
                array.add(point3)
                array.add(point4)
                array.add(point5)
                array.add(point6)
                array.add(point7)
                array.add(point8)
                polygon = arcpy.Polygon(array, out_spref)
                cursor.insertRow(
                    (polygon, "Sao Vicente 1", "11A", "SV1", "Martim Afonso de Sousa", "Rio Macae", "Actual"))

                # 12B - SA - Pero Lopes de Sousa - Rio Juquiriquere
                array = arcpy.Array()
                point1 = arcpy.Point(X=-48.70, Y=-23.00, ID=9)
                point2 = arcpy.Point(X=-46.14, Y=-23.00, ID=9)
                point3 = arcpy.Point(X=-45.43, Y=-23.71, ID=9)
                point4 = arcpy.Point(X=-45.43 + min(abs(fc_xmax - -45.43), abs(fc_ymin - -23.71)),
                                     Y=-23.71 - min(abs(fc_xmax - -45.43), abs(fc_ymin - -23.71)), ID=9)
                point5 = arcpy.Point(X=-46.13 + min(abs(fc_xmax - -46.13), abs(fc_ymin - -23.86)),
                                     Y=-23.86 - min(abs(fc_xmax - -46.13), abs(fc_ymin - -23.86)), ID=9)
                point6 = arcpy.Point(X=-46.13, Y=-23.86, ID=9)
                point7 = arcpy.Point(X=-48.70, Y=-23.86, ID=9)

                array.add(point1)
                array.add(point2)
                array.add(point3)
                array.add(point4)
                array.add(point5)
                array.add(point6)
                array.add(point7)
                polygon = arcpy.Polygon(array, out_spref)
                cursor.insertRow(
                    (polygon, "Santo Amaro", "12B", "SA", "Pero Lopes de Sousa", "Rio Juquiriquere", "Actual"))

                # 11B - SV2 - Martim Afonso de Sousa - Barra de Bertioga
                array = arcpy.Array()
                point1 = arcpy.Point(X=-48.70, Y=-23.86, ID=10)
                point2 = arcpy.Point(X=-46.13, Y=-23.86, ID=10)
                point3 = arcpy.Point(X=-46.13 + min(abs(fc_xmax - -46.13), abs(fc_ymin - -23.86)),
                                     Y=-23.86 - min(abs(fc_xmax - -46.13), abs(fc_ymin - -23.86)), ID=10)
                point4 = arcpy.Point(X=-48.36, Y=-25.55, ID=10)
                point5 = arcpy.Point(X=-48.70, Y=-25.55, ID=10)

                array.add(point1)
                array.add(point2)
                array.add(point3)
                array.add(point4)
                array.add(point5)
                polygon = arcpy.Polygon(array, out_spref)
                cursor.insertRow(
                    (polygon, "Sao Vicente 2", "11B", "SV2", "Martim Afonso de Sousa", "Barra de Bertioga", "Actual"))
                # 12C - ST - Pero Lopes de Sousa - Barra sul de Paranagua
                array = arcpy.Array()
                point1 = arcpy.Point(X=-48.70, Y=-25.55, ID=11)
                point2 = arcpy.Point(X=-48.36, Y=-25.55, ID=11)
                point3 = arcpy.Point(X=-46.13 + min(abs(fc_xmax - -46.13), abs(fc_ymin - -23.86)),
                                     Y=-23.86 - min(abs(fc_xmax - -46.13), abs(fc_ymin - -23.86)), ID=11)
                point4 = arcpy.Point(X=-48.70, Y=-28.33, ID=11)

                array.add(point1)
                array.add(point2)
                array.add(point3)
                array.add(point4)
                polygon = arcpy.Polygon(array, out_spref)
                cursor.insertRow(
                    (polygon, "Santana", "12C", "ST", "Pero Lopes de Sousa", "Barra sul de Paranagua", "Actual"))

                # 1A - MA1 - Aires de Cunha - Rio Turiacu
                array = arcpy.Array()
                point1 = arcpy.Point(X=-45.25, Y=fc_ymax, ID=12)
                point2 = arcpy.Point(X=-45.25, Y=-6.68, ID=12)
                point3 = arcpy.Point(X=-44.36, Y=-6.68, ID=12)
                point4 = arcpy.Point(X=-44.36, Y=fc_ymax, ID=12)

                array.add(point1)
                array.add(point2)
                array.add(point3)
                array.add(point4)
                polygon = arcpy.Polygon(array, out_spref)
                cursor.insertRow(
                    (polygon, "Maranhao 1", "1A", "MA1", "Aires de Cunha", "Rio Turiacu", "Actual"))

                # 2A - MA2 - Joao de Barros - Ponto intermediario
                array = arcpy.Array()
                point1 = arcpy.Point(X=-44.36, Y=fc_ymax, ID=13)
                point2 = arcpy.Point(X=-44.36, Y=-6.68, ID=13)
                point3 = arcpy.Point(X=-43.75, Y=-6.68, ID=13)
                point4 = arcpy.Point(X=-43.75, Y=fc_ymax, ID=13)

                array.add(point1)
                array.add(point2)
                array.add(point3)
                array.add(point4)
                polygon = arcpy.Polygon(array, out_spref)
                cursor.insertRow(
                    (polygon, "Maranhao 2", "2A", "MA2", "Joao de Barros", "Ponto intermediario", "Actual"))

                # 3 - PI - Fernando Alvares de Andrade - Ilha de Santana (oeste)
                array = arcpy.Array()
                point1 = arcpy.Point(X=-43.75, Y=fc_ymax, ID=14)
                point2 = arcpy.Point(X=-43.75, Y=-6.68, ID=14)
                point3 = arcpy.Point(X=-40.85, Y=-6.68, ID=14)
                point4 = arcpy.Point(X=-40.85, Y=fc_ymax, ID=14)

                array.add(point1)
                array.add(point2)
                array.add(point3)
                array.add(point4)
                polygon = arcpy.Polygon(array, out_spref)
                cursor.insertRow(
                    (polygon, "Piaui", "3", "PI", "Fernando Alvares de Andrade", "Ilha de Santana (oeste)", "Actual"))

                # 4 - CE - Antonio Cardoso de Barros - Camocim
                array = arcpy.Array()
                point1 = arcpy.Point(X=-40.85, Y=fc_ymax, ID=15)
                point2 = arcpy.Point(X=-40.85, Y=-6.68, ID=15)
                point3 = arcpy.Point(X=-38.46, Y=-6.68, ID=15)
                point4 = arcpy.Point(X=-38.46, Y=fc_ymax, ID=15)

                array.add(point1)
                array.add(point2)
                array.add(point3)
                array.add(point4)
                polygon = arcpy.Polygon(array, out_spref)
                cursor.insertRow(
                    (polygon, "Ceara", "4", "CE", "Antonio Cardoso de Barros", "Camocim", "Actual"))

                # 1B - RN1 - Aires da Cunha - Mucuripe
                array = arcpy.Array()
                point1 = arcpy.Point(X=-38.46, Y=fc_ymax, ID=16)
                point2 = arcpy.Point(X=-38.46, Y=-6.68, ID=16)
                point3 = arcpy.Point(X=-36.66, Y=-6.68, ID=16)
                point4 = arcpy.Point(X=-36.66, Y=fc_ymax, ID=16)

                array.add(point1)
                array.add(point2)
                array.add(point3)
                array.add(point4)
                polygon = arcpy.Polygon(array, out_spref)
                cursor.insertRow(
                    (polygon, "Rio Grande do Norte 1", "1B", "RN1", "Aires da Cunha", "Mucuripe", "Actual"))

                # 2B - RN2 - Joao de Barros - Ponto intermediario
                array = arcpy.Array()
                point1 = arcpy.Point(X=-36.66, Y=fc_ymax, ID=17)
                point2 = arcpy.Point(X=-36.66, Y=-6.68, ID=17)
                point3 = arcpy.Point(X=fc_xmax, Y=-6.68, ID=17)
                point4 = arcpy.Point(X=fc_xmax, Y=fc_ymax, ID=17)

                array.add(point1)
                array.add(point2)
                array.add(point3)
                array.add(point4)
                polygon = arcpy.Polygon(array, out_spref)
                cursor.insertRow(
                    (polygon, "Rio Grande do Norte 2", "2B", "RN2", "Joao de Barros", "Ponto intermediario", "Actual"))

                # Nondistributed land
                array = arcpy.Array()
                point1 = arcpy.Point(X=-48.70, Y=fc_ymax, ID=18)
                point2 = arcpy.Point(X=-48.70, Y=-6.68, ID=18)
                point3 = arcpy.Point(X=-45.25, Y=-6.68, ID=18)
                point4 = arcpy.Point(X=-45.25, Y=fc_ymax, ID=18)

                array.add(point1)
                array.add(point2)
                array.add(point3)
                array.add(point4)
                polygon = arcpy.Polygon(array, out_spref)
                cursor.insertRow((polygon, "Non-distributed land", "", "", "", "", "Actual"))

                # Placebo capitania 1
                array = arcpy.Array()
                point1 = arcpy.Point(X=fc_xmin, Y=fc_ymax, ID=19)
                point2 = arcpy.Point(X=fc_xmin, Y=-6.68, ID=19)
                point3 = arcpy.Point(X=-48.70, Y=-6.68, ID=19)
                point4 = arcpy.Point(X=-48.70, Y=fc_ymax, ID=19)

                array.add(point1)
                array.add(point2)
                array.add(point3)
                array.add(point4)
                polygon = arcpy.Polygon(array, out_spref)
                cursor.insertRow((polygon, "Placebo 1", "0A", "PC1", "", "", "Placebo"))

                # Placebo capitania 2
                array = arcpy.Array()
                point1 = arcpy.Point(X=fc_xmin, Y=-6.68, ID=20)
                point2 = arcpy.Point(X=fc_xmin, Y=-7.81, ID=20)
                point3 = arcpy.Point(X=-48.70, Y=-7.81, ID=20)
                point4 = arcpy.Point(X=-48.70, Y=-6.68, ID=20)

                array.add(point1)
                array.add(point2)
                array.add(point3)
                array.add(point4)
                polygon = arcpy.Polygon(array, out_spref)
                cursor.insertRow((polygon, "Placebo 2", "0B", "PC2", "", "", "Placebo"))

                # Placebo capitania 3
                array = arcpy.Array()
                point1 = arcpy.Point(X=fc_xmin, Y=-7.81, ID=21)
                point2 = arcpy.Point(X=fc_xmin, Y=-10.50, ID=21)
                point3 = arcpy.Point(X=-48.70, Y=-10.50, ID=21)
                point4 = arcpy.Point(X=-48.70, Y=-7.81, ID=21)

                array.add(point1)
                array.add(point2)
                array.add(point3)
                array.add(point4)
                polygon = arcpy.Polygon(array, out_spref)
                cursor.insertRow((polygon, "Placebo 3", "0C", "PC3", "", "", "Placebo"))

                # Placebo capitania 4
                array = arcpy.Array()
                point1 = arcpy.Point(X=fc_xmin, Y=-10.50, ID=22)
                point2 = arcpy.Point(X=fc_xmin, Y=-13.14, ID=22)
                point3 = arcpy.Point(X=-48.70, Y=-13.14, ID=22)
                point4 = arcpy.Point(X=-48.70, Y=-10.50, ID=22)

                array.add(point1)
                array.add(point2)
                array.add(point3)
                array.add(point4)
                polygon = arcpy.Polygon(array, out_spref)
                cursor.insertRow((polygon, "Placebo 4", "0D", "PC4", "", "", "Placebo"))

                # Placebo capitania 5
                array = arcpy.Array()
                point1 = arcpy.Point(X=fc_xmin, Y=-13.14, ID=23)
                point2 = arcpy.Point(X=fc_xmin, Y=-15.65, ID=23)
                point3 = arcpy.Point(X=-48.70, Y=-15.65, ID=23)
                point4 = arcpy.Point(X=-48.70, Y=-13.14, ID=23)

                array.add(point1)
                array.add(point2)
                array.add(point3)
                array.add(point4)
                polygon = arcpy.Polygon(array, out_spref)
                cursor.insertRow((polygon, "Placebo 5", "0E", "PC5", "", "", "Placebo"))

                # Placebo capitania 6
                array = arcpy.Array()
                point1 = arcpy.Point(X=fc_xmin, Y=-15.65, ID=24)
                point2 = arcpy.Point(X=fc_xmin, Y=-18.09, ID=24)
                point3 = arcpy.Point(X=-48.70, Y=-18.09, ID=24)
                point4 = arcpy.Point(X=-48.70, Y=-15.65, ID=24)

                array.add(point1)
                array.add(point2)
                array.add(point3)
                array.add(point4)
                polygon = arcpy.Polygon(array, out_spref)
                cursor.insertRow((polygon, "Placebo 6", "0F", "PC6", "", "", "Placebo"))

                # Placebo capitania 7
                array = arcpy.Array()
                point1 = arcpy.Point(X=fc_xmin, Y=-18.09, ID=25)
                point2 = arcpy.Point(X=fc_xmin, Y=-21.00, ID=25)
                point3 = arcpy.Point(X=-48.70, Y=-21.00, ID=25)
                point4 = arcpy.Point(X=-48.70, Y=-18.09, ID=25)

                array.add(point1)
                array.add(point2)
                array.add(point3)
                array.add(point4)
                polygon = arcpy.Polygon(array, out_spref)
                cursor.insertRow((polygon, "Placebo 7", "0G", "PC7", "", "", "Placebo"))

                # Placebo capitania 8
                array = arcpy.Array()
                point1 = arcpy.Point(X=fc_xmin, Y=-21.00, ID=26)
                point2 = arcpy.Point(X=fc_xmin, Y=-23.00, ID=26)
                point3 = arcpy.Point(X=-48.70, Y=-23.00, ID=26)
                point4 = arcpy.Point(X=-48.70, Y=-21.00, ID=26)

                array.add(point1)
                array.add(point2)
                array.add(point3)
                array.add(point4)
                polygon = arcpy.Polygon(array, out_spref)
                cursor.insertRow((polygon, "Placebo 8", "0H", "PC8", "", "", "Placebo"))

                # Placebo capitania 9
                array = arcpy.Array()
                point1 = arcpy.Point(X=fc_xmin, Y=-23.00, ID=27)
                point2 = arcpy.Point(X=fc_xmin, Y=-23.86, ID=27)
                point3 = arcpy.Point(X=-48.70, Y=-23.86, ID=27)
                point4 = arcpy.Point(X=-48.70, Y=-23.00, ID=27)

                array.add(point1)
                array.add(point2)
                array.add(point3)
                array.add(point4)
                polygon = arcpy.Polygon(array, out_spref)
                cursor.insertRow((polygon, "Placebo 9", "0I", "PC9", "", "", "Placebo"))

                # Placebo capitania 10
                array = arcpy.Array()
                point1 = arcpy.Point(X=fc_xmin, Y=-23.86, ID=28)
                point2 = arcpy.Point(X=fc_xmin, Y=-25.55, ID=28)
                point3 = arcpy.Point(X=-48.70, Y=-25.55, ID=28)
                point4 = arcpy.Point(X=-48.70, Y=-23.86, ID=28)

                array.add(point1)
                array.add(point2)
                array.add(point3)
                array.add(point4)
                polygon = arcpy.Polygon(array, out_spref)
                cursor.insertRow((polygon, "Placebo 10", "0J", "PC10", "", "", "Placebo"))

                # Placebo capitania 11
                array = arcpy.Array()
                point1 = arcpy.Point(X=fc_xmin, Y=-25.55, ID=29)
                point2 = arcpy.Point(X=fc_xmin, Y=fc_ymin, ID=29)
                point3 = arcpy.Point(X=-48.70, Y=fc_ymin, ID=29)
                point4 = arcpy.Point(X=-48.70, Y=-25.55, ID=29)

                array.add(point1)
                array.add(point2)
                array.add(point3)
                array.add(point4)
                polygon = arcpy.Polygon(array, out_spref)
                cursor.insertRow((polygon, "Placebo 11", "0K", "PC11", "", "", "Placebo"))

            except Exception as e:
                print e
            finally:
                # Cleanup the cursor if necessary
                if cursor:
                    del cursor

            print "capitanias_ext has", arcpy.GetCount_management(in_rows=capitanias_ext), "rows."
        else:
            print "Capitanias FC extended already exists or overwrite set to False: Done."

        # Intersect the extended capitanias FC and the input fc to remove the sea from the former:
        cursor = None
        try:
            arcpy.Intersect_analysis(in_features=[capitanias_ext, fc_name], out_feature_class="temp_int")
            arcpy.Dissolve_management(in_features="temp_int",
                                      out_feature_class=capitanias_fc,
                                      dissolve_field=["Name_ascii", "Code", "Abbrev",
                                                      "Donatario", "Limite", "Category"])
        except Exception as e:
            print e
        finally:
            # Cleanup the cursor if necessary
            if cursor:
                del cursor
            # Delete temp intersection if necessary:
            if arcpy.Exists("temp_int"):
                arcpy.Delete_management(in_data="temp_int")
    else:
        print "Capitanias FC already exists or overwrite set to False: Done."

    return
