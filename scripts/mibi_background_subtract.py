#!/usr/bin/env python
# coding: utf-8

# This script does background subtraction on all
# of the channels in a mibitiff according to the 
# methods outlined in 
# Keren et al. Cell2018,174 (6), 1373-1387
#
# Author: Austin Edwards (austin.edwards@ucsf.edu)

import numpy as np
import pandas as pd
import imageio
from pathlib import Path
from scipy.ndimage import gaussian_filter
from mibidata import tiff

# Parameters
bg_channel_index = 0
sigma = 3
threshold = 0.07

# Set paths
datadir = Path("/home/bidc/Documents/mibi/Background_Subtraction/Images")

# Opens the tiff file
def open_tiff(file_name):
    return tiff.read(str(files[0]))

files = [f for f in datadir.iterdir() if (f.name.endswith(".tiff") or f.name.endswith(".tif"))]
mibitf = open_tiff(files[0])
channels = mibitf.channels

# Find bg channel if one is not set
if bg_channel_index == -1:
    for i,c in enumerate(channels):
        if 'background' in c.lower():
            bg_channel_index = i
            break
if bg_channel_index == -1:
    bg_channel_index = 0
    
for f in files:
    
    mibitf = open_tiff(f)
    new_im = mibitf.copy()
    
    # Apply gaussian filter to bg channel and mask based on provided threshold
    smooth_bg = gaussian_filter(mibitf.data[:,:,bg_channel_index], sigma=sigma)
    mask = np.array(smooth_bg > threshold, dtype=np.uint8)

    for channel_id in np.arange(mibitf.data.shape[2]):
        
        channel_im = mibitf.data[:,:,channel_id]
        
        # Subtract 2 counts from each channel where the mask is above threshold
        channel_im = channel_im - 2*mask
        channel_im[channel_im<0] = 0
        
        new_im.data[:,:,channel_id]=channel_im
        
    tiff.write(str(Path(datadir, f.stem + "_background_subtracted.tiff")), new_im)
