<h1 align="center">NDPI to JPG</h1>

### Converts NDPI files from Hamamatsu NanoZoomer slide scanner to JPG images.

## Required packages
* Python 3.8+
* tifffile
* tdqm

## Usage
Put NDPI files in the "data" directory. The script will slice the original files into 512x512 JPG images and save them in the "output" directory.