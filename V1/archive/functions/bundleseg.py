from ..functions import scripts
import nibabel as nib

def action(title):
    homepath = "/Users/krishna/Local/TractX"
    dataset = "/" + title
    scripts.set(dataset, homepath, 2)
    
    #Uses Tractseg- after fiber_density.py
    
    #scripts.do("fod2fixel wmfod_norm.mif fixel_dict -fmls_peak_value 0.1")
    #scripts.do("fixel2peaks fixel_dict peaks_dict.mif")
    
    #scripts.do("mrconvert peaks_dict.mif peaks_dict.nii.gz -datatype float32")
    
    '''
    peaks = nib.load("../../dataset/instance_files/peaks_dict.nii.gz").get_fdata()
    segmentation = run_tractseg(peaks)
    
    '''
    scripts.do("TractSeg -i original_preproc.nii.gz -o tract_output --bvals ../" + title + "/dwi/dwi_" + title+ "_AP.bval --bvecs ../" + title + "/dwi/dwi_" + title+ "_AP.bvec --raw_diffusion_input")
    
    scripts.set_context(3)
    #scripts.do("TractSeg -i peaks_dict.nii.gz")
    scripts.do("TractSeg -i peaks.nii.gz --output_type tract_segmentation")
    scripts.do("TractSeg -i peaks.nii.gz --output_type endings_segmentation")
    scripts.do("TractSeg -i peaks.nii.gz --output_type TOM ")
    scripts.do("Tracking -i peaks.nii.gz")
    
    