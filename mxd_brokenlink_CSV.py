# -*- coding: utf-8 -*-
"""
Title:          mxd_brokenlink_CSV.py
Python:         2.7.8
Purpose:        List broken data sources in MXDs and write to a .csv file
Description: 	This script will output a csv file indicating the layers
                with broken data sources within MXDs in a given folder.
                User inputs pathway to map folder.
Type:           Standalone script
Author:         Stephen Morgan, GISP
Date Created: 	09/26/2017
"""

# Import modules
import os
import csv
from arcpy import mapping
import time


# Get user's map folder pathway
workspace = input('Type/paste the full pathway to your maps folder, and then press Enter.'
                  ' \nExample, r"C:Project\GIS\Maps": ')

fullname = os.path.basename(workspace) # Return base name of pathway (name of folder)
path_csv = os.path.dirname(workspace) + os.sep + fullname + "_mxdbrokenlinks.csv" # Store folder name as string

print "\nYour map directory: \n" + os.path.dirname(workspace)
print "\nThe name of your map folder: \n" + fullname
print "\nThe path of csv we're creating: \n" + path_csv


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
        print "\nCreating template csv file...\n"
        w = csv.writer(f)
        # Set variable to include the column headers of the csv
        header = ("Map_Document", "Broken_Layer", "Layer_Data_Source")
        w.writerow(header)
        rows = mxd_broken_links(folder)
        w.writerows(rows)


def mxd_broken_links(folder):
    """
    Given a folder path, search folder directory for mxd files.

    Parameters
    ----------
    folder: string
            folder pathway

    Returns
    -------
    result: A sequence of feature class information to store in csv file. For each
    broken layer found within a MXD file, the following information is stored:
    
        map name: string
        broken layer: string
        broken layer data path: string
    """

    for root, dirs, files in os.walk(folderPath):
        for fileName in files:
            # Crawl folder for files with .mxd extention
            if fileName.lower().endswith(".mxd"):
                # Return MXD pathways
                fullPath = os.path.join(root, fileName)
                # Return MXD properties
                mxd = mapping.MapDocument(fullPath)
                print "\nChecking MXD: " + fileName

                # Loop broken layers in MXDs, returning a list
                brokenlinks = mapping.ListBrokenDataSources(mxd)
                if brokenlinks == None:
                    fileName = "No broken links were found"
                    linkname = "No broken links were found"
                    DataSource = "No broken links were found"
                    seq = (fileName, linkname, DataSource)
                    yield seq
                else:
                    for brokenlink in brokenlinks:
                        print "Broken Data Link: " + brokenlink.name
                        linkname = brokenlink.name
                        DataSource = brokenlink.dataSource
                        seq = (fileName, linkname, DataSource)
                        yield seq
                del mxd
                
            else:
                #fileName = "No MXDs were found in folder"
                linkname = "File is not a MXD"
                DataSource = os.path.join(root, fileName)
                seq = (fileName, linkname, DataSource)
                yield seq
                print "\nFile(s) is not a MXD: " + fileName


if __name__ == "__main__":
    folderPath = workspace      # or arcpy.GetParameterAsText(0)
    output = path_csv           # or arcpy.GetParameterAsText(1)
    csv_template(folderPath, output)

time.sleep(6)

print "\nSpam and Eggs are Done\n"
