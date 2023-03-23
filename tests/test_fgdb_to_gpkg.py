import os
import tempfile
import geopandas as gpd
from fgdb_to_gpkg import fgdb_to_gpkg


def test_fgdb_to_gpkg():
    # Create a temporary File GeoDatabase and GeoPackage
    with tempfile.TemporaryDirectory() as temp_dir:
        fgdb_path = os.path.join(temp_dir, "test.gdb")
        gpkg_path = os.path.join(temp_dir, "test.gpkg")

        # Create a GeoDataFrame and save it to the File GeoDatabase
        gdf = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
        gdf.to_file(fgdb_path, layer="test", driver="FileGDB")

        # Convert the File GeoDatabase to a GeoPackage
        fgdb_to_gpkg(fgdb_path, gpkg_path)

        # Load the GeoPackage into a GeoDataFrame
        gdf_gpkg = gpd.read_file(gpkg_path, layer="test")

        # Assert that the two GeoDataFrames are equal
        assert gdf_gpkg.equals(gdf)
