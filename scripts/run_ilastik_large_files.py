import sys, io
import os
import h5py
import subprocess
import numpy as np
import tkinter as tk
from tkinter import filedialog
from stitch_ilastik_output import stitch
from file_cleanup import cleanup
from pathlib import Path, PurePath

# dummy GUI for file dialog purposes
root = tk.Tk()
root.withdraw()

files = filedialog.askopenfilenames(title="Select input files")

for filepath in files:
    
    p = Path(filepath)

    decimation_factor = 5 
    overlap = 0.05

    dir_ = p.parent
    file_ = p.name
    filesep = "/"

    f = h5py.File(filepath,'r')

    d = f['data']
    t,z,x,y,c=d.shape

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
    tmp_file_list = []

    tmp_dir = PurePath(dir_, "tmp")
    
    try:
        os.mkdir(tmp_dir)
    except OSError:
        print ("Creation of directory %s failed" % tmp_dir)
    
    for i in np.arange(len(xstart)):
        for j in np.arange(len(ystart)):
     
            rs = int(xstart[i])
            re = int(xend[i])
            cs = int(ystart[j])
            ce = int(yend[j])       
            
            tmp_filename = "tmp" + "_".join(["",str(rs),str(re),str(cs),str(ce)]) + ".h5"
            with h5py.File(PurePath(tmp_dir, tmp_filename), "w") as out:
                dset = out.create_dataset("data", data=d[:,:,rs:re,cs:ce,:])
            
            tmp_file_list.append(str(PurePath(tmp_dir, tmp_filename)))

    pixel_probability_maps = [s[:-3] + "_Pixel_Probabilities.h5" for s in tmp_file_list]
    cmd_pixel= "C:\Program Files\ilastik-1.3.2\ilastik.exe --headless"
    cmd_pixel+= ' --project="E:\\Data\\Austin\\CD4_CD8_pixel.ilp"'
    cmd_pixel+= ' --output_format=hdf5 '
    cmd_pixel+= ' --export_source="Pixel Probabilities" '

    cmd_pixel += " ".join(tmp_file_list)
    subprocess.call(cmd_pixel)

    for tmp_file in os.listdir(tmp_dir):
        new_file_name = tmp_file.replace(" ","_")

        os.rename(os.path.join(tmp_dir, tmp_file), os.path.join(tmp_dir, new_file_name))

    cmd_object = "C:\Program Files\ilastik-1.3.2\ilastik.exe --headless"
    cmd_object += ' --project="E:\Data\Austin\CD4_CD8_object.ilp"'
    cmd_object += ' --output_format=hdf5'
    cmd_object += ' --table_filename=' + str(PurePath(tmp_dir, "object_feature_output.csv"))
    cmd_object += ' --raw_data ' + " ".join(tmp_file_list)
    cmd_object += ' --prediction_maps ' + " ".join(pixel_probability_maps)
    subprocess.call(cmd_object)

    stitch(tmp_dir)
    cleanup(tmp_dir)
