# toxoplasma3D

Data analysis pipeline for the quantification of ZsGreen+ cell volume in 3D image stacks of mouse brain scans, acquired by light-sheet microscopy (mesoSPIM). Developed for the publication:  
* Bracha, Shahar, et al. "Engineering Toxoplasma gondii secretion systems for intracellular delivery of multiple large therapeutic proteins to neurons." Nature Microbiology (2024): 1-22.  
[https://doi.org/10.1038/s41564-024-01750-6](https://doi.org/10.1038/s41564-024-01750-6)

## Installation


### Requirements

* [img3D](https://github.com/aecon/img3D)
* [elastix](https://elastix.lumc.nl)
* [Fiji](https://fiji.sc)
* [AllenSDK](https://allensdk.readthedocs.io/en/latest)
* [ClearMap 2.0](https://christophkirst.github.io/ClearMap2Documentation/html/home.html)
* Python packages (see below)


### Python packages

Create a new conda environment.
```
conda create -n "toxoplasma3D" python=3.8
```

Activate the environment.
```
conda activate toxoplasma3D
```

Install python packages.
```
pip install -r requirements.txt
```



## Contents

The directories `pre-processing`, `processing` and `plotting` contain tools to detect cells from whole 3D mouse brains, perform statistical analysis and generate figures for the corresponding publication.

### pre-processing:
Tools for stack pre-processing.
* Conversion of image stacks from tif to raw/nrrd file formats.

### processing:
Main pipeline for image processing of 3D stacks.
* Cell segmentation: Detection of candidate cells in 3D.
* Artifact classification: Classification of candidate cells into true cells and artifacts.
* Alignment: Registration to Allen Brain Atlas Reference space.
* Voxelization: Apply a Gaussian smoothing with diameter 15 pixels, for visualization purposes.

### plotting:
Tools to perform statistical analysis and generate paper figures.



## Dataset

Tif stacks (3D image data) of mouse brains, obtained with light-sheet microscopy (mesoSPIM), imaged across the sagittal plane.

### Cohorts
```
Group 1 - Toxofilin-Cre:
samples=(4834 4836 4844 4849 4851 4858 4864 4868)

Group 2 - Gra16-Cre:
samples=(4837 4840 4847 4848 4850 4871 4873)

Group 3 - Saline:
samples=(4838 4843)
```

### Overview
```
Status      Pan     Mouse	Ear Punch	Sex	Straing         Group       Used?   Notes
DONE+CHK    854651	4834	N	        F	Toxofilin-Cre   group 1     YES     Rip in cerebellum.
DONE        854651	4836	L	        F	Toxofilin-Cre   group 1     YES     Left is missing cerebellum in some slices.
DONE        854652	4844	L	        M	Toxofilin-Cre   group 1     YES
DONE        854654	4849	L	        M	Toxofilin-Cre   group 1     YES     Left+right missing cerebellum in some slices.
DONE        854654	4851	Rx2	        M	Toxofilin-Cre   group 1     YES     Left+right missing cerebellum in some slices.
DONE        864447	4858	R	        F	Toxofilin-Cre   group 1     YES     Left is missing cerebellum in some slices.
DONE        864449	4864	N	        F	Toxofilin-Cre   group 1     YES
DONE        864449	4868	Rx2	        F	Toxofilin-Cre   group 1     YES     Left and Right missing cerebellum in some slices.
            864449	4866	L	        F	Toxofilin-Cre   group 1     -NO     Missing part. Error in stitching format.
            854661	4872	R	        M	Toxofilin-Cre   group 1     -NO     Missing part.

DONE        854651	4837	B	        F	Gra16-Cre       group 2     YES     Small cerebellum part missing.
DONE        854652	4840	R	        M	Gra16-Cre       group 2     YES     Small cerebellum part missing in left.
DONE        854654	4847	N	        M	Gra16-Cre       group 2     YES     Small cerebellum part missing in left.
DONE        854654	4848	R	        M	Gra16-Cre       group 2     YES     Medium cerebellum part missing, left.
DONE        854654	4850	B	        M	Gra16-Cre       group 2     YES     Small cerebellum part missing in left.
DONE        854661	4871	N	        M	Gra16-Cre       group 2     YES     Small parts are cut.
DONE        854661	4873	L	        M	Gra16-Cre       group 2     YES
            854651	4835	R	        F	Gra16-Cre       group 2     -NO     Missing large part of cerebellum.
            864447	4857	N	        F	Gra16-Cre       group 2     -NO     Left cerebellum is cut.
            864449	4867	B	        F	Gra16-Cre       group 2     -NO     Large missing part in left hemisphere.
            864449	4865	R	        F	Gra16-Cre       group 2     -NO     Stitched file not found (never received it).

DONE        854651	4838	Rx2	        F	saline          group 3     YES
DONE        854652	4843	N	        M	Saline          group 3     YES
```


### Data resources

The data used in the study are located in this [Zenodo repository](https://zenodo.org/records/10835742), DOI: 10.5281/zenodo.10835741, containing the raw data per sample at the resolution of the Allen Brain Atlas (25 micro meters), 3D maps of the the detected cell colume per voxel, and the detected cell maps after voxelization.



## Authors
The pipeline was developed in the laboratories of Prof. Petros Koumoutsakos (Harvard University) and Prof. Adriano Aguzzi (University of Zurich) by:

* Athena Economides
* Sergey Litvinov
* Francesca Catto


## TODO
* Replace alignment with newer version (AllenSDK).
* Add `requirements.txt`.
* Improve alignment of brain 4851.
* Generalize paths to data.

