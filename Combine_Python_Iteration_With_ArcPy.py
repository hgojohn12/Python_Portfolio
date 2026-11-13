#Name: Haley Gojohn
#Created Date: 10/29/2026
#Last Modified: 10/29/2026
#Description: Combine Python iteration and conditional statements with arcpy functions for
#geoprocessing task.

#Imports the modules.
import arcpy, os

#Initializing the variable values with hardcoded values allow the output results to be overwritten.
arcpy.env.workspace = r"C:\\Users\\River\\OneDrive\\Documents\\ArcGIS\\School\\Geoprocess_W_Python\\Practice9\\Data\\USA.gdb"
outputWS = r"C:\\Users\\River\\OneDrive\\Documents\\ArcGIS\\School\\Geoprocess_W_Python\\Practice9\\Data"
outTemplate = r"C:\\Users\\River\\OneDrive\\Documents\\ArcGIS\\School\\Geoprocess_W_Python\\Practice9\\Data\\us48.shp"
arcpy.env.overwriteOutput = True

#Retrieves the template layer’s spatial reference property and saves it as the variable outCS.
outCS = arcpy.Describe(outTemplate).SpatialReference

#Creates iteration for the feature class in current workspace.
fcs = arcpy.ListFeatureClasses()
for fc in fcs:
    outfc = outputWS + os.sep + fc + ".shp"     #Saves the final output feature class name as variable outfc.
    desc = arcpy.Describe(fc)                   #Retrieves the geometry type information.
    shapeType = desc.shapeType
    print("output is {0} as {1}.".format(outfc, shapeType))

#Conditional statement to test the feature class geometric type.
#If the feature class is a polygon feature, projects the feature class with the template’s coordinate system (outCS)
#and saves it as the output feature class. 
    if shapeType == "Polygon":
        arcpy.Project_management(fc, outfc, outCS)
        print("Project {0} to {1}.".format(fc, outfc))      #Print out message for verification.

#Tests whether the geometry type is “Polyline”. If so, projects the feature class with the template’s coordinate system (outCS)
#and saves it as the output feature class.
    elif shapeType == "Polyline":
        prjfc = fc + "_prj"
        arcpy.Project_management(fc, prjfc, outCS)
        arcpy.Clip_analysis(prjfc, outTemplate, outfc)
        print("Project and clip {0} to {1}.".format(fc, outfc))     #Prints out message for verification.

#Tests for point feature, projects the point feature classes to the template layer’s coordinate system (outCS), clip it to
#the extent of the template layer (outTemplate), then save the results in the output
#workspace (outputWS).
    elif shapeType == "Point":
        prjfc = fc + "_prj"
        arcpy.Project_management(fc, prjfc, outCS)
        arcpy.Clip_analysis(prjfc, outTemplate, outfc)
        print("Project and clip {0} to {1}.".format(fc, outfc))
        outBuf = outfc[:-4] + "_buf.shp"
        arcpy.Buffer_analysis(outfc, outBuf, "100 Miles")
        print ("Create 100 Miles buffer as {0}.".format(outBuf))    #Prints out message for verification.

#then continue with the for loop.
cleanupfcs = arcpy.ListFeatureClasses("*_prj")
for cleanfc in cleanupfcs:
    arcpy.Delete_management(cleanfc)                #Delete the intermediate feature class from the current workspace.
    print("Delete {0}".format(cleanfc))             #Prints out message for verification.
