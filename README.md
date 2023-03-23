# fgdb_to_gpkg

`fgdb_to_gpkg` is a Python package that converts all feature classes within a specific [Esri File GeoDatabase](https://pro.arcgis.com/en/pro-app/latest/help/data/geodatabases/manage-file-gdb/file-geodatabases.htm) into layers within a [OGC GeoPackage](https://www.geopackage.org). If the GeoPackage does not already exist, then a new one will be created. This package is designed to be used from the command line or imported as a module.

This package does not have a dependency on ArcPy, which means that you can safely extract feature classes locked inside an Esri File GeoDataBase without needing to worry about any ArcGIS licensing.

## Installation

1. Clone the repository: `git clone https://github.com/philiporlando/fgdb_to_gdb.git`
2. Navigate to the repository directory: `cd fgdb_to_gdb`
3. Install the package and its dependencies with pipenv: `pipenv install`

```
# TODO add alternative installation instructions using pip?
pip install git+https://github.com/philiporlando/fgdb_to_gpkg
```

## Usage

### Command Line Usage

To use `fgdb_to_gpkg` from the command line, simply call the `fgdb_to_gpkg` command with the path to the input File GeoDatabase and the path to the output GeoPackage:

```
pipenv run python -m fgdb_to_gpkg <input_fgdb_path> <output_gpkg_path> --verbose
```

### Module Usage

You can also import `fgdb_to_gpkg` as a module in Python and use it to convert any Esri File GeoDatabase feature classes to GeoPackage layers programmatically.

Here's an example of how to use `fgdb_to_gpkg` as a module:

```python
from fgdb_to_gpkg import fgdb_to_gpkg

input_fgdb_path = "/path/to/my_fgdb.gdb"
output_gpkg_path = "/path/to/my_gpkg.gpkg"

fgdb_to_gpkg(input_fgdb_path, output_gpkg_path, verbose=True)

# See help(fgdb_to_gpkg) for more details
```