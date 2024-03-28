import os
import nrrd
import argparse
import skimage.io
import numpy as np

from regions_ABA import brain_regions


parser = argparse.ArgumentParser()
parser.add_argument('-i', type=str, required=True, help="cell volume per voxel, nrrd")
parser.add_argument('-r', type=str, required=True, help="aligned region labels, nrrd")
parser.add_argument('-o', type=str, required=True, help="output txt file")
parser.add_argument('-s', type=str, required=True, help="sample ID")
args = parser.parse_args()


print("Processing:", args.i)

# load files
cells, _ = nrrd.read(args.i)
regions, _ = nrrd.read(args.r)

print(cells.shape)
print(regions.shape)
assert( np.shape(cells) == np.shape(regions) )

Region_IDs = np.unique(regions)
cell_volumes = np.zeros(len(Region_IDs)-1)  # exclude Background label, 0

for i, rid in enumerate(Region_IDs):
    if rid > 0:
        print("Region:", rid)

        idx = regions==rid
        volume = np.sum(cells[idx])

        cell_volumes[i-1] = volume
        print("volume:", volume)

with open(args.o, 'w') as f:
    f.write("%10s " % "Sample")
    for br in brain_regions:
        f.write("%25s " % br)
    f.write("\n")

    f.write("%10s " % args.s)
    for volume in cell_volumes:
        f.write("%25d " % volume)
    f.write("\n")

