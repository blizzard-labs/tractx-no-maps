import scripts

def action():
    homepath, dataset, title, tempfiles, current_path, bundlepath = scripts.state()
    scripts.set_context(dataset + "dwi")    
                    
    #2. Convert raw data to .mif ===============================================
    scripts.do("mrconvert dwi_" + title + "_AP.nii.gz " + tempfiles + title + "_dwi.mif -fslgrad dwi_" + title + "_AP.bvec dwi_" + title + "_AP.bval")

    #3. Denoising the Dataset ===============================================
    scripts.set_context(tempfiles)
    scripts.do("dwidenoise " + title + "_dwi.mif " + title + "_den.mif -noise noise.mif")


    #4. Distortion Correction ===============================================
    scripts.set_context(dataset + "dwi")
    scripts.do("mrconvert dwi_" + title + "_PA.nii.gz " + tempfiles + "PA.mif")
    
    scripts.do("mrconvert "+ tempfiles + "PA.mif -fslgrad dwi_" + title + "_PA.bvec dwi_" + title + "_PA.bval - | mrmath - mean " + tempfiles + "mean_b0_PA.mif -axis 3")
    
    scripts.set_context(tempfiles)
    scripts.do("dwiextract " + title + "_den.mif - -bzero | mrmath - mean mean_b0_AP.mif -axis 3")

    scripts.do("mrcat mean_b0_AP.mif mean_b0_PA.mif -axis 3 b0_pair.mif")

    #5. Preprocessing ===============================================
    scripts.do("dwifslpreproc " + title + "_den.mif " + title + '_den_preproc.mif -nocleanup -pe_dir AP -rpe_pair -se_epi b0_pair.mif -eddy_options " --slm=linear --data_is_shelled"')

    #6. Bias field correction ===============================================
    scripts.do("dwibiascorrect ants " + title + "_den_preproc.mif " + title + "_den_preproc_unbiased.mif -bias bias.mif")
    

    #Copy final output file to "main files"    
    scripts.do("mrconvert " + title + "_den_preproc_unbiased.mif ../bundleseg/subjects/" + title + "/fa.nii.gz -datatype float32")