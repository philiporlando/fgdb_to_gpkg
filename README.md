# fgdb_to_gpkg

`fgdb_to_gpkg` is a Python package that converts all feature classes within an [Esri File GeoDatabase](https://pro.arcgis.com/en/pro-app/latest/help/data/geodatabases/manage-file-gdb/file-geodatabases.htm) to layers within a [OGC GeoPackage](https://www.geopackage.org). This package is designed to be used from the command line or imported as a module.

This package does not have a dependency on ArcPy, which means that you can safely extract feature classes locked inside an Esri File GeoDataBase without needing to worry about any ArcGIS licensing.

## Installation

#### Installing from PyPI

```bash
# Recommended: Install globally using pipx
pipx install fgdb-to-gpkg

# Or install to a manually-created virtual environment
python -m venv env
./env/bin/pip install fgdb-to-gpkg

# Or install to the global Python environment
pip install fgdb-to-gpkg
```

#### Installing the development version of this package

1. Clone the repository: `git clone https://github.com/philiporlando/fgdb_to_gdb.git`
2. Navigate to the repository directory: `cd fgdb_to_gdb`
3. Install the package and its dependencies with [uv](https://astral.sh/uv):  
   ```bash
   uv sync --extra dev
   ```
4. Optionally, install the package to be run globally with pipx: `pipx install --editable .`

## Usage

### Command Line Usage

To use from the command line, simply call the `fgdb-to-gpkg` command with the path to the input File GeoDatabase and the path to the output GeoPackage:

```bash
fgdb-to-gpkg <input_fgdb_path> <output_gpkg_path>
```

See the help menu for more details:

```bash
fgdb-to-gpkg --help
```

### Module Usage

You can also import `fgdb_to_gpkg` as a module in Python and use it to convert any Esri File GeoDatabase feature classes to GeoPackage layers programmatically.

Here's an example of how to use `fgdb_to_gpkg` as a module:

```python
from fgdb_to_gpkg import fgdb_to_gpkg

input_fgdb_path = "/path/to/my_fgdb.gdb"
output_gpkg_path = "/path/to/my_gpkg.gpkg"

fgdb_to_gpkg(input_fgdb_path, output_gpkg_path)
```

See the help menu for more details:

```python
help(fgdb_to_gpkg)
```

## Testing

Unit tests can be performed by the developers of this package using the following command:

```bash
uv run pytest
```

Test coverage can be assessed using the following command:

```bash
uv run pytest --cov=fgdb_to_gpkg --cov-report term-missing
```

#### Handling the Fiona GDAL compilation error

The unit tests within this package depend on `gdal=^3.6.0`, but the current version of `fiona` ships with `gdal=3.5.3`. The fiona package must be installed using the `--no-binary` flag to test this package. If this is not configured properly, then you will see the following error:

```bash
uv run tests
# fiona.errors.DriverError: OpenFileGDB driver requires at least GDAL 3.6.0 for mode 'w', Fiona was compiled against: 3.5.3
```

If you encounter errors related to GDAL or Fiona compatibility, ensure you have the correct versions installed and that your environment is synced using `uv`. If you still encounter issues, try reinstalling Fiona with:

```bash
uv pip install --force-reinstall fiona --no-binary fiona
```

## Publishing

This package is automatically published to PyPI when a new release is crafted. For a successful publication, maintainers should:

1. Increment the version number in the `pyproject.toml` file.
2. Adhere to the `vX.X.X` naming convention for the release name and tag.