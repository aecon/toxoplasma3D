# Image processing (v.2)


## Pre-processing

**STEP 1. Create raw/nrrd files**  
```
    See:
    01_tif_to_rawnrrd/run_tif2nrrd.sh
```

**STEP 2. General process (all-in-one)**  
Runs the full pipeline for segmentation & alignment.
The script is SAFE to run: it uses a test data set and output folder.
```
    ./run.sh
```
Main processing algorithms called in `run.sh`:
```
    back2.py
    segment.py
    align.py
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
    

**STEP 3. Figure generation**   
```
    Region labeling:
    ./run_regions.sh <Path to */align/cells.vtk files>
    -> output: cells.vtk.out, cells.vtk.vtk files

    Collect region counts:
    ./run_regions_collect.sh <list of cells.vtk.out files>
    -> prints counts per selected brain region
```


## Specific for Oded project. DO NOT RERUN!!

### Scripts
Located inside `./0_ODED_PROJECT`  
```
STEP 1: Manual copy & file rename. See data paths below.
STEP 2: runall_BEq_parametric_study.sh
STEP 3:
```

### Data

```
di=/media/athena-admin/FastSSD/Athena/collabODED/data

group 1
samples=(4834 4836 4844 4849 4851 4858 4864 4868)

group 2
samples=(4837 4840 4847 4848 4850 4871 4873)

saline
samples=(4838 4843)
```

## Test data
* 4864: Group 1 - Toxofilin-Cre
* 4857: Group 2 - Gra16-Cre
* 4838: Group 3 - saline


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


## Status

```
Status      Pan     Mouse	Ear Punch	Sex	Strains	        Group       Used in Image Processing ?
DONE+CHK    854651	4834	N	        F	Toxofilin-Cre	group 1     YES (FC). split cerebellum
DONE        854651	4836	L	        F	Toxofilin-Cre	group 1     YES check. (left is missing cerebellum in some slices)
DONE        854652	4844	L	        M	Toxofilin-Cre	group 1     YES
DONE        854654	4849	L	        M	Toxofilin-Cre	group 1     YES (left+right missing cerebellum in some slices)
DONE        854654	4851	Rx2	        M	Toxofilin-Cre	group 1     YES (left+right missing cerebellum in some slices)
DONE        864447	4858	R	        F	Toxofilin-Cre	group 1     YES (left is missing cerebellum in some slices)
DONE        864449	4864	N	        F	Toxofilin-Cre	group 1     YES
DONE        864449	4868	Rx2	        F	Toxofilin-Cre	group 1     YES (left+right missing cerebellum in some slices)
            864449	4866	L	        F	Toxofilin-Cre	group 1     -NO  missing part. weird stitched format
            854661	4872	R	        M	Toxofilin-Cre	group 1     -NO missing part

DONE        854651	4837	B	        F	Gra16-Cre	    group 2     YES (small cerebellum part missing)
DONE        854652	4840	R	        M	Gra16-Cre	    group 2     YES (small cerebellum part missing in left)
DONE        854654	4847	N	        M	Gra16-Cre	    group 2     YES (small cerebellum part missing in left)
DONE        854654	4848	R	        M	Gra16-Cre	    group 2     YES (medium cerebellum part missing, left)
DONE        854654	4850	B	        M	Gra16-Cre	    group 2     YES (small cerebellum part missing in left)
DONE        854661	4871	N	        M	Gra16-Cre	    group 2     YES (...missing parts...)
DONE        854661	4873	L	        M	Gra16-Cre	    group 2     YES
            854651	4835	R	        F	Gra16-Cre	    group 2     -NO: Big missing cerebellum
            864447	4857	N	        F	Gra16-Cre	    group 2     -NO: left cerebellum is cut
            864449	4867	B	        F	Gra16-Cre	    group 2     -NO. Has huge missing piece in left
            864449	4865	R	        F	Gra16-Cre	    group 2     -stitched not found (never received it)

DONE        854651	4838	Rx2	        F	saline	        group 3     YES
DONE        854652	4843	N	        M	Saline	        group 3     YES
```

```
bsub -R 'span[hosts=1]' -n 80 OMP_NUM_THREADS=80 ADV_VERBOSE= cm.python -u cell_detection.py  -i /cluster/scratch/lisergey/01_Toxofilin-Cre/4864/midres_left.nrrd -o /cluster/scratch/lisergey/ -Imin 160 -Imax 800 -v -p
```

## Extra
* zoom in for sample 4864

```
smb://qnap1/home/Data/FrancescaCatto_PhD/TOXOPLASMA/images_and_stitched/smal%20stacks_images_4x_1um%20resolution
```

