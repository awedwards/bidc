#!/usr/bin/env python
# coding: utf-8
from mibidata import tiff
import re
from pathlib import Path
import shutil
from os import remove
from sys import argv

def isempty(dir_path):
    # Checks a directory to see if it contains any files
    
    path = Path(dir_path)
    has_next = next(path.iterdir(), None)
    if has_next is None:
        return True
    return False

def create_dir(dir_path):
    # Create an empty directory at dir_path if it doesn't yet exist
    try:
        Path.mkdir(dir_path)
    except FileExistsError:
        if not isempty(input_dir):
            raise Exception('Directory ' +dir_path.name + ' is not empty.')

#Get tiff file names in this folder (say something if there aren't any)
files = [f for f in Path(".").iterdir() if (f.name.endswith(".tif") or f.name.endswith(".tiff"))]

if len(files) == 0:
    raise Exception('No mibi tiff files found. Please place this script in your directory folder.')

cwd = Path.cwd()

#Create required directory structure for DeepCell
input_dir = Path(cwd,"input_data")
create_dir(input_dir)
single_tiff_dir = Path(input_dir, "single_channel_inputs")
create_dir(single_tiff_dir)
mibitiff_dir = Path(input_dir, "mibitiff_inputs")
create_dir(mibitiff_dir)
deepcell_input_dir = Path(input_dir,"deepcell_input")
create_dir(deepcell_input_dir)
deepcell_output_dir = Path(cwd, "deepcell_output")
create_dir(deepcell_output_dir)

for f in files:

    res = re.match("fov\d+",f.name)[0]
    create_dir(Path(single_tiff_dir,res))
    fov_dir = Path(single_tiff_dir,res,"TIFs")
    create_dir(fov_dir)
    mibitf = tiff.read(str(f))
    tiff.write(str(Path(fov_dir)), mibitf,multichannel=False)


#Move tiff files to tiff input directory

for f in files:
    shutil.move(str(Path(cwd, f)), str(Path(mibitiff_dir, f)))

# self-delete
remove(argv[0])

