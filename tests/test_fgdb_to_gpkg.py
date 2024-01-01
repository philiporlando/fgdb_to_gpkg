import pytest
import tempfile
import os
import geopandas as gpd
import warnings
from typing import Literal
from shapely.geometry.polygon import Polygon
from shapely.geometry.multipolygon import MultiPolygon
from fgdb_to_gpkg import (
    remove_gpkg_if_overwrite,
    get_layer_lists,
    convert_layer,
    fgdb_to_gpkg,
)


# Setup fixture
@pytest.fixture
def setup_fgdb_gpkg() -> tuple[str, str, list[str]]:
    # Setup fixture for creating a temporary File GeoDatabase and GeoPackage
    with tempfile.TemporaryDirectory() as temp_dir:
        fgdb_path = os.path.join(temp_dir, "test.gdb")
        gpkg_path = os.path.join(temp_dir, "test.gpkg")
        layer = "layer1"
        layers = [layer, "layer2", "layer3"]

        # Create a GeoDataFrame
        gdf = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
        gdf["geometry"] = [
            MultiPolygon([feature]) if isinstance(feature, Polygon) else feature
            for feature in gdf["geometry"]
        ]

        # Write the GeoDataFrame to layers within File GeoDatabase
        for layer in layers:
            gdf["layer_name"] = layer
            gdf.to_file(fgdb_path, layer=layer, driver="OpenFileGDB")

        yield fgdb_path, gpkg_path, layer


def test_remove_gpkg_if_overwrite(setup_fgdb_gpkg: tuple[str, str, list[str]]):
    _, gpkg_path, _ = setup_fgdb_gpkg
    # Create a dummy file to simulate an existing GeoPackage
    with open(gpkg_path, "w") as f:
        f.write("dummy content")
    remove_gpkg_if_overwrite(gpkg_path, True)
    assert not os.path.exists(gpkg_path), "GeoPackage was removed as expected."


# Test for get_layer_lists function
def test_get_layer_lists(setup_fgdb_gpkg: tuple[str, str, list[str]]):
    fgdb_path, gpkg_path, _ = setup_fgdb_gpkg
    fc_list, layer_list = get_layer_lists(fgdb_path, gpkg_path, False)
    # Check the returned lists as per your expectations


# Test for convert_layer function
def test_convert_layer(setup_fgdb_gpkg: tuple[str, str, list[str]]):
    fgdb_path, gpkg_path, layer = setup_fgdb_gpkg
    convert_layer(layer, fgdb_path, gpkg_path, False, [])
    # Read and check if the layer was added to the GeoPackage


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


def test_layer_already_exists(setup_fgdb_gpkg: tuple[str, str, Literal["test_fc"]]):
    # Test the behavior when a layer already exists and overwrite is False
    fgdb_path, gpkg_path, _ = setup_fgdb_gpkg

    warnings.simplefilter("always")

    # First conversion to create the layer
    fgdb_to_gpkg(fgdb_path, gpkg_path, overwrite=True)

    # Try converting again with overwrite=False
    # This should raise a warning because the layers already exists
    with pytest.warns(UserWarning) as record:
        fgdb_to_gpkg(fgdb_path, gpkg_path, overwrite=False)


def test_fgdb_to_gpkg_missing_inputs():
    # Test that a type error is raised when no positional arguments are passed
    with pytest.raises(TypeError):
        fgdb_to_gpkg()
