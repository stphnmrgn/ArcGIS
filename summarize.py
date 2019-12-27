# Description: Use SummarizeWithin to summarize the crimes in each city neighborhood

# import system modules 
import arcpy

# Set environment settings
arcpy.env.workspace = 'C:/data/city.gdb'

#  Set local variables
polys = 'neighborhoods'
points = 'crimes'
outFeatureClass = 'crimes_aggregated'
keepAll = 'KEEP_ALL'
sumFields = [['Damages', 'SUM'], ['VICTIM_AGE', 'MEAN']]
addShapeSum = 'ADD_SHAPE_SUM'
groupField = 'Crime_type'
addMinMaj = 'ADD_MIN_MAJ'
addPercents = 'ADD_PERCENT'
outTable = 'crimes_aggregated_groups'

arcpy.SummarizeWithin_analysis(polys, points, outFeatureClass, keepAll, 
                               sumFields, addShapeSum, '', groupField, 
                               addMinMaj, addPercents, outTable)