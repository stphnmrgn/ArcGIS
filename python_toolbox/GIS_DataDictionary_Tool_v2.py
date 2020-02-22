'''
Title:        	GIS_DataDictionary_Tool_v2.py
Purpose:     	Process for extracting information from features within a gdb
Description: 	This script will return feature descriptions and then write them in a .csv file.
		        User needs to input pathway of a geodatabase and the pathway +"\nameyourcsv.csv". 
		        Output includes the following:
			Feature Dataset, Feature Class Name, Shape Type, Feature Description, 
			Spatial Reference, Editor, Workspace, and Populated
Author:      	Stephen Morgan, GISP, AECOM
Created:     	09/24/2017
'''

#Import modules
import arcpy, sys, os, csv
from arcpy import env

print "Enter geodatabase path:"
#workspace = raw_input()
workspace = sys.argv[1]
print os.path.dirname(workspace)

fullname = os.path.basename(workspace) #Return base name of pathway (name of folder). Set variable to path and name of folder
name = fullname.strip(".gdb") #Strip off GDB file extension and store as string variable for the 'path_csv'
print name

path_csv = os.path.dirname(workspace) + os.sep + name + ".csv" #Store folder name as string variable for the 'path_csv'

#Set env.workspace to user's workspace
env.workspace = workspace

#Create a list of feature classes and datasets
fcList = arcpy.ListFeatureClasses()
datasetList = arcpy.ListDatasets('*','Feature')

#Loop through feature classes in fcList and print
for fc in fcList:
    print fc
#Loop through datasets and its features and print
for dataset in datasetList:
    print dataset
    #Input dataset as an argument for ListFeatureClasses function,
    #creating list of dataset feature classes
    setList = arcpy.ListFeatureClasses("*","",dataset)
    for fc in setList:
        print fc

#Open a new csv file using "path_csv"
with open(path_csv, 'ab') as f:
    writer = csv.writer(f) #Start writing
    #Set a variable to include the column headers of the csv 
    header = ("Feature_Dataset", "Feature_Class", "Shape_Type", "Feature_Description", "Spatial_Reference", "Editor", "Workspace", "Populated")
    writer.writerow(header)
    #Loop through feature classes
    for fc in fcList:
        desc = arcpy.Describe(fc) #Create describe objects of features
        sr = desc.spatialReference.name #Return spatial reference
        st = desc.shapeType #Return geometry shape
        dt = desc.dataType #Return dataType object so that Editor Tracking objects can be returned
        #If feature class has editor tracker enabled, then return editorFieldName
        if desc.editorTrackingEnabled:
            who = desc.editorFieldName
            #Use a cursor to search through editorFieldName of all features
            #and create a dictionary of the user's name
            userDictionary = {}
            cur = arcpy.da.SearchCursor(fc, [who])
            for row in cur:
                featureEditedBy = row[0]
                if featureEditedBy in userDictionary:
                    userDictionary[featureEditedBy] += 1
                else:
                    userDictionary[featureEditedBy] = 1
            for user in list(userDictionary.keys()):
                #If editor tracking is on and editorFieldName is None (no data),
                #then user is set to "Null", else the field is set to the user's name
                if user == None:
                    who = "Null"
                else:
                    who = user
        #If editor tracker is not enabled, then write that
        else:
            who = ("Editor tracker not enabled")
        #If feature count of first attribute field = zero then
        #feature is not populated, else the feature is populated
        if arcpy.management.GetCount(fc)[0] == "0":
            pop = "No"
        else:
            pop = "Yes"
        #Create Describe object of gdb from user's workspace, return gdb name
        desc = arcpy.Describe(workspace)
        gdb = desc.name
        #Write returned objects into columns (not rows) by using a [list]
        writer.writerow(['"Not in Feature Dataset"', fc, st, '"Feature Description"', sr, who, gdb, pop])
    #Same, except for features within a dataset
    for dataset in datasetList:
        setList = arcpy.ListFeatureClasses("*","",dataset)
        for fc in setList:
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
            if arcpy.management.GetCount(fc)[0] == "0":
                pop = "No"
            else:
                pop = "Yes"
            desc = arcpy.Describe(workspace)
            gdb = desc.name
            writer.writerow([dataset, fc, st, '"Feature Description"', sr, who, gdb, pop])

#This gives feedback in the script tool dialog:
arcpy.GetMessages()

print "Spam and Eggs are Well Done"
