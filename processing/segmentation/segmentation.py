import os
import sys
import mmap
import time
import numba
import pickle
import argparse
import numpy as np
import multiprocessing
from skimage.morphology import remove_small_objects, remove_small_holes, ball
import adv

me = "cell_detection.py"


def stamp(s):
    if Verbose:
        sys.stderr.write("%s: %d: %s\n" % (me, time.time() - start, s))

def nrrd_details(fnrrd):
    nrrd        = adv.nrrd_read(fnrrd)
    dtype       = nrrd["type"]
    path        = nrrd["path"]
    shape       = nrrd["sizes"]
    offset      = nrrd.get("byte skip", 0)
    dx, dy, dz  = nrrd.get("spacings")
    return dtype, path, shape, offset, dx, dy, dz

def read_stride(argsk):
    if len(argsk) != 3:
        sys.stderr.write("%s: -k needs three arguments\n" % me)
        sys.exit(1)
    kx, ky, kz = argsk
    return kx, ky, kz

def read_input(argsi, me, path, dtype, offset, shape):
    try:
        a0 = np.memmap(path, dtype, 'r', offset=offset, shape=shape, order='F')
    except FileNotFoundError:
        sys.stderr.write("%s: file not found '%s'\n" % (me, argsi))
        sys.exit(1)
    except ValueError:
        sys.stderr.write("%s: wrong size/type '%s'\n" % (me, argsi))
        sys.exit(1)
    return a0

@numba.njit(parallel=True)
def divide(a1, a2, keep, out):
    nx, ny, nz = a1.shape
    for k in numba.prange(nz):
        for j in numba.prange(ny):
            for i in numba.prange(nx):
                out[i, j, k] = a1[i, j, k] / a2[i, j, k] if keep[i, j, k] > 0 else 0

@numba.njit(parallel=True)
def clip(a, value, out):
    nx, ny, nz = a.shape
    for k in numba.prange(nz):
        for j in numba.prange(ny):
            for i in numba.prange(nx):
                out[i, j, k] = a[i, j, k] if a[i, j, k] <= value else value

@numba.njit(parallel=True)
def uclip(a, value, out):
    nx, ny, nz = a.shape
    for k in numba.prange(nz):
        for j in numba.prange(ny):
            for i in numba.prange(nx):
                out[i, j, k] = a[i, j, k] if a[i, j, k] >= value else 0

@numba.njit(parallel=True)
def mask_array(a, keep, out):
    nx, ny, nz = a.shape
    for k in numba.prange(nz):
        for j in numba.prange(ny):
            for i in numba.prange(nx):
                out[i, j, k] = a[i, j, k] if keep[i, j, k] > 0 else 0

@numba.njit(parallel=True)
def mask_01(a, keep, out):
    nx, ny, nz = a.shape
    for k in numba.prange(nz):
        for j in numba.prange(ny):
            for i in numba.prange(nx):
                out[i, j, k] = 1 if (keep[i, j, k]>0 and a[i, j, k]>0) else 0

@numba.njit(parallel=True)
def copy(a, out):
    nx, ny, nz = a.shape
    for k in numba.prange(nz):
        for j in numba.prange(ny):
            for i in numba.prange(nx):
                out[i, j, k] = a[i, j, k]


parser = argparse.ArgumentParser()
# Required
parser.add_argument('-i', type=str, required=True, help="raw data, nrrd")
parser.add_argument('-o', type=str, required=True, help="output directory")
# - background equalization
parser.add_argument('-Imax', type=int, required=True, help="intensity clip")
parser.add_argument('-Imin', type=int, required=True, help="mask region below this value")
# Flags
parser.add_argument('-v', action='store_true', help='verbose')
parser.add_argument('-p', action='store_true', help='run in parallel')
# Defaults
parser.add_argument('-w',  type=int, default=10, help="background smoothing kernel size")
parser.add_argument('-log',type=float, default=0.05, help="numerical threshold for LoG")
parser.add_argument('-Vmin',type=int, default=10, help="minimum cell volume")
parser.add_argument('-Ibmax',type=int, default=1.1, help="minimum Imax per blob")
parser.add_argument('-s',  type=int, default=(1, 1, 1), nargs='+', help="stride (int, int, int)")
parser.add_argument('-ro', type=int, default=300, help="remove objects smaller than ro")
parser.add_argument('-rh', type=int, default=200, help="remove holes smaller than rh")
args = parser.parse_args()
print(args)

Verbose = args.v
Parallel = args.p

# Read RAW data
dtype, path, shape, offset, dx, dy, dz = nrrd_details(args.i)
img_stack = read_input(args.i, me, path, dtype, offset, shape)

# Stride RAW data
sx, sy, sz = read_stride(args.s)
dx, dy, dz = sx*dx, sy*dy, sz*dz
img_stack = img_stack[::sx, ::sy, ::sz]
shape = img_stack.shape
spacings = (dx, dy, dz)
if Verbose:
    sys.stderr.write("%s: shape: %d %d %d\n" % (me, shape[0], shape[1], shape[2]))

start = time.time()

# Create new arrays
stamp("create new arrays")
odir = "%s/%s" % (args.o, "segment")
odir_lst = "%s/%s" % (args.o, "lst")
if not os.path.exists(odir):
    os.makedirs(odir)
if not os.path.exists(odir_lst):
    os.makedirs(odir_lst)
