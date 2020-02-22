"""
Title: 		Batch_Rename_FeatureClasses.py
Purpose: 	Find and Replace String of Feature Classes. Ex: rename all features w/ suffix "_01"
Author: 	Stephen Morgan
"""

import arcpy
import os

# Get parameters from tool inputs
gdb = arcpy.GetParameterAsText(0)
search_for = arcpy.GetParameterAsText(1)
replace_with = arcpy.GetParameterAsText(2)


def main():
    # crawl gdb looking for features
    walk = arcpy.da.Walk(gdb, datatype="FeatureClass")
    for root, dirs, files in walk:
        rename = (name for name in files if search_for in name)
        for fc in rename:
            arcpy.AddMessage("Replacing '{0}' by '{1}'".format(
                fc, fc.replace(search_for, replace_with)))
            arcpy.Rename_management(os.path.join(root, fc),
                                    os.path.join(root, fc.replace(search_for, replace_with)))


if __name__ == '__main__':
    main()
