#!/bin/bash
set -eu

python3 compare_with_annotations.py -a annotations_FC_2021Nov/corrected_z40.nrrd -s predictions/labels32_z40.nrrd -o `pwd`/val
