import sys
import glob
import os

src = sys.argv[1]

#image_files = glob.glob(f + "\\*czi")

#for im_file in image_files:
dest = src

#im_file = im_file[:-4]
dest = dest.replace("-", "_")
dest = dest.replace(" ","_")
#    dest = im_file+".czi"
print(src)
print(dest)
os.rename(src, dest)
