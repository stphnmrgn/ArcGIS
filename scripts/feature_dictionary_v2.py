# -*- coding: utf-8 -*-
"""
Title:        	feature_dictionary_v2.py

Purpose:     	Process for extracting information from feature fields to generate
                a data dictionary of the feature attributes

Description: 	This script will return descriptions  of feature fields and then 
                write them to a .csv file. User needs to input pathway of a 
                feature class. Output includes the following: 
                Feature Dataset, Feature Class Name, Shape Type, 
                Spatial Reference, Editor, Workspace, and Populated

Type: 		    Standalone script

Author:      	Stephen Morgan, GISP

Version:        Python 2.7.8
"""

import os
from os.path import dirname
import csv
import arcpy
from arcpy import env



########################## USER INPUTS ##########################

# Get user's workspace
workspace = input('Type/paste the full pathway to your GDB folder, and then press Enter.'
                  ' \nExample, r"C:Project\GIS\MyData.gdb\FeatureClass": ')

########################## USER INPUTS ##########################

env.workspace = workspace

# Return base name of pathway (name of folder)
fullname = os.path.basename(workspace)

# Get directory two folders up from workspace
# two_folders_up = dirname(dirname(workspace))
name = fullname.strip(".gdb") #<<-- commented out, dont want csv in my gdb

# Store folder name as string variable for the 'path_csv'
path_csv = os.path.dirname(workspace) + os.sep + \
    name + "_feature_attribute_dictionary.csv"

print "\nYour geodatabase directory: \n" + os.path.dirname(workspace)
print "\nThe name of your feature: \n" + fullname
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

    with open(outputfile, "ab") as f:
        print "\nCreating template csv file...\n"
         
        w = csv.writer(f)
        # Set variable to include column headers of the csv
        header = ("Field_Name", "Field_Alias", "Field_Value", "Domain", 
                "Null_Values_OK", "Field_Required", "Field_Type", "Length", 
                "Precesion", "Scale")
        w.writerow(header)
        rows = describe(folder)
        w.writerows(rows)


def describe(folder):
    """
    Given a folder path, create a csv template.

    Parameters
    ----------
    folder: string. folder pathway

    outputfile: string. pathway & filename

    Returns
    -------
    result: template csv file saved using the user specified file name
    and folder destination.
    """

    print "\nReading & Writing Feature Field Descriptions... \n"

    # Create a list of feature classes and datasets
    fcList = arcpy.ListFeatureClasses()
    datasetList = arcpy.ListDatasets('*', 'Feature')

    # Loop through feature classes
    for fc in fcList:
        # Create a list of fields
        fields = arcpy.ListFields(fc)
        
        # Loop through feature classes
        for field in fields:
            # return specific describe objects to write to csv
            name = field.name
            alias = field.aliasName
            value = field.defaultValue
            domain = field.domain
            nullable = field.isNullable
            required = field.required
            fieldtype = field.type
            length = field.length
            precesion = field.precision
            scale = field.scale
            # Get number of features in feature classes
            # fc_count = arcpy.management.GetCount(field)
            # # If feature count of first attribute field = zero then
            # # feature is not populated, else the feature is populated
            # if fc_count[0] == "0":
            #     pop = "False"
            # else:
            #     pop = "True"
            # Put all these variables in order for the .csv file
            seq = (name, alias, value, domain, nullable, required, fieldtype, 
                    length, precesion, scale)
            yield seq


if __name__ == "__main__":
    folderPath = workspace
    output = path_csv
    csv_template(folderPath, output)


print "\nSpam and Eggs are Done\n"
