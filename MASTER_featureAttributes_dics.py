# -*- coding: utf-8 -*-
"""
Name: featureAttributes_dicSwitch
Purpose: Contains all of the dictionaries required by featureAttributes_functions.py
Author: rparker
Created: 30-01-2018
"""


def periSwitch(x):
    return {
        "TYPE": "PERI_TYPE",
        "SUBTYPE": "PERI_SUBTYPE",
        "IND_MUL": "IND_MUL"
    }.get(x, "")


def massSwitch(x):
    return {
        "TYPE": "MASS_TYPE",
        "SUBTYPE": "MASS_SUBTYPE",
        "SUBTYPE_DESC": "MASS_SUBTYPE_DESC",
        "MATERIAL": "MASS_MATERIAL",
        "ACTIVITY": "MASS_ACTIVITY",
        "IND_MUL": "IND_MUL"
    }.get(x, "")


def hydroSwitch(x):
    return {
        "TYPE": "HYDRO_TYPE",
        "SUBTYPE": "HYDRO_SUBTYPE",
        "ORIENTED": "HYDRO_ORIENT",
        "IND_MUL": "IND_MUL"
    }.get(x, "")


def addInfoDic(x):
    return {
        "PHYSIOGRAPHIC_POLY_250K": "PHY_UNIT",
        "pfIceContent_1M_canada_poly": "COMBUNIT",
        "nts_snrc_50k": "NTS_SNRC",
        "surficialGeology_1647A": "UTYPE_DID",
        "surficialGeology_1745A": "ULABEL1_DID",
        "surficialGeology_1746A": "ULABEL1_DID",
        "surficialGeology_yukon": "ULABEL1_DID",
        "mappingReferenceGrid": "GRID_NUM",
        "pfMapOfCanada_wedgeIce": "LEGEND",
        "pfMapOfCanada_relicIce": "LEGEND",
        "pfMapOfCanada_segregatedIce": "LEGEND",
        "maxGlacialLimit": "GLACIATED"
    }.get(x, "")


def fNameDic(x):
    return {
        "PHYSIOGRAPHIC_POLY_250K": "PHYS_REG",
        "pfIceContent_1M_canada_poly": "PF_CODE",
        "nts_snrc_50k": "NTS_50K",
        "surficialGeology_1647A": "SURF_GEO1",
        "surficialGeology_1745A": "SURF_GEO2",
        "surficialGeology_1746A": "SURF_GEO3",
        "surficialGeology_yukon": "SURF_GEO4",
        "mappingReferenceGrid": "NTS_SUBCELL",
        "pfMapOfCanada_wedgeIce": "WEDGE_ICE",
        "pfMapOfCanada_relicIce": "RELIC_ICE",
        "pfMapOfCanada_segregatedIce": "SEG_ICE",
        "maxGlacialLimit": "GLACIATED"
    }.get(x, "")


def imgNameDic(x):
    return {
        "SOURCE": "IMG_SOURCE_ALL",
        "IMG_SET": "IMG_SET_ALL",
        "IMG_NUM": "IMG_NUM_ALL",
        "DATE": "IMG_DATE_ALL"
    }.get(x, "")


def indMulDic(x):
    return {
        "IND": "Individual",
        "MUL": "Multiple",
        "NA": "Not Applicable",
        "UN": "Unclassified"
    }.get(x, "")


def imgSetDic(x):
    return {
        "3010": "056177773010",
        "3020": "056177773020",
        "3030": "056177773030",
        "3040": "056177773040",
        "3050": "056177773050",
        "3060": "056177773060",
        "7010": "057680547010",
        "7020": "057680547020",
        "7040": "057680547040",
        "7050": "057680547050",
        "7080": "057680547080",
        "7090": "057680547090",
        "7100": "057680547100",
        "7110": "057680547110",
        "7130": "057680547130",
        "7140": "057680547140",
        "7160": "057680547160",
        "11020": "058706911020",
        "11030": "058706911030",
        "11040": "058706911040",
        "11050": "058706911050",
        "11060": "058706911060",
        "11070": "058706911070",
        "11080": "058706911080",
        "11090": "058706911090",
        "1100": "058706911100",
        "1110": "058706911110",
        "1120": "058706911120",
        "33010": "058878233010",
        "33020": "058878233020",
        "33030": "058878233030"
    }.get(x, "")


def actDic(x):
    return {
        "ACT": "Active",
        "INACT": "Inactive",
        "UN": "Unclassified"
    }.get(x, "")


def orientDic(x):
    return {
        "Y": "Yes",
        "N": "No",
        "NA": "Not Applicable",
        "UN": "Unclassified"
    }.get(x, "")


def mTypeDic(x):
    return {
        "FL": "Flow",
        "SL": "Slide",
        "FA": "Fall",
        "TO": "Topple",
        "CX": "Complex",
        "UN": "Unclassified"
    }.get(x, "")


