import scripts

def action():
    homepath, dataset, title, tempfiles, current_path, bundlepath = scripts.state()
    scripts.set_context(tempfiles)

    #
    # Generates Fiber Orientation Distribution
    #

    #7. Computing (average) tissue response functions ===============================================
    scripts.do("dwi2response dhollander " + title + "_den_preproc_unbiased.mif wm.txt gm.txt csf.txt -voxels voxels.mif")

    #8. Unique response functions ===============================================
    scripts.mkdir(tempfiles + "../avgresponse")
    scripts.do("responsemean wm.txt ../avgresponse/group_average_response_wm.txt")
    scripts.do("responsemean gm.txt ../avgresponse/group_average_response_gm.txt")
    scripts.do("responsemean csf.txt ../avgresponse/group_average_response_csf.txt")

    #9. Upsampling DW images ===============================================
    scripts.do("mrgrid " + title + "_den_preproc_unbiased.mif regrid -vox 1.00 " + title + "_den_preproc_unbiased_upsampled.mif")

    #10. Computer upsampled brain mask images ===============================================
    scripts.do("dwi2mask " + title + "_den_preproc_unbiased_upsampled.mif mask.mif")

    #11. Fiber Orientation Distribution  estimation ===============================================
    scripts.do("dwi2fod msmt_csd " + title + "_den_preproc_unbiased_upsampled.mif ../avgresponse/group_average_response_wm.txt wmfod.mif ../avgresponse/group_average_response_gm.txt gm.mif ../avgresponse/group_average_response_csf.txt csf.mif -mask mask.mif")

    #12. Joint bias field correction and intensity normalization ===============================================
    scripts.do("mtnormalise wmfod.mif wmfod_norm.mif gm.mif gm_norm.mif csf.mif csf_norm.mif -mask mask.mif")

    # Concatenate files for viewing
    scripts.do("mrconvert -coord 3 0 wmfod_norm.mif - | mrcat csf_norm.mif gm_norm.mif - vf.mif")
    #Viewing: mrview vf.mif -odf.load_sh wmfod.mif