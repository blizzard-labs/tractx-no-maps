import scripts

def action():
    homepath, dataset, title, tempfiles, current_path, bundlepath = scripts.state()
    scripts.set_context(tempfiles)
    
    #Finding number of fixels in each voxel
    #scripts.do("fod2fixel wmfod_norm.mif ../fixel_dict -mask mask.mif")

    #Segment Bundles w/ RBX pipeline
    scripts.set_context(homepath + "src/idBottle/rbxpipeline")
    scripts.do("nextflow run main.nf --input=" + bundlepath + "subjects --atlas_directory=" + bundlepath + "rbxatlas")