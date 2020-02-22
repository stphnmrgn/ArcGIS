# -*- coding: utf-8 -*-
"""
Title: 		    data_fixbrokenlink.py

Purpose: 	    Replace layer workspace of all features in map folder

Description:    If a series of maps have broken links as the result of
                renaming a geodatabase, this standalone script will fix 
                the broken links for all the maps within a folder.

Type: 		    Standalone script

Author: 	    Stephen Morgan, GISP

Version:        Python 2.7.8
"""

# Import modules
import os
from arcpy import mapping



########################## USER INPUTS ##########################

# Get user's map folder pathway
workspace = input('\nType/paste the full pathway to your maps folder, and then press Enter.'
                  ' \nExample, r"L:\DPE\MyProject\Maps": ')

# Get pathway of the old data source, it will be replaced
old_gdb = input('\nType/paste the full pathway of the old workspace, then press Enter.'
                ' \nExample, r"L:\DPE\MyProject\OLD_GDB.gdb": ')

# Get pathway of the new data source
new_gdb = input('\nType/paste the full pathway of the new workspace, then press Enter.'
                ' \nExample, r"L:\DPE\MyProject\NEW_GDB.gdb": ')

########################## USER INPUTS ##########################

fullname = os.path.basename(workspace)

print '\nYour map directory: \n' + os.path.dirname(workspace)
print '\nThe name of your map folder: ' + fullname
print "\nThe two workspaces we're switching out: "
print os.path.basename(old_gdb)
print os.path.basename(new_gdb)


def crawlmxds(folder):
    for root, dirs, files in os.walk(folderPath):
        for f in files:
            # Crawl folder for files with .mxd extention
            if f.lower().endswith(".mxd"):
                # Return MXD names and pathways
                mxdName = os.path.splitext(f)[0]
                mxdPath = os.path.join(root, f)
                print '\nChecking MXD titled: ' + mxdName
                # Return MXD properties
                mxd = mapping.MapDocument(mxdPath)
                # Return and loop broken layer list in MXD
                for lyr in mapping.ListBrokenDataSources(mxd):
                    lyrName = lyr.name
                    brokensource = lyr.dataSource
                    if lyr.supports("DATASOURCE"):
                        if old_gdb in brokensource:
                            print '     \nReplacing workspace of broken layer: ' + lyrName
                            lyr.findAndReplaceWorkspacePath(old_gdb, new_gdb)
                mxd.save()
                del mxd


if __name__ == "__main__":
    folderPath = workspace
    crawlmxds(folderPath)


print "\nSpam and Eggs are Done\n"
