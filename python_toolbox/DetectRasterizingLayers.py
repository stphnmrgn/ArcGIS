'''
Title: 		DetectRasterizingLayers.py
Purpose: 	Execute this arcpy.mapping script in the Python Window of ArcMap
          to report any layers in your map that may be causing rasterization
          during printing or exporting
Author: 	Stephen Morgan
Created: 	09/26/2017
'''

# Import modules
import arcpy


def DetectRasterization():
    mxd = arcpy.mapping.MapDocument("CURRENT")
    df_list = arcpy.mapping.ListDataFrames(mxd)
    foundRasterization = False
    noneFoundMsg = "No rasterizing layers were detected."
    for df in df_list:
        lyr_list = arcpy.mapping.ListLayers(mxd, data_frame=df)
        for lyr in lyr_list:
            if lyr.isRasterizingLayer or lyr.supports("BRIGHTNESS"):
                foundRasterization = True
                if lyr.isGroupLayer and lyr.transparency > 0:
                    print "In data frame '" + df.name + "', the group layer '" + \
                        lyr.longName + "' is a rasterizing layer:\r",
                    print "\tVisibility is " + str(lyr.visible) + ".\n" + \
                          "\tTransparency is " + \
                        str(lyr.transparency) + " percent.\n"
                elif not lyr.isGroupLayer:
                    print "In data frame '" + df.name + "', the layer '" + \
                        lyr.longName + "' is a rasterizing layer:\r",
                    if lyr.transparency > 0:
                        print "\tVisibility is " + str(lyr.visible) + ".\n" + \
                              "\tTransparency is " + \
                            str(lyr.transparency) + " percent.\n"
                    else:
                        print "\tVisibility is " + str(lyr.visible) + ".\n" + \
                              "\tTransparency is 0 percent, but the layer may be a\n" + \
                              "\traster layer or contain rasterizing symbology such\n" + \
                              "\tas bitmap picture symbols.\n"
            del lyr
        del lyr_list
        del df
    if not foundRasterization:
        print noneFoundMsg
    del df_list
    del mxd
