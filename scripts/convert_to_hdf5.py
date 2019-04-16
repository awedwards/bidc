import h5py
import sys
from PIL import Image
Image.MAX_IMAGE_PIXELS = 10000000000
import cv2
import numpy as np
import glob

f = sys.argv[1]
files = glob.glob(f + "\\*tif")

for file_ in files:
  
  im = Image.open(file_)
  imarray = np.array(im)
  print(imarray.shape) 
  while len(imarray.shape) < 5:
    imarray = np.expand_dims(imarray, axis=0)
  print(imarray.shape)
  i = file_.find("_s")
  new_name = "".join(["full",file_[i:i+3],".hdf5"])
  dest = "\\".join(f.split("\\") + [new_name])
  
  print(dest)
  
  with h5py.File(dest, "w") as out:
    dset = out.create_dataset("data", data=imarray)

