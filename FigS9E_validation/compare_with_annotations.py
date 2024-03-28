import os
import argparse
import numpy as np
import scipy.ndimage
from skimage.morphology import ball
import img3
import matplotlib.pyplot as plt


parser = argparse.ArgumentParser()
parser.add_argument('-a', type=str, required=True, help="annotated nrrd")
parser.add_argument('-s', type=str, required=True, help="segmented nrrd")
parser.add_argument('-o', type=str, required=True, help="output dir")
args = parser.parse_args()


# Manual annotations
fa=args.a
# Prediction for segmented cells
fs=args.s


def nrrd_details(f):
    nrrd        = img3.nrrd_read(f)
    dtype       = nrrd["type"]
    path        = nrrd["path"]
    shape       = nrrd["sizes"]
    offset      = nrrd.get("byte skip", 0)
    dx, dy, dz  = nrrd.get("spacings")
    return dtype, path, shape, offset, dx, dy, dz


def confusion_matrix(ann, sim, o):
    o[(ann == 0) & (sim == 0)] = 0 #TN
    o[(ann == 1) & (sim >  0)] = 1 #TP
    o[(ann == 0) & (sim >  0)] = 2 #FP
    o[(ann == 1) & (sim == 0)] = 3 #FN
    TN = np.sum(o==0)
    TP = np.sum(o==1)
    FP = np.sum(o==2)
    FN = np.sum(o==3)
    totT = np.sum(ann==1)
    totN = np.sum(ann==0)
    print("(TP) %4.1f%%  (FN) %4.1f%%" % (TP/totT*100, FN/totT*100))
    print("(FP) %4.1f%%  (TN) %4.1f%%" % (FP/totN*100, TN/totN*100))

    if 1:
        # Plot convergence of TP/FP/...
        Nk = o.shape[2]
        zTP = np.zeros(Nk)
        zTN = np.zeros(Nk)
        zFP = np.zeros(Nk)
        zFN = np.zeros(Nk)
        ztotT = np.zeros(Nk)
        ztotN = np.zeros(Nk)
        for i in range(Nk):
            _o = o[:,:,0:i+1]
            zTP[i] = np.sum(_o==1)
            zFN[i] = np.sum(_o==3)
            zFP[i] = np.sum(_o==2)
            zTN[i] = np.sum(_o==0)
            ztotT[i] = np.sum(ann[:,:,0:i+1]==1)
            ztotN[i] = np.sum(ann[:,:,0:i+1]==0)
            print(zTP[i], zTN[i], zFP[i], zFN[i], ztotT[i], ztotN[i])

        fig, ax1 = plt.subplots(figsize=(4.3,2.5))
        ax2 = ax1.twinx()
        color = '#02a0a9' #'#02ced9'
        ax1.plot(np.arange(0,Nk), zTP/ztotT, '-',  c='k')
        ax2.plot(np.arange(0,Nk), zTN/ztotN, '--', c=color)
        ax1.set_ylim([0.9, 1.0])
        ax2.set_ylim([0.9, 1.0])
        ax1.set_xlim([0, 40])
        ax1.set_xlabel("z-slice")
        ax1.set_ylabel(r'$\frac{\mathrm{TP}\,(z)}{\sum P \, (z)}$')
        ax2.set_ylabel(r'$\frac{\mathrm{TN} \, (z)}{\sum N \, (z)}$')
        ax2.yaxis.label.set_color(color)
        ax2.tick_params(axis='y', colors=color)
        plt.tight_layout()
        #plt.show()
        plt.savefig("validation_statistics.eps", transparent=False)
        plt.close()


# inputs
dtype, path, shape, offset, dx, dy, dz = nrrd_details(fa)
ann0 = np.memmap(path, dtype, 'r', offset=offset, shape=shape, order='F')
print(">> Annotation:", dtype, path, shape, offset, dx, dy, dz)
dtype, path, shape, offset, dx, dy, dz = nrrd_details(fs)
sim0 = np.memmap(path, dtype, 'r', offset=offset, shape=shape, order='F')
print(">> Prediction:", dtype, path, shape, offset, dx, dy, dz)

ann = np.zeros(ann0.shape)
ann[ann0>0] = 1
sim = np.zeros(sim0.shape)
sim[sim0>0] = 1


# output
of = args.o
if not os.path.exists(of):
    os.makedirs(of)

o = img3.mmap_create("%s/o.raw"%of, np.dtype('uint16'), ann.shape)
img3.nrrd_write("%s/o.nrrd"%of, "%s/o.raw"%of, o.dtype, o.shape, (dx,dy,dz))
o[:,:,:] = 0


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Confusion matrix without pixel adjustment
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#confusion_matrix(ann, sim, o)



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Ignore boundaries of correctly-detected cells
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# connected components from annotations
labelsa, Nca = scipy.ndimage.label(ann, structure=ball(1))

# output array with labels:
# 0: nothing
# 1: correctly detected
# 2: non-detected perimeter
# 3: non-detected cells
ol = img3.mmap_create("%s/ol.raw"%of, np.dtype('uint16'), ann.shape)
img3.nrrd_write("%s/ol.nrrd"%of, "%s/ol.raw"%of, ol.dtype, ol.shape, (dx,dy,dz))
ol[:,:,:] = 0
ol[sim>0] = 1  # original segmentation prediction

#loop over annotated blobs
for i in range(Nca):
    #skip background
    if i==0:
        continue
    if i%100==0:
        print(" %d/%d" % (i,Nca))

    idx = (labelsa==i)

    # color non-detected perimeter to `ol'
    if np.sum(sim[idx]) > 0:
        ol[(idx) & (ol!=1)] = 2

confusion_matrix(ann, ol, o)

# color non-detected cells
ol[(ann == 1) & (ol == 0)] = 3

