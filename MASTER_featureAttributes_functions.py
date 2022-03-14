# -*- coding: utf-8 -*-
"""Contains the functions required by featureAttributes.py

Author: rparker
Created: 30-01-2018
"""

import arcpy
import csv
import MASTER_featureAttributes_dics as ds

getSourceScript = """
def seperateMultiInputs(inString, delimiter):
    fileList = []
    path = ""
    for char in inString:
        if char != delimiter:
            path = path + char
        else:
            fileList.append(path)
            path = ""
    fileList.append(path)
    return(fileList)


def getSource(iSet, iSetAll, iNum, iNumAll, iSourceAll):
    iSource = "NoData"
    setList = seperateMultiInputs(iSetAll, ",")
    numList = seperateMultiInputs(iNumAll, ",")
    sourceList = seperateMultiInputs(iSourceAll, ",")

    for x in range(len(numList)):
        if iNum.endswith(numList[x]) and setList[x].endswith(iSet):
            iSource = sourceList[x]
            break
    return(iSource)
"""

getDateScript = """
def seperateMultiInputs(inString, delimiter):
    fileList = []
    path = ""
    for char in inString:
        if char != delimiter:
            path = path + char
        else:
            fileList.append(path)
            path = ""
    fileList.append(path)
    return(fileList)


def getDate(iSet, iSetAll, iNum, iNumAll, iDateAll):
    iDate = "NoData"
    setList = seperateMultiInputs(iSetAll, ",")
    numList = seperateMultiInputs(iNumAll, ",")
    dateList = seperateMultiInputs(iDateAll, ",")

    for x in range(len(numList)):
        if iNum.endswith(numList[x]) and setList[x].endswith(iSet):
            iDate = dateList[x]
            break
    return(iDate)
"""

getValuesScript = """
def getValues(x):
    return(x)
"""


def attPtsJoin(target, join, out, feature):
    """Adds user input attributes to a polygon layer

    This function adds the user input attributes from the point features created during the digitization process to the
    polygon features created from the line digitized line features.

    :param target: The path of the polygon layer the attributes will be joined to
    :param join: The path of the layer whose attributes will be joined
    :param out: The path of the new joined layer
    :param feature: the feature type of the layer being input (mass, peri, hydro)
    """
    operation = "JOIN_ONE_TO_ONE"
    jType = "KEEP_COMMON"
    match = "CONTAINS"

    fMapping = arcpy.FieldMappings()
    fMapping.addTable(join)

    fieldMaps = fMapping.fieldMappings
    fields = fMapping.fields
    fNames = []
    for x in range(len(fieldMaps)):
        name = fields[x].name
        fNames.append(name)
        index = fMapping.findFieldMapIndex(name)
        fMap = fieldMaps[x]
        fMap.mergeRule = "Join"
        fMap.joinDelimiter = ","
        fMapping.replaceFieldMap(index, fMap)

    fMappingStr = fMapping.exportToString()

    arcpy.SpatialJoin_analysis(target_features=target, join_features=join, out_feature_class=out, join_type=jType,
                               field_mapping=fMappingStr, match_option=match, join_operation=operation)
    domain = ""
    for n in fNames:
        if feature == "peri":
            domain = ds.periSwitch(n)
        elif feature == "mass":
            domain = ds.massSwitch(n)
        elif feature == "hydro":
            domain = ds.hydroSwitch(n)
        if domain != "":
            arcpy.AssignDomainToField_management(in_table=out, field_name=n, domain_name=domain)
    return


def addAttJoin(target, join, out):
    """Adds a specific attribute based on the join layer to the target layer

    This function takes in the digitized polygon features and adds a specific attribute field from the join feature's
    attribute table to the attribute table of the digitized polygons.

    :param target: The path of the layer the attributes will be joined to
    :param join: The path of the layer whose attributes will be joined
    :param out: The path of the new joined layer
    """
    operation = "JOIN_ONE_TO_ONE"
    jType = "KEEP_ALL"

    jName = arcpy.Describe(join).name
    if jName == "testSites_v2" or jName == "testSites_v1":
        match = "INTERSECT"
    else:
        match = "HAVE_THEIR_CENTER_IN"

    jField = ds.addInfoDic(jName)
    oField = ds.fNameDic(jName)

    fMapping = arcpy.FieldMappings()
    fMapping.addTable(join)

    index = fMapping.findFieldMapIndex(jField)
    fMap = fMapping.getFieldMap(index)

    fMap.mergeRule = "Join"
    fMap.joinDelimiter = ","

    f = fMap.outputField
    f.name = oField
    f.aliasName = oField
    fMap.outputField = f

    fMapping.removeAll()
    fMapping.addTable(target)
    fMapping.addFieldMap(fMap)

    index = fMapping.findFieldMapIndex("Join_Count")
    fMapping.removeFieldMap(index)
    index = fMapping.findFieldMapIndex("TARGET_FID")
    fMapping.removeFieldMap(index)

    fMappingStr = fMapping.exportToString()

    arcpy.SpatialJoin_analysis(target_features=target, join_features=join, out_feature_class=out, join_type=jType,
                               field_mapping=fMappingStr, match_option=match, join_operation=operation)
    return


