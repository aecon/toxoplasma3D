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


parser = argparse.ArgumentParser()
parser.add_argument('-i', type=str, required=True, help="input: merged_transformed_cells.nrrd OR merged_voxelized.nrrd")
parser.add_argument('-s', type=int, required=True, help="sample ID")
parser.add_argument('-on', type=str, required=True, help="data type: real or blur")
parser.add_argument('-a', type=str, required=True, help="atlas reference file, tif")
parser.add_argument('-od', type=str, default="plots_coronal_slices_per_brain", help="output folder")
args = parser.parse_args()


def coronal(ax, atlas, cells_masked, cmap, Vmax, Vmin):
    for ic in range(Nc):
        i = slices[ic]
        pa = ax[ic].imshow(atlas[:,i,:], interpolation='nearest', cmap=cm.gray)

        if args.on == "real":
            pb = ax[ic].imshow(cells_masked[:,i,:], interpolation='nearest', cmap=cmap, vmin=Vmin, vmax=Vmax)
        else:
            alphas = ((cells_masked[:,i,:]))/400; alphas[alphas<0.1]=0.1; alphas[alphas>1]=1
            pb = ax[ic].imshow(cells_masked[:,i,:], interpolation='nearest', cmap=cmap, alpha=alphas, vmin=Vmin, vmax=Vmax)

        ax[ic].set_axis_off()

        if ic==0:
            ax[ic].annotate(text="%d"%args.s, xy=(16, 36), xycoords='data', color='w', fontsize=18)

    output_dir = args.od
    if not os.path.exists(output_dir):
    	os.makedirs(output_dir)
    
    plt.subplots_adjust(wspace=0, hspace=0)
    plt.savefig("%s/pic_density_coronal_%s_%d.png"%(output_dir, args.on, sample), bbox_inches='tight', pad_inches=0)
    plt.close()


sample = args.s
print(sample)
if np.sum(np.isin(sample, group1))==1:
    color = 'm'
    vmin=-2e6; vmax=-1e6
    group = "group1"
    cmap = cm.cool
elif np.sum(np.isin(sample, group2))==1:
    color = 'c'
    vmin=1e6; vmax=2e6
    group = "group2"
    cmap = cm.cool
elif np.sum(np.isin(sample, group3))==1:
    color = 'y'
    vmin=-2e6; vmax=-1e6
    group = "group3"
    cmap = cm.viridis
else:
    sys.exit()


# load
atlas = skimage.io.imread(args.a, plugin='tifffile').T

dtype_, path_, shape_, offset_, dx_, dy_, dz_ = img3.nrrd_details(args.i)
cells = img3.read_input(args.i, path_, dtype_, offset_, shape_)
cells_masked = masked_array(cells,cells==0)


# plot
Nc=7
Nr=1
slices = [150, 200, 250, 300, 350, 400, 450, 500]
fig,ax = plt.subplots(Nr,Nc, figsize=(24,3))
coronal(ax, atlas, cells_masked, cmap, vmax, vmin)

