import os
from . import scripts

def action(title):
    homepath = "/Users/krishna/Local/TractX"
    dataset = "/" + title
    scripts.set(dataset, homepath, 2)
    
    #
    # Reorients fixels
    #
    
    #18. Reorient Fixels ===============================================
    scripts.do("fixelreorient fixel_in_template_space_NOT_REORIENTED subject2template_warp.mif fixel_in_template_space")