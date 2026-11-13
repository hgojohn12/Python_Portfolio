#Name: Haley Gojohn
#Created Date: 11/12/2026
#Last Modified: 11/12/2026
#Description: Write a script that shows more on the combination of queries, and
#then outputs the results as feature class and table.

#Imports the module.
import arcpy

#Set the path name for the current workspace and allow the output results to be overwritten.
arcpy.env.workspace = r"C:\\Users\\River\\OneDrive\\Documents\\ArcGIS\\School\\Geoprocess_W_Python\\Practice10\\Data"
arcpy.env.overwriteOutput = True

#Assigns the variables with feature classes.
park_feat = "parks.shp"
quake_feat = "quakehis.shp"
river_feat = "rivers.shp"
state_feat = "States.shp"
park_layer = "parks"
quake_layer = "quakes"
river_layer = "rivers"
st_layer = "States"

#Defines the output variables.
out_feat = "SelParks.shp"
out_table = "SelState.dbf"

#Find the national parks based on the name containing NP, create a new feature layer parks.
if arcpy.Exists(park_layer):
    arcpy.Delete_management(park_layer)

query = '"NAME" LIKE \'%NP%\''
arcpy.MakeFeatureLayer_management(park_feat, park_layer, query)
result = arcpy.GetCount_management(park_layer)
print("There are {0} national parks.".format(result))

#Find the earthquake hits with magnitude 5 or higher and create a new feature layer quakes.
if arcpy.Exists(quake_layer):
    arcpy.Delete_management(quake_layer)

query = '"MAG" >= 5'
arcpy.MakeFeatureLayer_management(quake_feat, quake_layer, query)
result = arcpy.GetCount_management(quake_layer)
print("There are {0} earthquake hits with magnitude 5 or higher".format(result))

#Utilize the SelectLayerByLoation function to select features in the feature layer parks
#based whether the feature is located within 50 miles of earthquakes with magnitude 5 and higher.
arcpy.SelectLayerByLocation_management(park_layer, "WITHIN_A_DISTANCE",
    quake_layer, "50 Miles")
result = arcpy.GetCount_management(park_layer)
print("There are {0} national parks located within 50 Miles of \
earthquake hits with magnitude 5 or higher".format(result))

#Within these selected national parks, choose the ones with major rivers
#crossing through the park area.
if arcpy.Exists(river_layer):
    arcpy.Delete_management(river_layer)
arcpy.MakeFeatureLayer_management(river_feat, river_layer)

arcpy.SelectLayerByLocation_management(
    park_layer, "INTERSECT", river_layer)
result = arcpy.GetCount_management(park_layer)
print("{0} of these national parks have major rivers crossing \
the park.".format(result))

#Use the Exists to check the existence of the output feature class.
#If yes, then utilize the Delete function to delete it from the computer disk.
#If not, then copy the selected feature into the new feature class SelParks.shp.
if arcpy.Exists(out_feat):
    arcpy.Delete_management(out_feat)
arcpy.CopyFeatures_management(park_layer, out_feat)
print("Copy the selected features to {0}".format(out_feat))

#Create a new feature layer States based on the feature class States.shp.
if arcpy.Exists(st_layer):
    arcpy.Delete_management(st_layer)
arcpy.MakeFeatureLayer_management(state_feat, st_layer)

#Utilize the SelectLayerByLoation function to
#find the states overlap with any previous selected parks. 
arcpy.SelectLayerByLocation_management(st_layer, "INTERSECT", park_layer)
result = arcpy.GetCount_management(st_layer)
print("These parks locate within {0} states.".format(result))

#Use the Exists to check the existence of the output table.
#If yes, then utilize the Delete function to delete it from the computer disk.
#If not, then just skip to the next line to copy the attribute table of the
#selected feature into the new table SelStates
if arcpy.Exists(out_table):
    arcpy.Delete_management(out_table)
arcpy.CopyRows_management(st_layer, out_table)
print("Copy the selected states into {0}.".format(out_table))

#Frees up computer memory and avoids data locks by deleting the inmemory feature layer.
arcpy.Delete_management(park_layer)
arcpy.Delete_management(quake_layer)
arcpy.Delete_management(river_layer)
arcpy.Delete_management(st_layer)
