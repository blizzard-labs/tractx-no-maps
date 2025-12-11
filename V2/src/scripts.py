import os
import subprocess
import datetime

import nibabel as nib
from nibabel.streamlines import Field
from nibabel.orientations import aff2axcodes

import image

#Presets =========================
homepath = "/Users/krishna/TractX/"
dataset = homepath + "samples/BTC_preop/sub-CON04/"
title = "sub-CON04"
logfile_path = homepath + "src/data/log.txt"
tempfiles = homepath + "src/data/temp/"
bundlepath = homepath + "src/data/bundleseg/"

current_path = homepath


#=================================

def state():
    return [homepath, dataset, title, tempfiles, current_path, bundlepath]


def set_context(path):
    global current_path
    current_path = path
    os.chdir(current_path)
    file = open(logfile_path, "a")
    file.write("\n" + "> (" + str(datetime.datetime.now()) + ") CONTEXT: " + current_path)
    file.close()


def do(cmd):
    file = open(logfile_path, "a")
    file.write("\n" + "> (" + str(datetime.datetime.now()) + ") " + cmd)
    result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
    file.write(result.stdout)
    file.close()
    return (result.stdout)


def load(filepath):
    return (image.load_mrtrix(filepath))


def load_trk_files(folder_path):
    trk_files = []
    for root, dirs, files in os.walk(folder_path):
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


def trk2tck(trkfile, tckfile):
    trk = nib.streamlines.load(trkfile)
    nib.streamlines.save(trk.tractogram, tckfile)


def delete(file):
    do("rm " + file)


def mkdir(path):
    os.mkdir(path)


def completeRunTime():
    file = open(logfile_path, "a")
    file.write("\n" + "> (" + str(datetime.datetime.now()) + ") FINISHED RUNTIME\n")
    file.close()
