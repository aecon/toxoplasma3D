# Image processing (v.2)

Tools to perform cell detection from whole 3D mouse brains, and registration to the [Allen Mouse Brain Reference Atlas](http://atlas.brain-map.org).

An updated version of this pipeline can be found in the repository [prionBrain3D](https://github.com/aecon/prionBrain3D).



## 1. segmentation

```
python segmentation.py -i "PATH/TO/SIGNAL/DATA/NRRD" -o "PATH/TO/OUTPUT/DIRECTORY" -Imin IMIN -Imax IMAX -v -p
```
where `IMIN` and `IMAX` are intensity thresholds for the minimum and maximum normalized cell intensity.


To automate the segmentation over all samples, adapt the paths and the intensity thresholds inside `run_segmentation` and run as:
```
./run_segmentation.sh
```


## 2. classification

Exclusion of illuminated vessels and vasculature parts from list of cadidate cells, by training a Random Forest Classifier on volumetric shape metrics and intensity levels.

Usage:
```
python classification.py -l "PATH/TO/LST/PICKLE/FILE" -d "PATH/TO/DENOISED/DATA"
```



## 3. alignment

Alignment of brains onto the Allen Brain Atlas Reference data.

Usage:
```
./run_align.sh
```

