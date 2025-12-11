#!/bin/bash -ue
for centroid in centroids/*.trk;
    do bname=${centroid/_centroid/}
    bname=$(basename $bname .trk)

    scil_apply_transform_to_tractogram.py ${centroid} fa.nii.gz S1__output0GenericAffine.mat tmp.trk --inverse --keep_invalid -f
    scil_remove_invalid_streamlines.py tmp.trk S1__${bname}.trk --cut_invalid --remove_single_point --remove_overlapping_points --no_empty
done
