import os
from . import scripts

def action(title):
    homepath = "/Users/krishna/Local/TractX"
    dataset = "/" + title
    scripts.set(dataset, homepath, 2)

    # 
    # Warps FOD images to standard template space
    #
            
    #13. Register all FOD images to the template ===============================================
    scripts.do("mrregister wmfod_norm.mif -mask1 mask.mif ../template/FOD.mif -nl_warp subject2template_warp.mif template2subject_warp.mif")

    #14. Compute Template Mask ===============================================
    scripts.do("mrtransform mask.mif -warp subject2template_warp.mif -interp nearest -datatype bit dwi_mask_in_template_space.mif")
    scripts.do("mv dwi_mask_in_template_space.mif ../template/template_mask.mif")

    #15. Compute a white matter template analysis fixel mask ===============================================
    scripts.do("fod2fixel -mask ../template/template_mask.mif -fmls_peak_value 0.06 ../template/FOD.mif ../template/fixel_mask")

    #16. Warp FOD images to template space ===============================================
    scripts.do("mrtransform wmfod_norm.mif -warp subject2template_warp.mif -reorient_fod no fod_in_template_space_NOT_REORIENTED.mif")


    #Copy final output file to "main files"
    scripts.do("cp fod_in_template_space_NOT_REORIENTED.mif .."+ dataset + "/main_files")
    scripts.do("cp ../template/template_mask.mif .." + dataset + "/main_files")