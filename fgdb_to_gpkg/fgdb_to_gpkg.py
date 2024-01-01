import argparse
import geopandas as gpd
import fiona
import os
import warnings
from tqdm import tqdm


def fgdb_to_gpkg(fgdb_path: str, gpkg_path: str, overwrite: bool = True, **kwargs):
    """Converts all feature classes within a File GeoDataBase to new layers within a GeoPackage.

    :param fgdb_path: file path of an Esri File GeoDataBase (.gdb)
    :type fgdb_path: str

    :param gpkg_path: file path of an OGC GeoPackage (.gpkg)
    :type fgdb_path: str

    :param overwrite: overwrites existing GeoPackage before copying over new layers if True, defaults to True
    :type bool, optional

    :param **kwargs: additional keyword arguments to pass to geopandas.to_file()
    """

    # Ensure input File GeoDataBase exists
    if not os.path.exists(fgdb_path):
        raise FileNotFoundError(f"{fgdb_path} does not exist!")

    try:
        # Remove existing GeoPackage if overwrite is True
        if os.path.exists(gpkg_path) and overwrite:
            os.remove(gpkg_path)

        # List all feature classes within File GeoDataBase
        fc_list = fiona.listlayers(fgdb_path)

        # Create progress bar
        progress_bar = tqdm(total=len(fc_list), desc="Converting layers")

        # Loop through each feature class
        for fc in fc_list:
            # Check if layer exists in GeoPackage when not overwriting
            if not overwrite and os.path.exists(gpkg_path):
                layer_list = fiona.listlayers(gpkg_path)
                with fiona.open(gpkg_path, "r") as gpkg:
                    if fc in layer_list:
                        warnings.warn(
                            f"Layer {fc} already exists in {gpkg_path}. Skipping...",
                            UserWarning,
                        )
                        continue

            # Read the feature class into GeoDataFrame
            gdf = gpd.read_file(fgdb_path, layer=fc)

            # Write the GeoDataFrame to a GeoPackage
            gdf.to_file(
                gpkg_path,
                driver="GPKG",
                layer=fc,
                index=False,
                if_exists="append",
                **kwargs,
            )

            # Update progress bar
            progress_bar.update(1)

        # Close progress bar
        progress_bar.close()

    except Exception as e:
        print(f"Error converting {fgdb_path} to {gpkg_path}: {e}")


if __name__ == "__main__":
    # Set up argparse to parse command line arguments
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

    # Parse command line arguments
    args = parser.parse_args()

    # Call the fgdb_to_gpkg function with the provided arguments
    fgdb_to_gpkg(args.fgdb_path, args.gpkg_path, args.overwrite)
