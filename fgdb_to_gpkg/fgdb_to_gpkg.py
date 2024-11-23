import argparse
import os
import warnings
from typing import List, Tuple

import fiona
import geopandas as gpd
import pandas
import pyogrio
from tqdm import tqdm


def remove_gpkg_if_overwrite(gpkg_path: str, overwrite: bool) -> None:
    """
    Removes an existing GeoPackage file if overwrite is True.

    :param gpkg_path: file path of the GeoPackage (.gpkg)
    :type gpkg_path: str

    :param overwrite: flag indicating whether to overwrite existing files
    :type overwrite: bool
    """
    if os.path.exists(gpkg_path) and overwrite:
        os.remove(gpkg_path)


def get_layer_lists(
    fgdb_path: str, gpkg_path: str, overwrite: bool
) -> Tuple[List[str], List[str]]:
    """
    Retrieves the list of layers from the File GeoDatabase and, if applicable, from the GeoPackage.

    :param fgdb_path: file path of an Esri File GeoDataBase (.gdb)
    :type fgdb_path: str

    :param gpkg_path: file path of the GeoPackage (.gpkg)
    :type gpkg_path: str

    :param overwrite: flag indicating whether to overwrite existing files
    :type overwrite: bool

    :return: Tuple of two lists containing feature classes and GeoPackage layers
    :rtype: Tuple[List[str], List[str]]
    """
    fc_list = fiona.listlayers(fgdb_path)
    layer_list = (
        fiona.listlayers(gpkg_path)
        if os.path.exists(gpkg_path) and not overwrite
        else []
    )
    return fc_list, layer_list


def convert_layer(
    fc: str,
    fgdb_path: str,
    gpkg_path: str,
    overwrite: bool,
    layer_list: List[str],
    **kwargs,
) -> None:
    """
    Converts a single feature class from the File GeoDatabase to a layer in the GeoPackage.

    :param fc: feature class name
    :type fc: str

    :param fgdb_path: file path of an Esri File GeoDataBase (.gdb)
    :type fgdb_path: str

    :param gpkg_path: file path of the GeoPackage (.gpkg)
    :type gpkg_path: str

    :param overwrite: flag indicating whether to overwrite existing files
    :type overwrite: bool

    :param layer_list: list of existing layers in the GeoPackage
    :type layer_list: List[str]

    :param kwargs: additional keyword arguments for geopandas.to_file(). Note that these
        are not applied to attribute layers.
    """
    if not overwrite and fc in layer_list:
        warnings.warn(
            f"Layer {fc} already exists in {gpkg_path}. Skipping...", UserWarning
        )
        return

    gdf = gpd.read_file(fgdb_path, layer=fc)
    if isinstance(gdf, pandas.DataFrame):
        # Handle attribute layer
        pyogrio.write_dataframe(gdf, gpkg_path, layer=fc, driver="GPKG", append=True)
    else:
        gdf.to_file(gpkg_path, driver="GPKG", layer=fc, index=False, mode="a", **kwargs)


def fgdb_to_gpkg(
    fgdb_path: str, gpkg_path: str, overwrite: bool = True, **kwargs
) -> None:
    """
    Converts all feature classes within a File GeoDataBase to new layers within a GeoPackage.

    :param fgdb_path: file path of an Esri File GeoDataBase (.gdb)
    :type fgdb_path: str

    :param gpkg_path: file path of an OGC GeoPackage (.gpkg)
    :type gpkg_path: str

    :param overwrite: overwrites existing GeoPackage before copying over new layers if True, defaults to True
    :type overwrite: bool

    :param kwargs: additional keyword arguments to pass to geopandas.to_file()
    """
    if not os.path.exists(fgdb_path):
        raise FileNotFoundError(f"{fgdb_path} does not exist!")

    try:
        remove_gpkg_if_overwrite(gpkg_path, overwrite)
        fc_list, layer_list = get_layer_lists(fgdb_path, gpkg_path, overwrite)

        with tqdm(total=len(fc_list), desc="Converting layers") as progress_bar:
            for fc in fc_list:
                convert_layer(fc, fgdb_path, gpkg_path, overwrite, layer_list, **kwargs)
                progress_bar.update(1)

    except Exception as e:
        print(f"Error converting {fgdb_path} to {gpkg_path}: {e}")
        raise


def main():
    parser = argparse.ArgumentParser(
        description="Convert an Esri File GeoDatabase to a GeoPackage"
    )
    parser.add_argument("fgdb_path", type=str, help="path to the File GeoDatabase")
    parser.add_argument("gpkg_path", type=str, help="path to the GeoPackage to create")
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="deletes an existing GeoPackage before copying layers from File GeoDataBase.",
    )

    args = parser.parse_args()
    fgdb_to_gpkg(args.fgdb_path, args.gpkg_path, args.overwrite)


if __name__ == "__main__":
    main()
