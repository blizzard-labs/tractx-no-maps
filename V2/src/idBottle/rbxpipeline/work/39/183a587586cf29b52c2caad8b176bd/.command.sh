#!/bin/bash -ue
mkdir tmp/
scil_tractogram_segment_bundles.py tracking.trk config_fss_1.json atlas/ S1__output0GenericAffine.mat --inverse --out_dir tmp/         -v DEBUG --minimal_vote_ratio 0.1         --seed 0 --processes 4
mv tmp/* ./
