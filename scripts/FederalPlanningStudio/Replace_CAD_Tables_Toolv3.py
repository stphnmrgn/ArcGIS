'''
Title: 		Replace_CAD_Tables_Toolv3.py
Purpose: 	Reads shapefiles/features in a workspace, copies them into a gdb and
				replaces CAD attribute fields with common planning fields.
Type: 		Standalone script
Author: 	Stephen Morgan
Created: 	10/26/2017
'''

import os, arcpy, sys
from arcpy import env

gdb = arcpy.GetParameterAsText(0) #Get parameters from tool

env.workspace = gdb #Set env.workspace to user's workspace

fullname = os.path.basename(gdb) #Get workspace name for GDB creation
outpath = os.path.dirname(gdb) #Get workspace path for GDB creation
name = fullname.strip(".gdb") #Strip extension off workspace name
gdb_update = name + "_Update.gdb" #Set a new workspace name for GDB creation

fcList = arcpy.ListFeatureClasses() #List features of input gdb
datasetList = arcpy.ListDatasets('*','Feature') #List dataset features of input gdb 

output_gdb = arcpy.CreateFileGDB_management(outpath, gdb_update) #Execute CreateFileGDB to hold new features
print "Created Geodatabase"
gdb_update_path = os.path.dirname(gdb) + os.sep + gdb_update #Get the new, full pathway of recently created GDB

def main():
    for fc in fcList:
        out_fc = os.path.join(gdb_update_path, fc) #Create output feature class variable
        desc = arcpy.Describe(fc) #Describe the input fc (need to test the dataset and data types)
        #Make a copy of input features (so we can maintain the original as is)
        if desc.datasetType == "FeatureClass":
            arcpy.CopyFeatures_management(fc, out_fc)
        else:
            arcpy.CopyRows_management(fc, out_fc)
        print "Copied Feature : " + fc
                #Set local parameter for DeleteField tool; CAD fields to delete
        
        cadfields = "Entity;Handle;LyrFrzn;LyrLock;LyrOn;LyrVPFrzn;LyrHandle;Color;EntColor;LyrColor;BlkColor;Linetype;EntLinetyp;LyrLnType;BlkLinetyp;Elevation;Thickness;LineWt;EntLineWt;LyrLineWt;BlkLineWt;RefName;LTScale;ExtX;ExtY;ExtZ;DocName;DocPath;DocType;DocVer"
        try:
            arcpy.DeleteField_management(out_fc, cadfields) #Execute DeleteField to delete all fields except "Layer"
            print "Deleted Fields"
        except:
            print "No Fields to Delete"
            
        #Set local variables for the AddField tool used later
        fieldName1 = "Project_Name"
        fieldName2 = "Project_Number"
        fieldName3 = "Label"
        fieldName4 = "Project_Location"
        fieldName5 = "Phasing"
        #Set local parameters for the AddField tool used later 
        fieldType = "TEXT"
        fieldAlias = None
        fieldLength = 50
        #Execute AddField to add the fields from local variables
        arcpy.AddField_management(out_fc, fieldName1, "TEXT", field_length=fieldLength)
        arcpy.AddField_management(out_fc, fieldName2, "TEXT", field_length=fieldLength)
        arcpy.AddField_management(out_fc, fieldName3, "TEXT", field_length=fieldLength)
        arcpy.AddField_management(out_fc, fieldName4, "TEXT", field_length=fieldLength)
        arcpy.AddField_management(out_fc, fieldName5, "TEXT", field_length=fieldLength)
        print "Added Fields"

if __name__ == '__main__':
    main()

#This gives feedback in the script tool dialog:
arcpy.GetMessages()
  
print "Spam and Eggs are Well Done"
