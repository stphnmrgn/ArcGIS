# -*- coding: utf-8 -*-
"""
Title: 		    data_fixbrokenlink_fc_rename.py

Purpose: 	    Replace broken layer's workspace for all MXDs in a folder

Description:    This standalone script will find and replace a specific
                workspace path for the broken layers in all maps within a
                folder. For each map, it will only search for the feature that
                is broken. If it matches the user provided broken feature,
                then it replaces that path with a new workspace path.

                The validate parameter is not set (default value is True)
                meaning the workspace will only be updated if the
                replace_workspace_path value is a valid workspace. If it
                is not valid, the workspace will not be replaced. 

                Example: Many maps in a folder use a layer that was renamed.
                A user needs to relink the many layers in each of these maps to 
                the renamed feature.

Type: 		    Standalone script

Author: 	    Stephen Morgan, GISP

Version:        Python 2.7.8
"""


import os
from arcpy import mapping



########################## USER INPUTS ##########################

# get user's map folder pathway
workspace = input('\nType/paste the full pathway to your maps folder, and then press Enter.'
                  ' \nExample, r"L:\DPE\MyProject\Maps": ')

# Get pathway of orignal feature
original_feature = input('\nType/paste the full pathway of the original feature, then press Enter.'
                ' \nExample, r"L:\DPE\MyProject\NEW_GDB.gdb\MajorRoads": ')

# Get pathway of the new data source
renamed_feature = input('\nType/paste the full pathway of the new feature, then press Enter.'
                ' \nExample, r"L:\DPE\MyProject\NEW_GDB.gdb\Highways": ')

########################## USER INPUTS ##########################

fullname = os.path.basename(original_feature)
# Set user inputs to variables that will be passed to lyr.replaceDataSource(
# workspace_path, workspace_type, dataset_name, {validate})
# return feature name from renamed_feature, passed as dataset_name
renamed_feature_basename = os.path.basename(renamed_feature)
# return feature's directory from renamed_feature, passsed as workspace_path
renamed_feature_workspace = os.path.dirname(renamed_feature)

print '\nThe original feature, ' + fullname + ', will be checked against a list of broken layers.'
'\nIf a match is found, then the data source will be replaced with the new feature'

print '\nThe new feature that will replace the original feature: ' + renamed_feature_basename


def crawlmxds(folder):
    """
    Given a directory search for mxd files. Every file with extension ".mxd" will 
    be opened in order to list layers with broken data links. If user input matches
    any features listed, it then replaces the workspace of broken layers.

    Parameters
    ----------
    folder: string, directory to map documents

    Returns
    -------
    result: relinked feature data sources.
    """

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
                # Return tables in MXDs
                tables = mapping.ListTableViews(mxd)

                # Return and loop broken layer list in MXD
                try:
                    brokenlayers = mapping.ListBrokenDataSources(mxd)
                    for brokenlayer in brokenlayers:
                        layername = brokenlayer.name
                        print '     Broken Layer: ' + layername
                    if original_feature in brokenlayers:
                        matchedname = original_feature.name
                        print '     Replacing broken layer workspace: ' + matchedname
                        # replace old data source with new data source
                        original_feature.replaceDataSource(renamed_feature_workspace,"FILEGDB_WORKSPACE", renamed_feature_basename)
                    else:
                        print '     No broken links were fixed because 1) there were no broken layers or 2) no broken layers matched original feature'
                    # for lyr in mapping.ListBrokenDataSources(mxd):
                    #     lyrName = lyr.name
                    #     print '  Broken Layer in ' + mxdName + '.mxd: ' + lyrName

                    #     if lyr.supports("DATASOURCE"):
                    #         # See if the original feature is one of the broken data layers
                    #         if original_feature in lyr.dataSource:
                    #             print '     Replacing broken layer workspace: ' + lyrName
                    #             # replace old data source with new data source
                    #             lyr.replaceDataSource(renamed_feature_workspace, 
                    #             "FILEGDB_WORKSPACE", renamed_feature_basename)

                # Ignore tables
                except:
                    #AttributeError
                    for table in tables:
                        if table.isBroken == True:
                            pass

                mxd.save()
                del mxd


if __name__ == "__main__":
    folderPath = workspace
    crawlmxds(folderPath)


print "\nSpam and Eggs are Done\n"