def pTypeDic(x):
    return {
        "PALSA": "Palsa",
        "LITH": "Lithalsa",
        "PINGO": "Pingo",
        "MOUND": "Mounds - Badlands",
        "POLY": "Ice Wedge Polygon",
        "SNF": "String / Net Fen",
        "PEATP": "Peat Plateau Complex",
        "UN": "Unclassified"
    }.get(x, "")


def hTypeDic(x):
    return {
        "TG": "Thermokarst Gully",
        "BS": "Beaded Stream",
        "DLB": "Drained Lake Basin",
        "ICE": "Icing",
        "TL": "Lake/Pond Affected by Thermokarst",
        "UN": "Unclassified"
    }.get(x, "")


def mSubtypeDic(x):
    return {
        "ALD": "Active-layer Detachment (skin flow)",
        "RTS": "Retrogressive Thaw Slump",
        "DF": "Debris Flow / Fan",
        "SO": "Solifluction",
        "RG": "Rock Glacier",
        "RS": "Rotational Slide",
        "TS": "Translational Slide",
        "SS": "Shoreline Slump",
        "BF": "Block Failure",
        "UN": "Unclassified"
    }.get(x, "")


def mSubtypeDescDic(x):
    return {
        "LO": "Lobes",
        "TE": "Terraces",
        "SH": "Sheet (Stripes)",
        "NA": "Not Applicable",
        "UN": "Unclassified"
    }.get(x, "")


def mMaterialDic(x):
    return {
        "Q": "Unconsolidated Sediments",
        "R": "Bedrock",
        "UN": "Unclassified"
    }.get(x, "")


def pSubtypeDic(x):
    return {
        "HIGH": "High Centre",
        "LOW": "Low Centre",
        "UNDIF": "Undifferentiated",
        "NA": "Not Applicable",
        "UN": "Unclassified"
    }.get(x, "")


def hSubtypeDic(x):
    return {
        "FULL": "Fully Drained",
        "PART": "Partially Drained",
        "NA": "Not Applicable",
        "UN": "Unclassified"
    }.get(x, "")


def massAttributeOrder(x):
    return {
        "LAT": 1,
        "LONG": 2,
        "NTS_50K": 3,
        "CLASS": 4,
        "TYPE": 5,
        "TYPE_CODE": 6,
        "SUBTYPE": 7,
        "SUBTYPE_CODE": 8,
        "SUBTYPE_DESC": 9,
        "SUBTYPE_DESC_CODE": 10,
        "DESC_CODE": 11,
        "IND_MUL": 12,
        "IND_MUL_CODE": 13,
        "ACTIVITY": 14,
        "ACTIVITY_CODE": 15,
        "MATERIAL": 16,
        "MATERIAL_CODE": 17,
        "AREA_HA": 18,
        "COMMENTS": 19,
        "TEST_SITE": 20,
        "SURGEOL_DESC": 21,
        "SURF_GEO": 22,
        "PHYS_REG": 26,
        "PF_DESC": 28,
        "PF_CODE": 29,
        "IMG_SET_IN": 31,
        "IMG_NUM_IN": 32,
        "IMG_SOURCE": 33,
        "IMG_DATE": 34,
        "WEDGE_ICE": 35,
        "RELIC_ICE": 36,
        "SEG_ICE": 37,
        "GLACIATED": 38
    }.get(x, "")


def periAttributeOrder(x):
    return {
        "LAT": 1,
        "LONG": 2,
        "NTS_50K": 3,
        "CLASS": 4,
        "TYPE": 5,
        "TYPE_CODE": 6,
        "SUBTYPE": 7,
        "SUBTYPE_CODE": 8,
        "IND_MUL": 9,
        "AREA_HA": 10,
        "COMMENTS": 11,
        "TEST_SITE": 12,
        "SURGEOL_DESC": 13,
        "SURF_GEO": 14,
        "PHYS_REG": 18,
        "PF_DESC": 20,
        "PF_CODE": 21,
        "IMG_SET_IN": 23,
        "IMG_NUM_IN": 24,
        "IMG_SOURCE": 25,
        "IMG_DATE": 26,
        "WEDGE_ICE": 27,
        "RELIC_ICE": 28,
        "SEG_ICE": 29,
        "GLACIATED": 30
    }.get(x, "")


def hydroAttributeOrder(x):
    return {
        "LAT": 1,
        "LONG": 2,
        "NTS_50K": 3,
        "CLASS": 4,
        "TYPE": 5,
        "TYPE_CODE": 6,
        "SUBTYPE": 7,
        "SUBTYPE_CODE": 8,
        "IND_MUL": 9,
        "ORIENTED": 10,
        "AREA_HA": 11,
        "COMMENTS": 12,
        "TEST_SITE": 13,
        "SURGEOL_DESC": 14,
        "SURF_GEO": 15,
        "PHYS_REG": 19,
        "PF_DESC": 21,
        "PF_CODE": 22,
        "IMG_SET_IN": 24,
        "IMG_NUM_IN": 25,
        "IMG_SOURCE": 26,
        "IMG_DATE": 27,
        "WEDGE_ICE": 28,
        "RELIC_ICE": 29,
        "SEG_ICE": 30,
        "GLACIATED": 31
    }.get(x, "")
