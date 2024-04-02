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




### Parameters
```
    Vmin    : minimum cell volume (excludes noise and very small cells)
    Vmax    : maximum cell volume (excludes objects that are much larger than expected cells)
    Rmax    : excludes large spreaded objects (that dont necessarily have high Vmax, or k)
    k       : excludes potential vessels (elongated structures)
    Iavg_min: excludes identified cells that are potential noise due to low illumination
    w       : box car window parameter. Window size: (2w+1)
    Imax    : intensity cap for Back. Eq. smoothing (avoids artifacts due to points of high signal intensity)
    Imin    : min sample intensity (used to mask region outside of sample, and exclude it from smoothing operations)
``` 
    



## Specific for Oded project. DO NOT RERUN!!

### Scripts
Located inside `./0_ODED_PROJECT`  
```
STEP 1: Manual copy & file rename. See data paths below.
STEP 2: runall_BEq_parametric_study.sh
STEP 3:
```

## Improvements wrt baseline 1
* Single script for entire pipeline.
* Region labeling.
* BoxCar smoothing, Mask and Cap intensity in background equalization.
* Exclusion of elongated structures (Relative Shape Anisotropy)
* Exclusion of large volumes and large spreaded structures



## atlas

Allen Common Coordinate data (v3)
```
http://download.alleninstitute.org/informatics-archive/current-release/mouse_ccf/ 
```

