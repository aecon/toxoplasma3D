import matplotlib.pyplot as plt
import numpy as np
import skimage.io
from numpy.ma import masked_array
from matplotlib import cm


# paths
# -right
resdir1="data/4864_right/align"
fcells1="%s/elastix_data_to_atlas/result.1.mhd" % resdir1
# -left
resdir2="data/4864_left/align"
fcells2="%s/elastix_data_to_atlas/result.1.mhd" % resdir2

fatlas="atlas/ABA_25um_annotation.tif"

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
Vmin=0
Vmax=600


# plot coronal view
Nc=5
Nr=2
fig,ax = plt.subplots(Nr,Nc, figsize=(20,8))
slices = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500]
for ir in range(2):
    for ic in range(5):
        k = int(Nc*ir + ic)
        i = slices[k]
        pa = ax[ir,ic].imshow(cells[:,i,:],interpolation='nearest',cmap=cm.gray, vmin=Vmin, vmax=Vmax)
        pb = ax[ir,ic].contour(np.log10(atlas[:,i,:]+1), levels=10, linewidths=0.5, linestyles='--', colors='m')
        print(np.min(atlas[:,i,:]), np.mean(atlas[:,i,:]), np.max(atlas[:,i,:]))

        ax[ir,ic].set_axis_off()

plt.subplots_adjust(wspace=0, hspace=0)

plt.savefig("alignment.pdf", transparent=True, bbox_inches='tight', pad_inches=0)
plt.close()
