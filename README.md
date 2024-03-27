# toxoplasma3D

Data analysis pipeline for the quantification of neuronal cell volume in 3D image data of mouse brain scans, acquired by light-sheet microscopy (mesoSPIM).


## Requirements

* [img3D package](https://github.com/aecon/img3D)
* [allenSDK library](https://allensdk.readthedocs.io/en/latest/)
* Python packages: tifffile, numba, scipy, scikit-image, pandas, matplotlib


## Data

### Groups
```
di=FastSSD/Athena/collabODED/data

group 1:
samples=(4834 4836 4844 4849 4851 4858 4864 4868)

group 2:
samples=(4837 4840 4847 4848 4850 4871 4873)

saline:
samples=(4838 4843)
```

### Cohorts
* Group 1 - Toxofilin-Cre
* Group 2 - Gra16-Cre
* Group 3 - saline


### Data overview
```
Status      Pan     Mouse	Ear Punch	Sex	Strains	        Group       Used in Image Processing
DONE+CHK    854651	4834	N	        F	Toxofilin-Cre	group 1     YES (FC). split cerebellum
DONE        854651	4836	L	        F	Toxofilin-Cre	group 1     YES check. (left is missing cerebellum in some slices)
DONE        854652	4844	L	        M	Toxofilin-Cre	group 1     YES
DONE        854654	4849	L	        M	Toxofilin-Cre	group 1     YES (left+right missing cerebellum in some slices)
DONE        854654	4851	Rx2	        M	Toxofilin-Cre	group 1     YES (left+right missing cerebellum in some slices)
DONE        864447	4858	R	        F	Toxofilin-Cre	group 1     YES (left is missing cerebellum in some slices)
DONE        864449	4864	N	        F	Toxofilin-Cre	group 1     YES
DONE        864449	4868	Rx2	        F	Toxofilin-Cre	group 1     YES Left and Right hemispheres miss part of cerebellum.
            864449	4866	L	        F	Toxofilin-Cre	group 1     -NO Missing part. Bad stitching format.
            854661	4872	R	        M	Toxofilin-Cre	group 1     -NO Missing part.

DONE        854651	4837	B	        F	Gra16-Cre	    group 2     YES (small cerebellum part missing)
DONE        854652	4840	R	        M	Gra16-Cre	    group 2     YES (small cerebellum part missing in left)
DONE        854654	4847	N	        M	Gra16-Cre	    group 2     YES (small cerebellum part missing in left)
DONE        854654	4848	R	        M	Gra16-Cre	    group 2     YES (medium cerebellum part missing, left)
DONE        854654	4850	B	        M	Gra16-Cre	    group 2     YES (small cerebellum part missing in left)
DONE        854661	4871	N	        M	Gra16-Cre	    group 2     YES (...missing parts...)
DONE        854661	4873	L	        M	Gra16-Cre	    group 2     YES
            854651	4835	R	        F	Gra16-Cre	    group 2     -NO: Missing large part of cerebellum
            864447	4857	N	        F	Gra16-Cre	    group 2     -NO: Left cerebellum is cut
            864449	4867	B	        F	Gra16-Cre	    group 2     -NO. Large missing part in left hemisphere
            864449	4865	R	        F	Gra16-Cre	    group 2     -stitched not found (never received it)

DONE        854651	4838	Rx2	        F	saline	        group 3     YES
DONE        854652	4843	N	        M	Saline	        group 3     YES
```


### Additional data
* zoom in for sample 4864

```
qnap1:FrancescaCatto_PhD/TOXOPLASMA/images_and_stitched/smal%20stacks_images_4x_1um%20resolution
```


## Authors
The pipeline was developed in the laboratories of Prof. Petros Koumoutsakos (Harvard University) and Prof. Adriano Aguzzi (University of Zurich) by:

* Athena Economides
* Sergey Litvinov
* Francesca Catto

for the publication:  
`<TO BE ADDED>`


