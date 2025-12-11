from . import scripts

def action(title):
    homepath = "/Users/krishna/Local/TractX"
    dataset = "/" + title

    scripts.set(dataset, homepath, 2)

    #
    # Computes fiber density of given voxels
    #

    #17. Segment FOD images to estimate fixels and their apparent fiber density (FD) ===============================================
    scripts.do("fod2fixel -mask ../template/template_mask.mif fod_in_template_space_NOT_REORIENTED.mif fixel_in_template_space_NOT_REORIENTED -afd fd.mif")

    #18. Reorient Fixels ===============================================
    scripts.do("fixelreorient fixel_in_template_space_NOT_REORIENTED subject2template_warp.mif fixel_in_template_space")

    #19. Assign subject fixels to template fixels ===============================================
    scripts.do("fixelcorrespondence fixel_in_template_space/fd.mif ../template/fixel_mask ../template/fd PRE.mif")

    #20. Compute the fiber cross-section (FC) metric ===============================================
    scripts.do("warp2metric subject2template_warp.mif -fc ../template/fixel_mask ../template/fc IN.mif")
    scripts.do("mkdir ../template/log_fc")
    scripts.do("cp ../template/fc/index.mif ../template/fc/directions.mif ../template/log_fc")
    scripts.do("mrcalc ../template/fc/IN.mif -log ../template/log_fc/IN.mif")

    #21. Compute a combined measure of fiber density and cross-section (FDC) ===============================================
    scripts.do("mkdir ../template/fdc")
    scripts.do("cp ../template/fc/index.mif ../template/fdc")
    scripts.do("cp ../template/fc/directions.mif ../template/fdc")
    scripts.do("mrcalc ../template/fd/PRE.mif ../template/fc/IN.mif -mult ../template/fdc/IN.mif")
    scripts.do("cp -R ../template/fdc .." + dataset + "/main_files/fdc")