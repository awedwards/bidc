#!/usr/bin/env python
# coding: utf-8

from pathlib import Path
import shutil
import pandas as pd

def make_dir(path):
    # creates a path if it doesn't already exist
    if not path.exists():
        path.mkdir()

# path to your source and destination
expdir = Path("F://ucsf/bidc/mibi/data/IPIMEL353_T1/")
destdir = Path(expdir.parent, "mantis")
make_dir(destdir)

# building paths to deepcell output folders
fovdirs = Path(expdir,"input_data","single_channel_inputs")
singlecelloutdir = Path(expdir, "single_cell_output")

outputdir = Path(destdir, expdir.name)
make_dir(outputdir)

print("Reading single cell expression file")
df = pd.read_csv(Path(singlecelloutdir,"cell_table_arcsinh_transformed.csv"))

print("Copying image data")
shutil.copytree(fov_dirs, Path(outputdir, "data"))

print("Copying segmentation and expression data")
for fov in fovdirs.iterdir():
    if fov.is_dir():        
        shutil.copy(Path(expdir,"deepcell_output", fov.name + "_feature_1.tif"), Path(outputdir, "data", fov.name, "seg.tif"))
        df[df["fov"] == fov.name].to_csv( Path(outputdir, "data", fov.name,"features.csv"))

