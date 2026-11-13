#Name: Haley Gojohn
#Created Date: 11/4/2026
#Last Modified: 11/4/2026
#Description: Utilize Describe() and List functions with geoprocessing analysis.

#Imports arcpy and os module.
import arcpy, os

#Set the path name for the current workspace and allow the output results to be overwritten.
arcpy.env.workspace = r"C:\\Users\\River\\OneDrive\\Documents\\ArcGIS\\School\\Geoprocess_W_Python\\Practice8\\Data"
arcpy.env.overwriteOutput = True

#Assigns values to the variables fc and desc.
fc = "precip.shp"
desc = arcpy.Describe(fc)

#Saves the geometry shape type of variable desc as the variable shapeType. Prints out message for verification.
shapeType = desc.ShapeType
print("The geometry type of {0} is {1}.".format(fc, shapeType))

#Lists all attribute fields in the feature class, saves them as list variable fieldList.
fieldList = arcpy.ListFields(fc)
for field in fieldList:
    print("{0} is a type of {1} with a length of {2}."
          .format(field.name, field.type, field.length))

#Retrieves the feature class spatial reference information.
#prints out the name of coordinate system. 
spatialRef = desc.SpatialReference
print("The coordinate system of {0} is {1}.".format(fc, spatialRef.Name))

#Defines the output workspace as variable outputWS. Utilizes the function in os module
#to create valid full path name.
outputWS = os.path.join(arcpy.env.workspace, "Missouri.gdb")
outfc = outputWS + os.sep + fc[:-4] + "2002"                #Defines the output feature class as variable outfc. 
template = os.path.join(outputWS, "MOBoundary")             #Defines the output template feature class for projection as variable template. 
outCS = arcpy.Describe(template).spatialReference           #Retrieves the template layer’s spatial reference property and saves it as variable outCS.
arcpy.Project_management(fc, outfc, outCS)                  #Uses Project tool to project the input to output feature class with the template layer’s spatial reference. 
print("{0} is projected to {1}.".format(fc, outCS.Name))    #Prints out message for verification.

#Creates iteration for range from 2003 to 2006, creates empty feature classes with newly created feature class precip2002 as schema template. 
for year in range(2003, 2006):
    newfile = fc[:-4] + str(year)
    arcpy.CreateFeatureclass_management(outputWS, newfile, shapeType, outfc)
    print("Create Feature Class {0} in {1}".format(newfile, outputWS))

