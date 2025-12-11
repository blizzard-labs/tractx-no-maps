#!/bin/bash -ue
export ANTS_RANDOM_SEED=1234
antsRegistrationSyNQuick.sh -d 3 -f fa.nii.gz -m mni_masked.nii.gz -n 4 -o S1__output -t a
cp fa.nii.gz S1__native_anat.nii.gz
