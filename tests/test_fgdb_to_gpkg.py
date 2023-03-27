import os
import tempfile
import geopandas as gpd
from shapely.geometry.polygon import Polygon
from shapely.geometry.multipolygon import MultiPolygon
from fgdb_to_gpkg import fgdb_to_gpkg


def test_fgdb_to_gpkg():
    # Create a temporary File GeoDatabase and GeoPackage
    with tempfile.TemporaryDirectory() as temp_dir:
        fgdb_path = os.path.join(temp_dir, "test.gdb")
        gpkg_path = os.path.join(temp_dir, "test.gpkg")
        layer = "test_fc"

        # Create a GeoDataFrame and save it to the File GeoDatabase
        gdf = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))

        # Promote Polygon to MultiPolygon to avoid fiona write error
        gdf["geometry"] = [
            MultiPolygon([feature]) if isinstance(feature, Polygon) else feature
            for feature in gdf["geometry"]
        ]

        # Write gdf to File GeoDataBase
        gdf.to_file(fgdb_path, layer=layer, driver="OpenFileGDB")

        # Convert the File GeoDatabase to a GeoPackage
        fgdb_to_gpkg(fgdb_path, gpkg_path)

        # Read the File GeoDatabase
        gdf_fgdb = gpd.read_file(fgdb_path, layer=layer)

        # Read the GeoPackage
        gdf_gpkg = gpd.read_file(gpkg_path, layer=layer)

        # Expect each gdf to be the same
        assert gdf_fgdb.equals(gdf_gpkg)
