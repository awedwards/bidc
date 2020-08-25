import h5py
import pathlib
import sys
from PIL import Image
Image.MAX_IMAGE_PIXELS = 10000000000
import cv2
import numpy as np
import glob

f = sys.argv[1]
files = glob.glob(str(pathlib.PurePath(f, "*tiff")))

for file_ in files:
  
  im = Image.open(file_)
  imarray = np.array(im)

  print(imarray.shape) 
  while len(imarray.shape) < 5:
    imarray = np.expand_dims(imarray, axis=0)
  print(imarray.shape)
  i = file_.find("_s")
  dest = pathlib.PurePath(f, "".join(["full",file_[i:i+3],".h5"]))
  
  print(dest)
  
  #with h5py.File(dest, "w") as out:
  #  dset = out.create_dataset("data", data=imarray)

