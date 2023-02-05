library(pacman)
p_load(dplyr, sf, magrittr)

fgdb_path = "data/oregon.gdb"
gpkg_path = "data/oregon.gpkg"

# Read all fgdb layers
layers_fgdb <- sf::st_layers(fgdb_path)
df_fgdb <- purrr::map(layers_fgdb$name, function(name) {
  sf::st_read(fgdb_path, layer = name)
}) %>% dplyr::bind_rows()

# Read all gpkg layers (after running python script)
layers_gpkg <- sf::st_layers(gpkg_path)
df_gpkg <- purrr::map(layers_gpkg$name, function(name) {
sf::st_read(gpkg_path, layer = name)  
}) %>% dplyr::bind_rows()

# Verify that all counties are included
plot(df_fgdb)
plot(df_gpkg)

glimpse(df_fgdb)
glimpse(df_gpkg)
