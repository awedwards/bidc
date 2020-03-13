import h5py
import numpy as np
import click
import sys
import pathlib

DEFAULT_NUM_ROIS = 5
w,h = 2000,2000

filepath = pathlib.Path(sys.argv[1])

try:
    num_rois = int(sys.argv[2])
except IndexError:
    num_rois = DEFAULT_NUM_ROIS

full_file = h5py.File(filepath,'r')

_,_,x,y,_ = full_file['data'].shape

for i in np.arange(num_rois):
    
    rx,ry = np.random.randint(x)-w, np.random.randint(y)-h
    
    with h5py.File(pathlib.Path(filepath.parent, "ROI_" + str(i) + ".h5"), 'w') as out:
        dset = out.create_dataset("data", data=full_file['data'][:, :, rx:rx+w, ry:ry+h, :])
