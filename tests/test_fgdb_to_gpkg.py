import pytest
import tempfile
import os
import geopandas as gpd
from typing import Literal
from shapely.geometry.polygon import Polygon
from shapely.geometry.multipolygon import MultiPolygon
from fgdb_to_gpkg import fgdb_to_gpkg


@pytest.fixture
def setup_fgdb_gpkg():
    # Setup fixture for creating a temporary File GeoDatabase and GeoPackage
    with tempfile.TemporaryDirectory() as temp_dir:
        fgdb_path = os.path.join(temp_dir, "test.gdb")
        gpkg_path = os.path.join(temp_dir, "test.gpkg")
        layer = "test_fc"

        # Create a GeoDataFrame
        gdf = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
        gdf["geometry"] = [
            MultiPolygon([feature]) if isinstance(feature, Polygon) else feature
            for feature in gdf["geometry"]
        ]

        # Write the GeoDataFrame to File GeoDatabase
        gdf.to_file(fgdb_path, layer=layer, driver="OpenFileGDB")

        yield fgdb_path, gpkg_path, layer


def test_fgdb_to_gpkg(setup_fgdb_gpkg: tuple[str, str, Literal["test_fc"]]):
    # Test basic functionality of fgdb_to_gpkg
    fgdb_path, gpkg_path, layer = setup_fgdb_gpkg

    fgdb_to_gpkg(fgdb_path, gpkg_path)

    # Read and compare data from File GeoDatabase and GeoPackage
    gdf_fgdb = gpd.read_file(fgdb_path, layer=layer)
    gdf_gpkg = gpd.read_file(gpkg_path, layer=layer)
    assert gdf_fgdb.equals(gdf_gpkg)


def test_fgdb_to_gpkg_overwrite(setup_fgdb_gpkg: tuple[str, str, Literal["test_fc"]]):
    # Test the overwrite functionality of fgdb_to_gpkg
    fgdb_path, gpkg_path, layer = setup_fgdb_gpkg

    # Convert the File GeoDatabase to a GeoPackage
    fgdb_to_gpkg(fgdb_path, gpkg_path, overwrite=True)

    # Modify the original GeoDataFrame
    gdf_modified = gpd.read_file(fgdb_path, layer=layer)
    gdf_modified["new_column"] = "test"

    # Write the modified GeoDataFrame to File GeoDatabase
    gdf_modified.to_file(fgdb_path, layer=layer, driver="OpenFileGDB")

    # Convert the modified File GeoDatabase to GeoPackage with overwrite=False
    fgdb_to_gpkg(fgdb_path, gpkg_path, overwrite=False)
    gdf_gpkg_no_overwrite = gpd.read_file(gpkg_path, layer=layer)
    assert "new_column" not in gdf_gpkg_no_overwrite.columns

    # Convert the modified File GeoDatabase to GeoPackage with overwrite=True
    fgdb_to_gpkg(fgdb_path, gpkg_path, overwrite=True)
    gdf_gpkg_overwrite = gpd.read_file(gpkg_path, layer=layer)
    assert "new_column" in gdf_gpkg_overwrite.columns


def test_nonexistent_fgdb(setup_fgdb_gpkg: tuple[str, str, Literal["test_fc"]]):
    # Test that a file not found error is raised when a nonexistent fgdb is used
    _, gpkg_path, _ = setup_fgdb_gpkg
    nonexistent_fgdb_path = "nonexistent.fgdb"
    with pytest.raises(FileNotFoundError):
        fgdb_to_gpkg(nonexistent_fgdb_path, gpkg_path, overwrite=False)
