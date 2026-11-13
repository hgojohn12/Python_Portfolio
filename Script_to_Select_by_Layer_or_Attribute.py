##Name: Haley Gojohn
##Created Date: 11/11/2026
##Last Modified: 11/11/2026
##Description: The script shows how to utilize the combination of the Make Feature Layer, Select Layer By
##Attribute, and Select Layer By Location tools to create feature layer.

import arcpy

arcpy.env.workspace = r"C:\\Users\\River\\OneDrive\\Documents\\ArcGIS\\School\\Geoprocess_W_Python\\Practice10\\Data"
arcpy.env.overwriteOutput = True

states_feat = "States.shp"
volcano_feat = "volcano.shp"
st_layer = "States"
vol_layer = "volcano"

#Finds the number of states with volcanos.
if arcpy.Exists(st_layer):
    arcpy.Delete_management(st_layer)
arcpy.MakeFeatureLayer_management(states_feat, st_layer)

result = arcpy.GetCount_management(st_layer)
print("There are {0} states in the feature layer {1}.".format(result, st_layer))

arcpy.SelectLayerByLocation_management(st_layer, "CONTAINS", volcano_feat)

result = arcpy.GetCount_management(st_layer)
print("There are {0} states with volcano".format(result))

#Finds the number of states with volcano
#higher than 2000 feet
if arcpy.Exists(st_layer):
    arcpy.Delete_management(st_layer)
arcpy.MakeFeatureLayer_management(states_feat, st_layer)

if arcpy.Exists(vol_layer):
    arcpy.Delete_management(vol_layer)

query = '"ELEVATION" > 2000'
arcpy.MakeFeatureLayer_management(volcano_feat, vol_layer, query)

result = arcpy.GetCount_management(vol_layer)
print("There are {0} volcano higher than 2000 feet.".format(result))

arcpy.SelectLayerByLocation_management(st_layer, "CONTAINS", vol_layer)

result = arcpy.GetCount_management(st_layer)
print("There are {0} states with volcano higher than 2000 feet.".format(result))

#Finds the number of volcanos higher than 2000 feet,
#not located within the Pacific region.
if arcpy.Exists(st_layer):
    arcpy.Delete_management(st_layer)

query = '"SUB_REGION" <> \'Pacific\''
arcpy.MakeFeatureLayer_management(states_feat, st_layer, query)

result = arcpy.GetCount_management(st_layer)
print("There are {0} states not part of the Pacific Region.".format(result))

arcpy.SelectLayerByLocation_management(vol_layer, "WITHIN", st_layer)

result = arcpy.GetCount_management(vol_layer)
print("There are {0} volcano higher than 2000 feet not \
located within the Pacific Region.".format(result))

#Finds the number of non-stratovolcano higher than 2000 feet,
# and located within the Pacific region.
if arcpy.Exists(st_layer):
    arcpy.Delete_management(st_layer)
query = '"SUB_REGION" = \'Pacific\''
arcpy.MakeFeatureLayer_management(states_feat, st_layer, query)

if arcpy.Exists(vol_layer):
    arcpy.Delete_management(vol_layer)
query = '"ELEVATION" > 2000'
arcpy.MakeFeatureLayer_management(volcano_feat, vol_layer, query)

query = '"TYPE" <> \'Stratovolcano\''
arcpy.SelectLayerByAttribute_management(vol_layer, "NEW_SELECTION", query)

result = arcpy.GetCount_management(vol_layer)
print("There are {0} non-stratovolcano higher than 2000 feet.".format(result))

arcpy.SelectLayerByLocation_management(vol_layer, "WITHIN", st_layer, "",
    "SUBSET_SELECTION")

result = arcpy.GetCount_management(vol_layer)
print("There are {0} non-stratovolcano higher than 2000 feet \
located within the Pacific Region.".format(result))

arcpy.Delete_management(st_layer)
arcpy.Delete_management(vol_layer)
