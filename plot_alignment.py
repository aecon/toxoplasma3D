import argparse
import skimage.io
import numpy as np
from numpy.ma import masked_array
import matplotlib.pyplot as plt
from matplotlib import cm


parser = argparse.ArgumentParser()
parser.add_argument('-left',  type=str, required=True, help="left hemisphere aligned data, mhd")
parser.add_argument('-right', type=str, required=True, help="right hemisphere aligned data, mhd")
parser.add_argument('-a', type=str, required=True, help="atlas reference file, tif")
parser.add_argument('-outputdir', type=str, required=True, help="path to output directory")
parser.add_argument('-sampleID', type=str, required=True, help="sample ID")
args = parser.parse_args()
print(args)


# paths
fcells1=args.right
fcells2=args.left
fatlas=args.a


# load
atlas  = skimage.io.imread(fatlas,  plugin='tifffile').T
cells1 = skimage.io.imread(fcells1, plugin='simpleitk')  # must be mhd file
cells1 = np.swapaxes(cells1, 0, 2)
cells2 = skimage.io.imread(fcells2, plugin='simpleitk')  # must be mhd file
cells2 = np.swapaxes(cells2, 0, 2)


# atlas shape: 320x528x456
zmid=228
cells1 = cells1[:,:,0:zmid]
cells2 = cells2[:,:,0:zmid]
cells = np.concatenate([cells2,np.flip(cells1, axis=(0,2))], axis=2)


# visuals (adjusted from auto in Fiji)
Vmin=50
Vmax=500
#atlas[atlas<20] = 0
#atlas[atlas>250] = 250


# plot coronal view
Nc=9
Nr=1
fig,ax = plt.subplots(Nr,Nc, figsize=(36,4))
slices = [50, 100, 150, 200, 250, 300, 350, 400, 450]
for ic in range(9):
    k = int(ic)
    i = slices[k]
    pa = ax[ic].imshow(cells[:,i,:],interpolation='nearest',cmap=cm.gray, vmin=Vmin, vmax=Vmax)
    pb = ax[ic].contour(np.log10(atlas[:,i,:]+1), levels=10, linewidths=0.5, linestyles='-', colors='m')
    # pb = ax[ic].contour(atlas[:,i,:], levels=3, linewidths=0.5, linestyles='-', colors='m')
    print(np.min(atlas[:,i,:]), np.mean(atlas[:,i,:]), np.max(atlas[:,i,:]))

    ax[ic].set_axis_off()

plt.subplots_adjust(wspace=0, hspace=0)

plt.savefig("%s/%s_alignment.png" % (args.outputdir, args.sampleID), transparent=True, bbox_inches='tight', pad_inches=0)
plt.close()

