# reSplit
Use REShAPE output files to split and merge tiled images.

## Installation
```
pip install ...
```
## Usage

`resplit split <path-to-reshape-json> <path-to-image-to-split>`

this command will use the REShAPE JSON file to split the target tiff file into the tile sizes specified in the JSON file.

To merge tiles, pass the REShAPE JSON file and the directory where the tiles are. This will re-assemble the tiles into an image. Note that image bit depth is not guarenteed to be conserved when re-assembling tiles.

`resplit merge <path-to-reshape-json> <path-to-directory-with-tiles>`

