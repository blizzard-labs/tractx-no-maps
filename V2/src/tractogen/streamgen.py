import scripts

def action():
    homepath, dataset, title, tempfiles, current_path, bundlepath = scripts.state()
    scripts.set_context(tempfiles)
    
    scripts.do("tckgen -angle 22.5 -maxlen 250 -minlen 10 -power 1.0 wmfod_norm.mif -seed_image mask.mif -mask mask.mif -select 25000000 -cutoff 0.06 tracks_25_million.tck")
    scripts.do("tcksift tracks_25_million.tck wmfod_norm.mif tracks_2_million_sift.tck -term_number 2000000")
    
    scripts.tck2trk(tempfiles + "tracks_2_million_sift.tck", tempfiles + "../conversions/original_preproc.nii.gz", bundlepath + "/subjects/" + title + "/tracking.trk")
    
    
