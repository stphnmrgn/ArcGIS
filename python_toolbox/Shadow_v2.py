"""
Title:        	Shadow_v2.py
Purpose:     	Process for creating building shadows
Description: 	Generates a building shadow feature based on building height
Author:      	Stephen Morgan, GISP
"""

import arcpy
import os
import math

arcpy.env.overwriteOutput = True

buildings = arcpy.GetParameterAsText(0)
shadows = arcpy.GetParameterAsText(1)
# Must be in the same units as the coordinate system!
floorfield = arcpy.GetParameterAsText(2)
try:
    azimuth = float(arcpy.GetParameterAsText(3))
except:
    azimuth = 200  # default
try:
    altitude = float(arcpy.GetParameterAsText(4))
except:
    altitude = 35  # default
try:
    unit = arcpy.GetParameterAsText(5)
except:
    unit = "Meters"  # default

shapefield = arcpy.Describe(buildings).shapeFieldName

# Output
#result = arcpy.CreateFeatureclass_management(os.path.dirname(shadows),os.path.basename(shadows),'POLYGON')
inscur = arcpy.InsertCursor(shadows)

# Compute the shadow offsets
# outside loop as it only needs calculating once
spread = 1 / math.tan(altitude)

# Get Floor Height
if unit == "Feet":
    floorHeight = 10
else:
    floorHeight = 3.2

for row in arcpy.SearchCursor(buildings):
    shape = row.getValue(shapefield)
    height = row.getValue(floorfield)
    # Get shadow height
    if height == None:
        height = 2.0 * floorHeight
    else:
        height = float(row.getValue(floorfield)) * floorHeight
    # Compute the shadow offsets
    x = -height * spread * math.sin(azimuth)
    y = -height * spread * math.cos(azimuth)
    # Clone the original shape
    clone = arcpy.CopyFeatures_management(shape, arcpy.Geometry())[0]
    # Adjoin the wall shadows
    for part in shape:
        for i, j in enumerate(range(1, part.count)):
            """This will fail if the scripts comes across a polygon with
            inner rings, to handle this case you'll need to test that each 
            point is not None."""
            pnt0 = part[i]
            pnt1 = part[j]
            if pnt1 is None:
                break  # don't get nice shadows from the inner walls.
            pnt0offset = arcpy.Point(pnt0.X + x, pnt0.Y + y)
            pnt1offset = arcpy.Point(pnt1.X + x, pnt1.Y + y)
            arr = arcpy.Array([pnt0, pnt1, pnt1offset, pnt0offset, pnt0])
            clone = arcpy.Union_analysis(
                [arcpy.Polygon(arr), clone], arcpy.Geometry())
            clone = arcpy.Dissolve_management(clone, arcpy.Geometry())[0]
    newrow = inscur.newRow()
    newrow.shape = clone
    inscur.insertRow(newrow)
    del newrow, clone, arr, pnt0, pnt0offset, pnt1, pnt1offset

del inscur
