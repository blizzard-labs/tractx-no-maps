tractoflow_folder=~/Local/TractX/dataset/bundleframe
models_path=~/Local/TractX/dataset/bundleframe  # Ex: hcp_models/ NOT USED???
model_T1=${models_path}/mni_masked.nii.gz
# model_config=${models_path}/config/config_fss_1.json
model_config=${models_path}/config/config_fss_1.json
subj=sample

# Filtering options (in mm). Change as needed.
minL=20
maxL=200

# RecobundlesX options. Change as needed.
nb_total_executions=9    # len(model_clustering_thr) * len(bundle_pruning_thr) * len(tractogram_clustering_thr) = max total executions (see json).
thresh_dist="10 12"      # Whole brain clustering threshold (in mm) for QuickBundles.
processes=6              # Number of thread used for computation.
seed=0                   # Random number generator initialisation.
minimal_vote=0.5         # Saving streamlines if recognized often enough.

# Defining subj folders
subj_folder=${tractoflow_folder}/${subj}

# Defining inputs
subj_trk=${subj_folder}/Tracking/sifttracts.trk
subj_T1=${subj_folder}/Register_T1/T1w_${subj}.nii.gz

###
# Registering model on subject (using ANTS)
#   -d=image dimension,
#   -f=fixed image, m=moving image
#   -t: transformation a = rigid+affine
#   -n = nb of threads
# This should create 3 files : model_to_subj_anat0GenericAffine.mat,
# model_to_subj_anatInverseWarped.nii.gz and  model_to_subj_anatWarped.nii.gz
###
rbx_folder=${subj_folder}/rbx_folder
model_to_subj=${rbx_folder}/model_to_subj_anat
antsRegistrationSyNQuick.sh -d 3 -f ${subj_T1} -m ${model_T1} -t a -n 4 -o ${model_to_subj}

###
# Cleaning tracking file to make sure it is not too big.
# Recobundles is already long enough :) .
###
subj_filtered_trk=${subj_folder}/Tracking/${subj}__tracking_filteredLength.trk
scil_filter_streamlines_by_length.py --minL ${minL} --maxL ${maxL} ${subj_trk} ${subj_filtered_trk}

###
# Scil's Recobundle
#   processes = nb of threads.
#   Seed = rnd generator seed.
#   inverse is to use the inverse affine
###
mkdir ${rbx_folder}/multi_bundles
affine=${rbx_folder}/model_to_subj_anat0GenericAffine.mat
atlas_dir=${tractoflow_folder}/atlas/atlas/pop_average
scil_recognize_multi_bundles.py ${subj_filtered_trk} ${model_config} ${atlas_dir} ${affine} \
    --out_dir ${rbx_folder}/multi_bundles \
    --processes ${processes} --seeds ${seed}  \
    --minimal_vote_ratio ${minimal_vote} \
    --log_level DEBUG --inverse -f