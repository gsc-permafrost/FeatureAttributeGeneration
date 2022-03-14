# -*- coding: utf-8 -*-
# Python 2.7
"""
This script converts the digitized point and line data into a final product of polygons with complete attribute tables.

***THIS CODE IS NOT MEANT TO BE EASILY PORTABLE***
It has been built for a highly specific purpose and requires very specific data sets therefore everything uses hard
coded path names.

Author: rparker
Created: 21-11-2017
"""


import os
import arcpy
import MASTER_featureAttributes_functions as func
import datetime

try:
    import helperFunctions as helper
except:
    import getHelper
    getHelper.getHelper()
    import helperFunctions as helper

combineSurfScript = """
def combineSurf(s1, s2, s3, s4):
    surf = "NoData"
    if s3 != "None":
        surf = s3
    elif s2 != "None":
        surf = s2
    elif s1 != "None":
        surf = s1
    elif s4 != "" and s4 != "None":
        surf = s4
    return(surf)
"""

getPfScript = """
def pfDic(x):
    return{
        "C" : "Continuous",
        "E" : "Extensive Discontinuous",
        "S" : "Sporadic Discontinuous",
        "I" : "Isolated Patches",
        "M" : "Alpine",
        "O" : "Subsea"
    }.get(x,"")

def getPf(c):
    first = c[0]
    desc = pfDic(first)
    return(desc)
"""

getCodeScript = """
def getCode(t):
    return(t)
"""


def main():
    start = datetime.datetime.now()
    print "Code v1.1 \nStarting at:", start

    # PASTE EMAIL HERE
    notify = "**********"
    # PASTE PATH TO DIGITIZED FEATURE GDB HERE
    featureGdb = r"C:\GIS\DempsterMapping\00-geospatialdata\DigitizedFeatures_DH_ITH.gdb"
    # PASTE PATH TO ATTRIBUTE JOIN DATA GDB HERE
    joinGdb = r"C:\GIS\DempsterMapping\00-geospatialdata\attributeJoinData_21_05_11.gdb"

    arcpy.env.workspace = featureGdb
    arcpy.env.overwriteOutput = True

    features = ["mass", "peri", "hydro"]

    for feat in features:
        inPath = feat + "_ln"
        outPath = feat + "_py"
        arcpy.FeatureToPolygon_management(in_features=inPath, out_feature_class=outPath)
        print feat, "lines converted to polygons"

        # Adding attributes from points
        t = feat + "_py"
        j = feat + "_pt"
        o = featureGdb + "/" + feat + "Att_py"
        func.attPtsJoin(t, j, o, feat)
        arcpy.Delete_management(t)
        print feat, "attributes added from points"

        # adding attributes from layers
        lyrs = ["pfIceContent_1M_canada_poly", "nts_snrc_50k", "surficialGeology_1647A", "surficialGeology_1745A",
                "surficialGeology_1746A", "surficialGeology_yukon", "PHYSIOGRAPHIC_POLY_250K"]
            # Add these to list for extra attribute information
            # , "pfMapOfCanada_wedgeIce", "pfMapOfCanada_relicIce", "pfMapOfCanada_segregatedIce", "maxGlacialLimit"]

        for l in lyrs:
            t = o
            j = os.path.join(joinGdb, l)
            if t.endswith("1"):
                o = feat + "Att_py"
            else:
                o = feat + "Att_py1"
            func.addAttJoin(t, j, o)
            arcpy.Delete_management(t)
            print l, "attribute added"

        # Adding imagery attributes
        t = o
        j = os.path.join(joinGdb, "orthoImageFp_att")
        finalLyr = feat + "_final"
        func.imgJoin(t, j, finalLyr)
        arcpy.Delete_management(t)
        print "imagery attributes added"

        # Compiling surficial geology data
        field = "SURF_GEO"
        exp = "combineSurf(str(!SURF_GEO1!), str(!SURF_GEO2!), str(!SURF_GEO3!), str(!SURF_GEO4!))"
        code = combineSurfScript
        arcpy.AddField_management(in_table=finalLyr, field_name=field, field_type="TEXT")
        arcpy.CalculateField_management(in_table=finalLyr, field=field, expression=exp,
                                        expression_type="PYTHON", code_block=code)

        arcpy.DeleteField_management(finalLyr, ["SURF_GEO1", "SURF_GEO2", "SURF_GEO3", "SURF_GEO4"])
        print "surficial geology fields compiled"

        # Determining permafrost description
        field = "PF_DESC"
        exp = "getPf(str(!PF_CODE!))"
        code = getPfScript
        arcpy.AddField_management(in_table=finalLyr, field_name=field, field_type="TEXT")
        arcpy.CalculateField_management(in_table=finalLyr, field=field, expression=exp,
                                        expression_type="PYTHON", code_block=code)
        print "permafrost description determined"

        # adding code fields
        if feat != "mass":
            fields = ["TYPE", "SUBTYPE"]
        else:
            fields = ["TYPE", "SUBTYPE", "MATERIAL", "SUBTYPE_DESC", "ACTIVITY"]
        code = getCodeScript
        for f in fields:
            field = f + "_CODE"
            exp = "getCode(str(!" + f + "!))"
            arcpy.AddField_management(in_table=finalLyr, field_name=field, field_type="TEXT")
            arcpy.CalculateField_management(in_table=finalLyr, field=field, expression=exp,
                                            expression_type="PYTHON", code_block=code)
            print field, "determined"

        # adding class field
        field = "CLASS"
        exp = "getCode(\"" + feat.upper() + "\")"
        code = getCodeScript
        arcpy.AddField_management(in_table=finalLyr, field_name=field, field_type="TEXT")
        arcpy.CalculateField_management(in_table=finalLyr, field=field, expression=exp,
                                        expression_type="PYTHON", code_block=code)
        print "class determined"

        # adding area and latitude/longitude fields
        field = "AREA_HA"
        arcpy.AddField_management(in_table=finalLyr, field_name=field, field_type="DOUBLE")
        arcpy.CalculateField_management(finalLyr, field, "!shape.area@HECTARES!",
                                        expression_type="PYTHON_9.3")

        field = "LAT"
        arcpy.AddField_management(in_table=finalLyr, field_name=field, field_type="DOUBLE")
        arcpy.CalculateField_management(finalLyr, field, "arcpy.PointGeometry(!Shape!.centroid, "
                                                         "!Shape!.spatialReference).projectAs(arcpy.SpatialReference("
                                                         "4326)).centroid.Y", expression_type="PYTHON_9.3")

        field = "LONG"
        arcpy.AddField_management(in_table=finalLyr, field_name=field, field_type="DOUBLE")
        arcpy.CalculateField_management(finalLyr, field, "arcpy.PointGeometry(!Shape!.centroid, "
                                                         "!Shape!.spatialReference).projectAs(arcpy.SpatialReference("
                                                         "4326)).centroid.X", expression_type="PYTHON_9.3")
        print "areas calculated"

        # removing unneeded fields and reorganizing attribute table
        arcpy.DeleteField_management(finalLyr, ["Join_Count", "TARGET_FID"])
        func.reorderAttributes(feat, finalLyr)
        print "Attribute table organized"

        # exporting layer attribute table to CSV
        outCsv = featureGdb[:-4] + "_" + feat + ".csv"
        func.shpToCsv(finalLyr, outCsv)

        print feat, "layer converted to final product and attributes exported as csv for analysis"
        print datetime.datetime.now() - start, "Elapsed since start\n"

    message = "All layers converted to final product and attributes exported as csv for analysis"
    m = helper.emailMessage(notify, message)
    print m
    return


if __name__ == '__main__':
    main()
