import geopandas as gpd
import fiona
# import arcpy

# Input FileGeodatabase path
fgdb_path = r"data/oregon.gdb"

# Output GeoPackage path
gpkg_path = r"data/oregon.gpkg"

# Using fiona ----

# List all feature classes within FileGeoDataBase
fc_list = fiona.listlayers(fgdb_path)

# Loop through each feature class
for fc in fc_list:

    print(fc)

    # Read the feature class into GeoDataFrame
    gdf = gpd.read_file(fgdb_path, layer=fc)

    # Write the GeoDataFrame to a GeoPackage
    gdf.to_file(gpkg_path, driver="GPKG", layer=fc, index=False, if_exists="append")

# Using arcpy ----

# # List to store all feature classes
# fc_list = []
# 
# # Get all feature classes within the FileGeoDataBase
# for fc in arcpy.ListFeatureClasses(fgdb_path):
#     fc_list.append(fc)
# 
# # Loop through each feature class
# for fc in fc_list:
#     # Read the feature class into a GeoDataFrame
#     gdf = gpd.read_file(fc)
# 
#     # Write the GeoDataFrame to a GeoPackage
#     gdf.to_file(gpkg_path, driver="GPKG", layer=fc, index=False, if_exists="append")
