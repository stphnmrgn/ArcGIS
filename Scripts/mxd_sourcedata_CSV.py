# -*- coding: utf-8 -*-
"""
Title: 		    mxd_sourcedata_CSV.py

Purpose: 	    List data in MXDs and write to a .csv file

Description:        This script will output a csv file indicating the pathways
                    of all features within MXDs in a given folder.
                    User inputs pathway to map folder.
                    
Type: 		    Standalone script

Author: 	    C_lupus_rufus, GISP

Created: 	    09/26/2017
Updated:            03/08/2019

Version:            Python 2.7.8
"""

# Import modules
import os
import csv
from arcpy import mapping


# Get user's map folder pathway
workspace = input('Type/paste the full pathway to your maps folder, and then press Enter.'
                  ' \nExample, r"C:Project\GIS\Maps": ')

print "\nYour map directory: \n" + os.path.dirname(workspace)
# arcpy.AddMessage("\nYour map directory: \n" + os.path.dirname(workspace))

# Return base name of pathway (name of folder)
fullname = os.path.basename(workspace)
print "\nThe name of your map folder: \n" + fullname
# arcpy.AddMessage("\nThe name of your map folder: \n" + fullname)

# Store folder name as string variable for the 'path_csv'
path_csv = os.path.dirname(workspace) + os.sep + \
    fullname + "_mxdsourcedata.csv"
print "\nThe path of csv we're creating: \n" + path_csv
# arcpy.AddMessage("\nThe path of csv we're creating: \n" + path_csv)


# Setup the CSV file
def csv_template(folder, outputfile):
    """
    Given a folder path, create a csv template.

    Parameters
    ----------
    a: string
        a folder pathway
    b: string
        a pathway & filename

    Returns
    -------
    result: a template csv file saved using the user specified file name
    and folder destination.

    """

    with open(outputfile, "wb") as f:
        print "\nCreating template csv file...\n"
        # arcpy.AddMessage("Creating template csv file...")
        w = csv.writer(f)
        # Set variable to include column headers of the csv
        header = ("Map_Document", "MXD_Path", "Layer_Name", "Layer_Data_Source")
        w.writerow(header)
        rows = crawlmxds(folder)
        w.writerows(rows)


def crawlmxds(folder):
    """
    Given a folder path, search folder directory for mxd files.

    Parameters
    ----------
    a: string
        a folder pathway

    Returns
    -------
    result: A sequence of feature class information to store in csv file. For each
    mxd file found, the following information is stored:
    
        map name, string
        map pathway, string
        map feature layer, string
        feature layer pathway, string

    """

    print "\nChecking data sources of each MXD...\n"
    # arcpy.AddMessage("Checking data sources of each MXD...")
    for root, dirs, files in os.walk(folderPath):
        for f in files:
            # Crawl folder for files with .mxd extention
            if f.lower().endswith(".mxd"):
                # Return MXD names and pathways
                mxdName = os.path.splitext(f)[0]
                mxdPath = os.path.join(root, f)
                print "     Checking MXD titled: " + mxdName
                # arcpy.AddMessage("\nChecking MXD titled: " + mxdName)
                
                # Return MXD properties
                mxd = mapping.MapDocument(mxdPath)

                # Return list of layers for MXDs
                layers = mapping.ListLayers(mxd, "")
                # Loop layers in MXDs
                for lyr in layers:
                    lyrName = lyr.name
                    # Return data source/pathway for each layer in MXD
                    lyrDatasource = lyr.dataSource if lyr.supports(
                        "dataSource") else "N/A"
                    # Put all these variables in order for the .csv file
                    seq = (mxdName, mxdPath, lyrName, lyrDatasource)
                    yield seq
                del mxd


if __name__ == "__main__":
    folderPath = workspace
    # arcpy.GetParameterAsText(0)
    output = path_csv
    # arcpy.GetParameterAsText(1)
    csv_template(folderPath, output)


print "\nSpam and Eggs are Done\n"