def imgJoin(target, join, out):
    """Adds multiple attributes describing the satellite image the data was digitized from

    This function adds multiple attributes from the imagery footprint features to the digitized polygons attribute
    table. It then uses the information from the user input imagery fields to sort through the information added and
    picks out only the sections that are relevant to the feature then deletes the remaining data.

    :param target: The path of the layer the attributes will be joined to
    :param join: The path of the layer whose attributes will be joined
    :param out: The path of the new joined layer
    """
    operation = "JOIN_ONE_TO_ONE"
    jType = "KEEP_ALL"
    match = "HAVE_THEIR_CENTER_IN"
    keepList = ["SOURCE", "DATE", "IMG_NUM", "IMG_SET"]

    fMapping = arcpy.FieldMappings()
    fMapping.addTable(join)

    fieldMaps = fMapping.fieldMappings
    fields = fMapping.fields

    for x in range(len(fieldMaps)):
        name = fields[x].name
        index = fMapping.findFieldMapIndex(name)
        keep = False
        for f in keepList:
            if name == f:
                keep = True
                break
        if keep:
            oField = ds.imgNameDic(name)
            fMap = fieldMaps[x]
            fMap.mergeRule = "Join"
            fMap.joinDelimiter = ","
            f = fMap.outputField
            f.name = oField
            f.aliasName = oField
            if name == "SOURCE":
                f.length = 100
            fMap.outputField = f

            fMapping.replaceFieldMap(index, fMap)
        else:
            fMapping.removeFieldMap(index)

    fMapping.addTable(target)
    index = fMapping.findFieldMapIndex("Join_Count")
    fMapping.removeFieldMap(index)
    index = fMapping.findFieldMapIndex("TARGET_FID")
    fMapping.removeFieldMap(index)

    fMappingStr = fMapping.exportToString()

    arcpy.SpatialJoin_analysis(target_features=target, join_features=join, out_feature_class=out, join_type=jType,
                               field_mapping=fMappingStr, match_option=match, join_operation=operation)
    arcpy.AssignDomainToField_management(in_table=out, field_name="IMG_SET_IN", domain_name="IMG_SET")
    arcpy.AssignDomainToField_management(in_table=out, field_name="IMG_NUM_IN", domain_name="IMG_NUM")

    field = "IMG_SOURCE"
    exp = "getSource(str(!IMG_SET_IN!), str(!IMG_SET_ALL!), str(!IMG_NUM_IN!),  str(!IMG_NUM_ALL!), " \
          "str(!IMG_SOURCE_ALL!)) "
    code = getSourceScript
    arcpy.AddField_management(in_table=out, field_name=field, field_type="TEXT")
    arcpy.CalculateField_management(in_table=out, field=field, expression=exp, expression_type="PYTHON",
                                    code_block=code)

    field = "IMG_DATE"
    exp = "getDate(str(!IMG_SET_IN!), str(!IMG_SET_ALL!), str(!IMG_NUM_IN!),  str(!IMG_NUM_ALL!), str(!IMG_DATE_ALL!))"
    code = getDateScript
    arcpy.AddField_management(in_table=out, field_name=field, field_type="TEXT")
    arcpy.CalculateField_management(in_table=out, field=field, expression=exp, expression_type="PYTHON",
                                    code_block=code)

    arcpy.DeleteField_management(out, ["IMG_SOURCE_ALL", "IMG_SET_ALL", "IMG_NUM_ALL", "IMG_DATE_ALL"])
    return


