from . import scripts

def action(title):
    homepath = "/Users/krishna/Local/TractX"
    dataset = "/" + title
    scripts.set(dataset, homepath, 1)
                    
    #2. Convert raw data to .mif ===============================================
    scripts.do("mrconvert dwi_" + title + "_AP.nii.gz ../../../dataset/instance_files/" + title + "_dwi.mif -fslgrad dwi_" + title + "_AP.bvec dwi_" + title + "_AP.bval")

    #3. Denoising the Dataset ===============================================
    scripts.set_context(2)
    scripts.do("dwidenoise " + title + "_dwi.mif " + title + "_den.mif -noise noise.mif")


    #4. Distortion Correction ===============================================
    scripts.set_context(1)
    scripts.do("mrconvert dwi_" + title + "_PA.nii.gz ../../../dataset/instance_files/PA.mif")
    
    scripts.do("mrconvert ../../../dataset/instance_files/PA.mif -fslgrad dwi_" + title + "_PA.bvec dwi_" + title + "_PA.bval - | mrmath - mean ../../../dataset/instance_files/mean_b0_PA.mif -axis 3")
    
    scripts.set_context(2)
    scripts.do("dwiextract " + title + "_den.mif - -bzero | mrmath - mean mean_b0_AP.mif -axis 3")

    scripts.do("mrcat mean_b0_AP.mif mean_b0_PA.mif -axis 3 b0_pair.mif")

    #5. Preprocessing ===============================================
    scripts.do("dwifslpreproc " + title + "_den.mif " + title + '_den_preproc.mif -nocleanup -pe_dir AP -rpe_pair -se_epi b0_pair.mif -eddy_options " --slm=linear --data_is_shelled"')

    #6. Bias field correction ===============================================
    scripts.do("dwibiascorrect ants " + title + "_den_preproc.mif " + title + "_den_preproc_unbiased.mif -bias bias.mif")
    

    #Copy final output file to "main files"
    scripts.do("cp " + title + "_den_preproc_unbiased.mif .." + dataset + "/main_files")
    
    scripts.do("mrconvert " + title + "_den_preproc_unbiased.mif original_preproc.nii.gz -datatype float32")
    scripts.do("cp original_preproc.nii.gz .." + dataset + "/main_files")
    scripts.do("mv original_preproc.nii.gz conversions")
    scripts.do("cp T1w_" + title + ".nii.gz ../bundleframe/Register_T1")