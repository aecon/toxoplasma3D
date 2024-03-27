import os
import sys
import img3
import argparse
import matplotlib.pyplot as plt
import numpy as np
import skimage.io
from numpy.ma import masked_array
from matplotlib import cm


# group details
group1 = [4834, 4836, 4844, 4849, 4851, 4858, 4864, 4868]
group2 = [4837, 4840, 4847, 4848, 4850, 4871, 4873]
group3 = [4838, 4843]
N = [len(group1), len(group2), len(group3)]

TITLES = ["TOXO","Gra16","SALINE"]

parser = argparse.ArgumentParser()
parser.add_argument('-i', type=str, required=True, nargs='+', help="input: merged_transformed_cells.nrrd OR merged_voxelized.nrrd")
parser.add_argument('-on', type=str, required=True, help="outname")  # "real" or "blur"
parser.add_argument('-of', type=str, required=True, help="output folder for figure")  # "real" or "blur"
parser.add_argument('-o', type=str, required=True, help="outdir")
parser.add_argument('-g', type=int, required=True, help="group ID") # 1,2,3 corresponding to: Toxofilin-Cre or Gra16-Cre or saline
parser.add_argument('-a', type=str, required=True, help="atlas reference file, tif")
args = parser.parse_args()


def coronal(ax, atlas, cells_masked, cmap, Vmax, Vmin, group, slices):
    print(args.on)
    for ic in range(Nc):
        i = slices[ic]
        pa = ax[ic].imshow(atlas[:,i,:], interpolation='nearest', cmap=cm.gray)

        if args.on == "real":
            pb = ax[ic].imshow(cells_masked[:,i,:], interpolation='nearest', cmap=cmap, vmin=Vmin, vmax=Vmax)
        else:
            alphas = ((cells_masked[:,i,:]))/100; alphas[alphas<0.1]=0.1; alphas[alphas>1]=1
            pb = ax[ic].imshow(cells_masked[:,i,:], interpolation='nearest', cmap=cmap, alpha=alphas, vmin=Vmin, vmax=Vmax)

        ax[ic].set_axis_off()

        if ic==0:
            if args.g == 1:
                text="Toxofilin-Cre"
            elif args.g == 2:
                text="Gra16-Cre"
            elif args.g == 3:
                text = "saline"
            ax[ic].annotate(text=text, xy=(16, 36), xycoords='data', color='w')

    plt.subplots_adjust(wspace=0, hspace=0)
    plt.savefig("%s/pic_density_coronal_AVG_g%d_%s_%s.png"%(args.of, group, TITLES[group-1], args.on), bbox_inches='tight', pad_inches=0)
    plt.close()


group = args.g; print("Processing group:", group)
if group==1:
    vmin=-2e6; vmax=-1e6
    cmap = cm.cool
elif group==2:
    vmin=1e6; vmax=2e6
    cmap = cm.cool
elif group==3:
    vmin=-2e6; vmax=-1e6
    cmap = cm.viridis
else:
    sys.exit()


# load
atlas = skimage.io.imread(args.a, plugin='tifffile').T
atlasshape = np.shape(atlas)


average = np.zeros(np.shape(atlas))
for file in args.i:
    dtype_, path_, shape_, offset_, dx_, dy_, dz_ = img3.nrrd_details(file)
    cells = img3.read_input(file, path_, dtype_, offset_, shape_)
    average += cells
average /= len(args.i)
cells_masked = masked_array(average,average==0)

name_raw = "%s/avg_cells_group%d.raw"%(args.o, group)
name_nrrd = "%s/avg_cells_group%d.nrrd"%(args.o, group)
o = img3.mmap_create(name_raw, np.dtype("uint16"), atlasshape)
img3.nrrd_write(name_nrrd, name_raw, o.dtype, o.shape, (1,1,1))
o[:,:,:] = average[:,:,:]

Nc=7
Nr=1
slices = [150, 200, 250, 300, 350, 400, 450, 500]
fig,ax = plt.subplots(Nr,Nc, figsize=(24,3))
coronal(ax, atlas, cells_masked, cmap, vmax, vmin, group, slices)

