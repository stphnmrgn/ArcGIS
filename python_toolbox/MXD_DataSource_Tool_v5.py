"""
Title: 			MXD_DataSource_v5.py
Purpose: 		List data in MXDs and write to a .csv file
Description: 	For every MXD in a folder, this script will write the following information
				MXD Name, MXD pathway, Layer Name, and Layer Data Source
Author: 		Stephen Morgan
"""

# Import modules; sys to get raw inputs and os to use path separator
import arcpy
import sys
import os
import csv

print "Enter folder path:"
# workspace = raw_input(). Include line below for ArcToolbox
workspace = sys.argv[1]
print os.path.dirname(workspace)

"""Return the base name of the pathway (name of folder). 
Set variable to path and name of folder"""
fullname = os.path.basename(workspace)
print fullname

# Store folder name as string variable for the 'path_csv'
path_csv = os.path.dirname(workspace) + os.sep + fullname + ".csv"

# Setup the CSV file


def main(folder, outputfile):
    with open(outputfile, "wb") as f:
        w = csv.writer(f)  # Start writing
        # Set a variable to include the column headers of the csv
        header = ("Map_Document", "MXD_Path", "Layer_Name",
                  "Layer_Data_Source", "Broken_Link", "Relative_Path_Set")
        w.writerow(header)
        rows = crawlmxds(folder)
        w.writerows(rows)

# Define crawlmxd function


def crawlmxds(folder):
    for root, dirs, files in os.walk(folder):
        for f in files:
            # Crawl folder for files with .mxd extension
            if f.lower().endswith(".mxd"):
                # Return MXD names
                mxdName = os.path.splitext(f)[0]
                # Return MXD pathways
                mxdPath = os.path.join(root, f)
                # Return MXD properties
                mxd = arcpy.mapping.MapDocument(mxdPath)
                # Check if MXDs have relative pathway checked
                if mxd.relativePaths == True:
                    relativePath = "Yes"
                else:
                    relativePath = "No"
                # Return list of layers for MXDs
                layers = arcpy.mapping.ListLayers(mxd, "")
                for lyr in layers:  # Loop layers in MXDs
                    print lyr
                    lyrName = lyr.name
                    # Return data source/pathway for layers in MXD
                    lyrDatasource = lyr.dataSource if lyr.supports(
                        "dataSource") else "N/A"
                    # Return list of broken layers/data sources
                    brknList = arcpy.mapping.ListBrokenDataSources(mxd)
                    # Variable "BrokenLink" is assigned here to avoid local variable error
                    BrokenLink = None
                    # Loop broken layers in MXDs
                    for brknItem in brknList:
                        print brknItem.name
                        brknName = brknItem.name
                        # Return data source/pathway for each broken data layer
                        DataSource = brknItem.dataSource
                        #"BrokenLink" is local variable here
                        # Matching data sources of broken data sources with regular data sources
                        if lyrDatasource == DataSource:
                            BrokenLink = "Yes"
                    # Put all these variables in order for the .csv file
                    seq = (mxdName, mxdPath, lyrName,
                           lyrDatasource, BrokenLink, relativePath)
                    yield seq
                del mxd


if __name__ == "__main__":
    folderPath = workspace  # or arcpy.GetParameterAsText(0)
    output = path_csv  # or arcpy.GetParameterAsText(1)
    main(folderPath, output)

# This gives feedback in the script tool dialog:
arcpy.GetMessages()

print "Spam and Eggs are Done"
