import os
import subprocess
from . import image
import nibabel as nib
from nibabel.streamlines import Field
from nibabel.orientations import aff2axcodes
import datetime

homepath = ""
dataset = ""
current_path = ""

def set_homepath(path):
    global homepath
    homepath = path  
    current_path = path  

def set_data(name):
    global dataset
    dataset = name

def set_context(path):
    if path == 1:
        set_context("/dataset" + dataset + "/dwi")
    elif path == 2:
        set_context("/dataset/instance_files")
    elif path == 3:
        pass
    elif path == 4:
        set_context("/main/functions")
    elif path == 5:
        set_context("/dataset/instance_files/bundleseg")
    else:  
        current_path = homepath + path
        os.chdir(current_path)
        

def set(dataname, home, spec):
    set_data(dataname)
    set_homepath(home)
    set_context(spec)

def do(cmd):
    file = open(homepath + "/main/log.txt", "a")
    file.write("\n" + "> (" + str(datetime.datetime.now()) + ") " + cmd)
    result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
    file.write(result.stdout)
    file.close()
    return(result.stdout)

def load(filename):
    return (image.load_mrtrix(filename))
    
def load_trk_files():
    trk_files = []
    for root, dirs, files in os.walk(current_path):
        for file in files:
            if file.endswith(".trk"):
                trk_files.append(os.path.join(root, file))
    return trk_files

def tck2trk(tckfile, dwifile, trkfile):
    nii = nib.load(dwifile)
    
    header = {}
    header[Field.VOXEL_TO_RASMM] = nii.affine.copy()
    header[Field.VOXEL_SIZES] = nii.header.get_zooms()[:3]
    header[Field.DIMENSIONS] = nii.shape[:3]
    header[Field.VOXEL_ORDER] = "".join(aff2axcodes(nii.affine))
    
    tck = nib.streamlines.load(tckfile)
    nib.streamlines.save(tck.tractogram, trkfile, header=header) 

def get_path():
    return current_path

def trk2tck(trkfile, tckfilename):
    trk = nib.streamlines.load(trkfile)
    nib.streamlines.save(trk.tractogram, tckfilename)

def delete(file):
    do("rm " + file)
    
def mkdir(path):
    os.mkdir(homepath + path)