# -*- coding: utf-8 -*-
"""
Title: 		    mxd_sourcedata_CSV.py

Purpose: 	    List data in MXDs and write to a .csv file

Description:    This script will output a csv file indicating the pathways
                of all features within MXDs in a given folder. User inputs 
                pathway to map folder.

Type:           Standalone script

Author:         Stephen Morgan, GISP

Python:         2.7.8
"""

# Import modules
import os
import csv
from arcpy import mapping


########################## USER INPUTS ##########################

# Get user's map folder pathway
workspace = input('Type/paste the full pathway to your maps folder, and then press Enter.'
                  ' \nExample, r"C:Project\GIS\Maps": ')

########################## USER INPUTS ##########################

fullname = os.path.basename(workspace)
# Store folder name as string
path_csv = os.path.dirname(workspace) + os.sep + fullname + "_mxdsourcedata.csv"

print "\nYour map directory: \n" + os.path.dirname(workspace)
# arcpy.AddMessage("\nYour map directory: \n" + os.path.dirname(workspace))
print "\nThe name of your map folder: \n" + fullname
# arcpy.AddMessage("\nThe name of your map folder: \n" + fullname)
print "\nThe path of csv we're creating: \n" + path_csv
# arcpy.AddMessage("\nThe path of csv we're creating: \n" + path_csv)


def csv_template(folder, outputfile):
    """
    Given a folder path, create a csv template.

    Parameters
    ----------
    folder: string
            folder pathway

    outputfile: string
            pathway & filename

    Returns
    -------
    result: template csv file saved using the user specified file name
    and folder destination.
    """

    with open(outputfile, "wb") as f:
        print "\nCreating template csv file...\n" # or arcpy.AddMessage("Creating template csv file...")
        w = csv.writer(f)
        # Set variable to include column headers of the csv
        header = ("Map_Document", "MXD_Path", "Layer_Name", "Layer_Data_Source")
        w.writerow(header)
        rows = mxd_data_source(folder)
        w.writerows(rows)


def mxd_data_source(folder):
    """
    Given a folder path, search folder directory for mxd files.

    Parameters
    ----------
    folder: string, folder pathway

    Returns
    -------
    result: A sequence of feature class information to store in csv file. For each
    mxd file found, the following information is stored:
    
        map name: string
        map pathway: string
        map feature layer: string
        feature layer pathway: string
    """

    print "\nChecking data sources of each MXD...\n"
    for root, dirs, files in os.walk(folderPath):
        for f in files:
            # Crawl folder for files with .mxd extention
            if f.lower().endswith(".mxd"):
                # Return MXD names and pathways
                mxdName = os.path.splitext(f)[0]
                mxdPath = os.path.join(root, f)
                print "     Checking MXD titled: " + mxdName

                # Return MXD properties
                mxd = mapping.MapDocument(mxdPath)
                # Return list of layers for MXDs
                layers = mapping.ListLayers(mxd, "")
                # Loop layers in MXDs
                for lyr in layers:
                    lyrName = lyr.name
                    # Return data source/pathway for each layer in MXD
                    lyrDatasource = lyr.dataSource if lyr.supports("dataSource") else "N/A"
                    # Put all these variables in order for the .csv file
                    seq = (mxdName, mxdPath, lyrName, lyrDatasource)
                    yield seq
                del mxd


if __name__ == "__main__":
    folderPath = workspace      # or arcpy.GetParameterAsText(0)
    output = path_csv           # or arcpy.GetParameterAsText(1)
    csv_template(folderPath, output)


print "\nSpam and Eggs are Done\n"

