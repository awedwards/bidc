import sys, io
import h5py
import subprocess
import numpy as np

files = sys.argv
decimation_factor = 10
overlap = 0.1

filepath = files[1]
file_ = files[1].split("/")[-1]
print(file_)

f = h5py.File(files[1],'r')

d = f['data']

z,t,x,y,c=d.shape

new_dim_x = np.floor(x/decimation_factor)
new_dim_y = np.floor(y/decimation_factor)

xstart = list(range(0,x,int(new_dim_x * (1-overlap) )))
if x-xstart[-1] < new_dim_x:
    xstart.pop(-1)

xend = xstart+new_dim_x
if xend[-1] < x:
    xend[-1] = x

ystart = list(range(0,y,int(new_dim_y * (1-overlap) )))
if y-ystart[-1] < new_dim_y:
    ystart.pop(-1)

yend = ystart+new_dim_y
if yend[-1] < y:
    yend[-1] = y

for i in np.arange(len(xstart)):
    for j in np.arange(len(ystart)):
 
        rs = int(xstart[i])
        re = int(xend[i])
        cs = int(ystart[j])
        ce = int(yend[j])       
  
        with h5py.File("/".join(files[1].split("/")[0:-1]) + "/tmp" + "_".join(["",str(rs), str(re), str(cs), str(ce)]) + ".h5", "w") as out:
            dset = out.create_dataset("data", data=d[:,:,rs:re,cs:ce,:])