keep    = adv.mmap_create("%s/mask.raw" % odir, np.dtype("uint8"), shape)
keepE   = adv.mmap_create("%s/mask_erosion.raw" % odir, np.dtype("uint8"), shape)
tmp8    = adv.mmap_create("%s/tmp8.raw" % odir, np.dtype("uint8"), shape)
tmp32a  = adv.mmap_create("%s/tmp32a.raw" % odir, np.dtype("float32"), shape)
tmp32b  = adv.mmap_create("%s/tmp32b.raw" % odir, np.dtype("float32"), shape)
labels  = adv.mmap_create("%s/labels.raw" % odir, np.dtype(np.int64), shape)
labels32= adv.mmap_create("%s/labels32.raw" % odir, np.dtype("uint32"), shape)
work    = adv.mmap_create("%s/work.raw" % odir, np.dtype(np.int64), shape)
denoised= adv.mmap_create("%s/denoised.raw" % odir, np.dtype("float32"), shape)

adv.nrrd_write("%s/mask.nrrd" % odir, "%s/mask.raw" % odir, keep.dtype, keep.shape, spacings)
adv.nrrd_write("%s/mask_erosion.nrrd" % odir, "%s/mask_erosion.raw" % odir, keepE.dtype, keepE.shape, spacings)
adv.nrrd_write("%s/denoised.nrrd" % odir, "%s/denoised.raw" % odir, denoised.dtype, denoised.shape, spacings)
adv.nrrd_write("%s/labels32.nrrd" % odir, "%s/labels32.raw" % odir, labels32.dtype, labels32.shape, spacings)

Imax = args.Imax
Imin = args.Imin
ro   = args.ro
rh   = args.rh



def mask(k):
    img0 = img_stack[:, :, k]

    # working array
    img = np.zeros((np.shape(img0)))
    img[:,:] = img0[:,:]

    # mask + remove holes and small objects from mask
    keep0 = np.zeros(np.shape(img), dtype=bool)
    keep0[img>=Imin] = 1
    remove_small_objects(keep0, min_size=ro, in_place = True)
    remove_small_holes(keep0, area_threshold=rh, in_place = True)

    keep[:,:,k] = keep0.astype(keep.dtype)



if __name__ == "__main__":

    stamp("generate mask (multiprocessing.Pool)")
    if Parallel:
        with multiprocessing.Pool() as pool:
            pool.map(mask, range(shape[2]))
    else:
        for k in range(shape[2]):
            mask(k)

    stamp("copy (numba)")
    copy(keep, out=tmp8)
    nstep = 10
    stamp("erode mask (adv.erosion)")
    adv.erosion(tmp8, nstep, keepE)

    stamp("copy (numba)")
    copy(img_stack, out=tmp32a)
    stamp("adv.memset(tmp32b, 0)")
    adv.memset(tmp32b, 0)
    stamp("clip Imax (numba)")
    clip(tmp32a, Imax, tmp32b)

    stamp("background smoothing (adv.gauss)")
    sigma = args.w
    adv.gauss(tmp32b, keep, sigma, tmp32a)

    stamp("intensity normalization (numba)")
    divide(img_stack, tmp32a, keep, out=tmp32b)

    stamp("adv.memset(tmp32a, 0)")
    adv.memset(tmp32a, 0)
    stamp("denoise (adv.gauss)")
    sigma = 1
    adv.gauss(tmp32b, keep, sigma, tmp32a)

    stamp("mask denoised (numba)")
    mask_array(tmp32a, keep, tmp32b)

    stamp("copy (numba)")
    copy(tmp32b, out=denoised)

    stamp("laplacian (adv.convolve)")
    adv.convolve(tmp32b, keep, tmp32a)

    stamp("internal from LoG (numba)")
    uclip(tmp32a, args.log, tmp32b)

    stamp("adv.memset(tmp8, 0)")
    adv.memset(tmp8, 0)
    stamp("mask internal with eroded mask (numba)")
    mask_01(tmp32b, keepE, tmp8)

    stamp("adv.memset(labels, 0)")
    adv.memset(labels, 0)
    stamp("labels (adv.label)")
    Nc = adv.labels(tmp8, labels, work)
    sys.stderr.write("  Nc(all): %d\n" % Nc)

    stamp("adv.remove_small_objects")
    Nc = adv.remove_small_objects(labels, args.Vmin, work)
    sys.stderr.write("  Nc(Vmin): %d\n" % Nc)
    copy(labels, out=labels32)

    stamp("candidate cells (adv.objects)")
    lst = adv.objects(labels, Nc)

    stamp("save candidate list to pickle")
    with open("%s/lst.pkl" % odir,'wb') as fl:
        pickle.dump(lst, fl)

    stamp("filter on Imax (for loop)")
    lst1 = []
    for l in lst:
        Intensities = denoised[l[:,0], l[:,1], l[:,2]]
        if np.max(Intensities) >= args.Ibmax:
            lst1.append(l)
        else:
            labels32[l[:,0], l[:,1], l[:,2]] = 0
    Nc = len(lst1)
    sys.stderr.write("  Nc(Imax): %d\n" % Nc)

    stamp("save candidate list with Imax>Imax_threshold to pickle")
    with open("%s/lst1.pkl" % odir_lst,'wb') as fl:
        pickle.dump(lst1, fl)

    stamp("done.")

