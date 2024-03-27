import os
import sys
import adv
import argparse
import skimage.io
import numpy as np

def nrrd_details(f):
    nrrd        = adv.nrrd_read(f)
    dtype       = nrrd["type"]
    path        = nrrd["path"]
    shape       = nrrd["sizes"]
    offset      = nrrd.get("byte skip", 0)
    dx, dy, dz  = nrrd.get("spacings")
    return dtype, path, shape, offset, dx, dy, dz

parser = argparse.ArgumentParser()
parser.add_argument('-lc', type=str, required=True, help="input: path to left  transformed_cells.nrrd")
parser.add_argument('-rc', type=str, required=True, help="input: path to right transformed_cells.nrrd")
parser.add_argument('-lv', type=str, required=True, help="input: path to left  voxelized.tif")
parser.add_argument('-rv', type=str, required=True, help="input: path to right voxelized.tif")
args = parser.parse_args()

# input data
cl = adv.nrrd_data(args.lc)
cr = adv.nrrd_data(args.rc)
vl = skimage.io.imread(args.lv, plugin='tifffile').T
vr = skimage.io.imread(args.rv, plugin='tifffile').T
print(np.shape(cl), np.shape(cr))
print(np.shape(vl), np.shape(vr))

# atlas
atlasshape = ([320,528,456])
zmid=atlasshape[2]//2

# output files
odir = os.path.dirname(args.lc)
# -merged transformed_cells.raw
oc = adv.mmap_create("%s/merged_transformed_cells.raw"%odir, np.dtype("uint16"), atlasshape)
adv.nrrd_write("%s/merged_transformed_cells.nrrd"%odir, "%s/merged_transformed_cells.raw"%odir, oc.dtype, oc.shape, (1,1,1))
# -merged voxelized.tif
ov = adv.mmap_create("%s/merged_voxelized.raw"%odir, np.dtype("float32"), atlasshape)
adv.nrrd_write("%s/merged_voxelized.nrrd"%odir, "%s/merged_voxelized.raw"%odir, ov.dtype, ov.shape, (1,1,1))

# merge data
cl = cl[:,:,0:zmid]
cr = cr[:,:,0:zmid]
oc[:,:,:] = np.concatenate([cl,np.flip(cr, axis=(2))], axis=2)
vl = vl[:,:,0:zmid]
vr = vr[:,:,0:zmid]
ov[:,:,:] = np.concatenate([vl,np.flip(vr, axis=(2))], axis=2)

# dump merged vtk points
points = []
coordinates = np.where( oc>0 )
coordinates = np.transpose(coordinates)
print("np.shape(coordinates):", np.shape(coordinates))
for c in coordinates:
    cx, cy, cz = c
    ct = oc[ cx, cy, cz ]  # cell counts
    assert(ct>0)
    ct = int(ct+0.5)
    for ic in range(ct):
        points.append( (cx, cy, cz ) )
print("Writing points for merged_cells.vtk", np.shape(coordinates), np.shape(points))
adv.points_write("%s/merged_cells.vtk"%odir, points)

