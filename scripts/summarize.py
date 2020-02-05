# Description: Use SummarizeWithin to summarize the crimes in each city neighborhood

# import system modules 
import arcpy


# # Set environment settings
arcpy.env.workspace = 'C:\Users\yourdata\created\'

#  Set local variables
polys = 'C:\Users\yourdata\tl_2018_us_county.shp'
points = 'defrauded_pts.shp'
outFeatureClass = 'aggregated_us_county2.shp'
keepAll = 'KEEP_ALL'
sumFields = [['S_AT_RISK', 'SUM'], ['S_LOST', 'SUM'], ['COUNT', 'SUM'], ['S_RECOVERE', 'SUM'], ['S_PROTECTE', 'SUM'], ['S_RETRO_AT', 'SUM'], ['S_RETRO_LO', 'SUM'], ['S_RETRO_RE', 'SUM'], ['S_RETRO_PR', 'SUM']]
addShapeSum = 'ADD_SHAPE_SUM'
# groupField = 'Crime_type'
# addMinMaj = 'ADD_MIN_MAJ'
# addPercents = 'ADD_PERCENT'
# outTable = 'crimes_aggregated_groups'


# arcpy.SummarizeWithin()
# arcpy.SummarizeWithin_analysis(polys, points, outFeatureClass, keepAll, 
#                                sumFields, addShapeSum)
