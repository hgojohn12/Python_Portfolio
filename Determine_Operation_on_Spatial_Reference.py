#Name: Haley Gojohn
#Created Date: 11/8/2026
#Last Modified: 11/8/2026
#Description: Creates a script tool for data version between shapefile and geodatabase feature class.
#Determine the operation based on the data’s spatial reference.

#Imports the modules.
import arcpy, os

#Sets the parameters.
inputWS = arcpy.GetParameterAsText(0)       # Folder containing shapefiles
output_gdb = arcpy.GetParameterAsText(1)    # Output geodatabase
template_fc = arcpy.GetParameterAsText(2)   # Template feature class

# Get template coordinate system
template_desc = arcpy.Describe(template_fc)
template_sr = template_desc.spatialReference
template_sr_name = template_sr.name

arcpy.AddMessage(f"Template Coordinate System: {template_sr_name}")

# Set workspace and list shapefiles
arcpy.env.workspace = inputWS
shapefiles = arcpy.ListFeatureClasses("*.shp")

# Process each shapefile
for shp in shapefiles:
    desc = arcpy.Describe(shp)
    shp_sr = desc.spatialReference
    shp_sr_name = shp_sr.name

    #Output feature class name (without .shp)
    base_name = os.path.splitext(shp)[0]

    #Compare coordinate systems by name
    if shp_sr_name == template_sr_name:
         out_fc = os.path.join(output_gdb, base_name)
         arcpy.AddMessage(f"{shp} and {os.path.basename(template_fc)} "f"are both in {template_sr_name}.")
         arcpy.AddMessage(f"Copy {shp} to {output_gdb}.")
         arcpy.management.CopyFeatures(shp, out_fc)

    else:
        out_fc = os.path.join(output_gdb, base_name + "_prj")
        arcpy.AddMessage(f"Project {shp} from {shp_sr_name} "f"to {template_sr_name}.")
        arcpy.management.Project(shp, out_fc, template_sr)

#Add verification message.
arcpy.AddMessage("Process Complete")