def shpToCsv(shp, outFile):
    """Takes in a shapefile and exports the attribute table as a CSV file.

    :param shp: The path of the shapefile whose data will be exported
    :param outFile: The path of the output CSV file
    """
    fields = arcpy.Describe(shp).fields
    fNames = []
    tbl = []
    swap = ["IND_MUL_", "TYPE_", "SUBTYPE_", "IMG_SET_", "ACTIVITY_", "ORIENTED_", "MATERIAL_", "SUBTYPE_DESC_"]

    for f in fields:
        fNames.append(f.name)

    with arcpy.da.SearchCursor(shp, fNames) as cursor:
        for row in cursor:
            tbl.append(list(row))

    names = [s for s in swap if s in fNames]

    for x in range(len(tbl)):
        for n in names:
            i = fNames.index(n)
            if n == "IND_MUL_":
                tbl[x][i] = ds.indMulDic(tbl[x][i])
            if n == "IMG_SET_":
                tbl[x][i] = ds.imgSetDic(tbl[x][i])
            if n == "ACTIVITY_":
                tbl[x][i] = ds.actDic(tbl[x][i])
            if n == "ORIENTED_":
                tbl[x][i] = ds.orientDic(tbl[x][i])
            if n == "MATERIAL_":
                tbl[x][i] = ds.mMaterialDic(tbl[x][i])
            if n == "SUBTYPE_DESC_":
                tbl[x][i] = ds.mSubtypeDescDic(tbl[x][i])
            if n == "TYPE_":
                if shp.startswith("mass"):
                    tbl[x][i] = ds.mTypeDic(tbl[x][i])
                if shp.startswith("peri"):
                    tbl[x][i] = ds.pTypeDic(tbl[x][i])
                if shp.startswith("hydro"):
                    tbl[x][i] = ds.hTypeDic(tbl[x][i])
            if n == "SUBTYPE_":
                if shp.startswith("mass"):
                    tbl[x][i] = ds.mSubtypeDic(tbl[x][i])
                if shp.startswith("peri"):
                    tbl[x][i] = ds.pSubtypeDic(tbl[x][i])
                if shp.startswith("hydro"):
                    tbl[x][i] = ds.hSubtypeDic(tbl[x][i])

    with open(outFile, 'wb') as outFile:
        w = csv.writer(outFile)
        w.writerow(fNames)
        for r in tbl:
            w.writerow(r)
    return


def reorderAttributes(feature, lyr):
    """
    reorders the fields of a layers attribute table based on the features it represents

    :param feature: the feature type of the layer being input (mass, peri, hydro)
    :param lyr: the path of the layer whose attributes will be reordered
    """
    fnames = [f.name for f in arcpy.ListFields(lyr)]
    order = []

    omitNames = [u'OBJECTID', u'Shape', u'Shape_Length', u'Shape_Area']
    imgDomains = [u"IMG_SET_IN", u"IMG_NUM_IN"]
    for oN in omitNames:
        fnames.remove(oN)
    for n in fnames:
        if feature == "mass":
            o = ds.massAttributeOrder(n)
        elif feature == "peri":
            o = ds.periAttributeOrder(n)
        else:
            o = ds.hydroAttributeOrder(n)
        print(n, o)
        order.append(o)

    newNamesFull = [None] * max(order)
    for x in range(len(order)):
        num = order[x] - 1
        newNamesFull[num] = fnames[x]

    newNames = []
    for x in newNamesFull:
        if x is not None:
            newNames.append(x)

    for n in newNames:
        if n.endswith("2"):
            field = n[:-1] + "_"
        elif n.endswith("IN"):
            field = n[:-2]
        else:
            field = n + "_"
        exp = "getValues(str(!" + n + "!))"
        code = getValuesScript
        arcpy.AddField_management(in_table=lyr, field_name=field, field_type="TEXT")
        arcpy.CalculateField_management(in_table=lyr, field=field, expression=exp, expression_type="PYTHON",
                                        code_block=code)
        arcpy.DeleteField_management(lyr, n)

        if feature == "mass":
            if ds.massSwitch(n) != "":
                arcpy.AssignDomainToField_management(in_table=lyr, field_name=field, domain_name=ds.massSwitch(n))
        elif feature == "peri":
            if ds.periSwitch(n) != "":
                arcpy.AssignDomainToField_management(in_table=lyr, field_name=field, domain_name=ds.periSwitch(n))
        else:
            if ds.hydroSwitch(n) != "":
                arcpy.AssignDomainToField_management(in_table=lyr, field_name=field, domain_name=ds.hydroSwitch(n))
        if n in imgDomains:
            if n == imgDomains[0]:
                arcpy.AssignDomainToField_management(in_table=lyr, field_name=field, domain_name="IMG_SET")
            else:
                arcpy.AssignDomainToField_management(in_table=lyr, field_name=field, domain_name="IMG_NUM")
    return
