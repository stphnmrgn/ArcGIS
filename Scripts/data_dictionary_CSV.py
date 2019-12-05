# -*- coding: utf-8 -*-
"""
Title:         	data_dictionary_CSV.py
Python:         2.7.8
Purpose:     	Process for extracting information of features in a gdb
Description: 	This script will return feature descriptions and then write 
                them in a .csv file. User needs to input pathway of a 
                geodatabase. Output includes the following: Feature Dataset, 
                Feature Class Name, Shape Type, Spatial Reference, Editor, 
                Workspace, and Populated
Type: 		    Standalone script
Author:      	Stephen Morgan, GISP
Date Created:   09/24/2017
"""

# Import modules
import os
import csv
import arcpy
from arcpy import env


# Get user's workspace
workspace = input('Type/paste the full pathway to your GDB folder, and then press Enter.'
                   ' \nExample, r"C:Project\GIS\MyData.gdb": ')

# Set env.workspace to user's workspace
env.workspace = workspace

# Return base name of pathway (name of folder)
fullname = os.path.basename(workspace)

# Strip extension off workspace name
name = fullname.strip(".gdb")

# Store folder name as string variable for the 'path_csv'
path_csv = os.path.dirname(workspace) + os.sep + \
     name + "_datadictionary.csv"

print "\nYour geodatabase directory: \n" + os.path.dirname(workspace)
print "\nThe name of your workspace: \n" + fullname
print "\nThe path to the csv we're creating: \n" + path_csv


# Setup the CSV file
def main(folder, outputfile):
     with open(outputfile, "ab") as f:
         # Start writing
         w = csv.writer(f)
         # Set variable to include column headers of the csv
         header = ("Feature_Dataset", "Feature_Class", "Shape_Type", "Populated", 
                    "Feature_Count", "Workspace", "Spatial_Reference", "Editor")
                    
         w.writerow(header)
         rows = describe(folder)
         w.writerows(rows)


def describe(folder):
     print "\nReading & Writing Feature Descriptions... \n"

     # Create a list of feature classes and datasets
     fcList = arcpy.ListFeatureClasses()
     datasetList = arcpy.ListDatasets('*', 'Feature')

     # Loop through feature classes
     for fc in fcList:
         print "    feature: " + fc
         
         # return specific describe objects to write to csv
         desc = arcpy.Describe(fc)
         sr = desc.spatialReference.name
         st = desc.shapeType
         # Return dataType object so Editor Tracking objects can be returned
         dt = desc.dataType
            
         # If feature class has editor tracker enabled, return editorFieldName
         if desc.editorTrackingEnabled:
             who = desc.editorFieldName
            # Use a cursor to search through editorFieldName of all features
            # and create a dictionary of the user's name
             userDictionary = {}
             cur = arcpy.da.SearchCursor(fc, [who])

             for row in cur:
                 featureEditedBy = row[0]
                 if featureEditedBy in userDictionary:
                     userDictionary[featureEditedBy] += 1
                 else:
                     userDictionary[featureEditedBy] = 1

             for user in list(userDictionary.keys()):
                # If editor tracking is on and editorFieldName is None (no data),
                # then user's set to "Null", else field is set to the user's name
                 if user == None:
                    who = "Null"
                 else:
                    who = user
         else:
             who = ("Editor tracker not enabled")

        # If feature count of first attribute field = zero then
        # feature is not populated, else the feature is populated   
        # Get number of features in feature classes first
         fc_count = arcpy.management.GetCount(fc)
         if fc_count[0] == "0":
             pop = "False"
         else:
             pop = "True"

        # Create Describe object of gdb from user's workspace, return gdb name
         desc = arcpy.Describe(workspace)
         gdb = desc.name

        # Put all these variables in order for the .csv file
         seq = ('"Not in Feature Dataset"', fc, st, pop, fc_count, gdb, sr, who)

         yield seq

     # Same, except for features within a dataset
     for dataset in datasetList:
         setList = arcpy.ListFeatureClasses("*", "", dataset)

         for fc in setList:
             print "    feature: " + fc
             desc = arcpy.Describe(fc)
             st = desc.shapeType
             sr = desc.spatialReference.name
             dt = desc.dataType

             if desc.editorTrackingEnabled:
                 who = desc.editorFieldName
                 userDictionary = {}
                 cur = arcpy.da.SearchCursor(fc, [who])

                 for row in cur:
                     featureEditedBy = row[0]
                     if featureEditedBy in userDictionary:
                         userDictionary[featureEditedBy] += 1
                     else:
                         userDictionary[featureEditedBy] = 1

                 for user in list(userDictionary.keys()):
                     if user == None:
                         who = "Null"
                     else:
                         who = user
             else:
                 who = ("Editor tracker not enabled")

             fc_count = arcpy.management.GetCount(fc)
             if fc_count[0] == "0":
                 pop = "False"
             else:
                 pop = "True"

             desc = arcpy.Describe(workspace)
             gdb = desc.name

             seq = (dataset, fc, st, pop, fc_count, gdb, sr, who)

             yield seq


if __name__ == "__main__":
     folderPath = workspace
     output = path_csv
     main(folderPath, output)


print "\nSpam and Eggs are Done\n"
