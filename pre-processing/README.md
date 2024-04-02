# Image pre-processing


## Convert tif to raw/nrrd file format

* Use to convert tif files to raw/nrrd format (**required for further steps of the analysis**).
* After running `tif_to_raw.py` two new files will apprear inside the same folder as the original data: A `.raw` file containing the cropped data, and a corresponding `.nrrd` file containing the image metadata.

Usage:
```
python tif_to_raw.py -i "PATH/TO/TIF/FILE"
```
where "PATH/TO/TIF/FILE" is the full path to the `.tif` file, inside quotes.

