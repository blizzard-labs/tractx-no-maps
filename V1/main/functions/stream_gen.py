from . import scripts

def action(title):
    homepath = "/Users/krishna/Local/TractX"
    dataset = "/" + title
    scripts.set(dataset, homepath, 2)
    
    scripts.do("tckgen -angle 22.5 -maxlen 250 -minlen 10 -power 1.0 wmfod_norm.mif -seed_image mask.mif -mask mask.mif -select 25000000 -cutoff 0.06 tracks_25_million.tck")
    scripts.do("tcksift tracks_25_million.tck wmfod_norm.mif tracks_2_million_sift.tck -term_number 2000000")
    
    scripts.do("cp tracks_2_million_sift.tck .."+ dataset + "/main_files")
    
    scripts.tck2trk("tracks_2_million_sift.tck", "conversions/original_preproc.nii.gz", "sifttracts.trk")
    scripts.do("mv sifttracts.trk ../bundleframe" + dataset + "/Tracking")
    
