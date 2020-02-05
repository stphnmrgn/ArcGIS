'''
Title: 		BrokenLink_Tool.py
Purpose: 	List broken data sources in MXDs and write to a .csv file
Type: 		Standalone script
Author: 	Stephen Morgan
Created: 	09/26/2017
'''

#Import modules
import arcpy, sys, os, csv

print "Enter folder path:"
#workspace = raw_input()
workspace = sys.argv[1] #Include line for ArcToolbox
print os.path.dirname(workspace)

fullname = os.path.basename(workspace) #Return base name of pathway (name of folder). Set variable to path and name of folder
print fullname

path_csv = os.path.dirname(workspace) + os.sep + fullname + ".csv" #Store the folder name as string variable for the 'path'

#Setup the CSV file
def main(folder, outputfile):
    with open(outputfile, "wb") as f:
        #Start writing
        w = csv.writer(f)
        #Set a variable to include the column headers of the csv
        header = ("Map Document", "Broken Layer", "Layer Datasource")
        w.writerow(header)
        rows = crawlmxds(folder)
        w.writerows(rows)

def crawlmxds(folder):
    for root, dirs, files in os.walk(folder):
        for fileName in files:
            basename, extension = os.path.splitext(fileName)
            if extension == ".mxd":
                fullPath = os.path.join(root, fileName)
                mxd = arcpy.mapping.MapDocument(fullPath)
                print "MXD: " + fileName
                brknList = arcpy.mapping.ListBrokenDataSources(mxd)
                for brknItem in brknList:
                    print brknItem.name
                    brknName = brknItem.name
                    DataSource = brknItem.dataSource
                    seq = (fileName, brknName, DataSource);
                    yield seq
                del mxd

if __name__ == "__main__":
    folderPath = workspace # or arcpy.GetParameterAsText(0)
    output = path_csv # or arcpy.GetParameterAsText(1)
    main(folderPath, output)

#This gives feedback in the script tool dialog:
arcpy.GetMessages()

print "Spam and Eggs are Done"
