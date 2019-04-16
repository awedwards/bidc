import os, sys
from shutil import rmtree
from pathlib import Path, PurePath

def cleanup(f):

    p = Path(f) 
    
    for src in p.glob("./*full*"):
        dest = PurePath(p.parent, src.name)
        os.rename(src, dest)
    rmtree(f)

