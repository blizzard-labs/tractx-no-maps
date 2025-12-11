from . import scripts
import os
import nibabel as nib
import numpy as np

def action(title):
    homepath = "/Users/krishna/Local/TractX"
    dataset = "/" + title
    scripts.set(dataset, homepath, 2)
    '''
    #
    # Identifies bottleneck regions
    #
    
    #Finding number of fixels in each voxel
    scripts.do("fod2fixel wmfod_norm.mif fixel_dict -mask mask.mif")
    scripts.do("fixel2voxel fixel_dict count fixels_per_voxel.mif")
    
    #----------------------------------------
    scripts.set_context(4)
    scripts.do("./recobund.sh")
    scripts.set_context("/dataset/bundleframe" + dataset + "/rbx_folder")
    scripts.do("mrconvert model_to_subj_anatInverseWarped.nii.gz ../../../instance_files/bundleseg/m2s_inverse_warp.mif")
    scripts.set_context(5)
    '''
    
    #Convert to .tck format and create a fixel TDI map
    input_dir = homepath + "/dataset/bundleframe" + dataset + "/rbx_folder/multi_bundles"
    
    masks = []
    scripts.set_context(5)
    
    #Temporary, post TDI-generation variable generation
    for file in (os.listdir(input_dir)):
        if file.endswith(".trk"):
            tdi_map_image = "thr_TDI_" + file.replace('.trk', '') + ".mif"
            if (tdi_map_image != "thr_TDI_ICP_R.mif"):
                masks.append([tdi_map_image, "tdi_map/" + file.replace('.trk', '')])
    
    '''
    for file in (os.listdir(input_dir)):
        if file.endswith(".trk"):
            #Convert back into tck format
            nname = file.replace('.trk', '.tck')
            scripts.trk2tck(os.path.join(input_dir, file), nname)
            
            #Warp back to initial state
            warped = 'w' + nname
            scripts.do('tcktransform ' + nname + ' m2s_inverse_warp.mif ' + warped)
                        
            #Generate Fixel TDI Map
            tdi_map_image = "TDI_" + file.replace('.trk', '') + ".mif"
            fixel_location = "../tdi_map/" + file.replace('.trk', '')
            scripts.mkdir("/dataset/instance_files" + fixel_location.replace("..", ""))
            scripts.do("tck2fixel " + warped + " ../fixel_dict " + fixel_location + " " + tdi_map_image)
            
            #Threshold map to 5%
            thresh = int(scripts.do("mrstats " + fixel_location + "/" + tdi_map_image + " -output max")) * 0.05
            mask_path = fixel_location + "/thr_" + tdi_map_image
            scripts.do("mrthreshold " + fixel_location + "/" + tdi_map_image + " " + mask_path + " -abs " + str(thresh))
            
            masks.append([tdi_map_image, "tdi_map/" + file.replace('.trk', '')])
    '''
    scripts.set_context(2)
    
    fixel_attributes = []
    index_data_1D = []
    
    with open(homepath + "/dataset/instance_files/fixel_dict/index.txt", "r") as f:
        for line in f:
            index_data_1D += [line]
    
    index_data = np.reshape(index_data_1D, (240, 240, 150, 2))
    
    num_per_voxel = index_data[:, :, :, 0]
    first_indices = index_data[:, :, :, 1]
    
    for x in range(num_per_voxel.shape[0]):
        for y in range(num_per_voxel.shape[1]):
            for z in range(num_per_voxel.shape[2]):
                first_index = int(first_indices[x][y][z])
                for i in range(int(num_per_voxel[x][y][z])):
                    fixel_attributes.append([[first_index + i], [x, y, z], ["*0*"], []])
    
    print("=========================================")
    
    for image in masks:
        print(image[0])
        scripts.do("mrdump " + image[1] + "/" + image[0].replace('thr_', '') + " " + image[1] + "/" + image[0].replace('mif','txt').replace('thr_', ''))
        mask_data = []
        with open(homepath + "/dataset/instance_files/" + image[1] + "/" + image[0].replace('mif','txt').replace('thr_', '')) as f:
            for line in f:
                mask_data += [int(line)]        
        for fixel_ind in range(len(mask_data)):
            if mask_data[fixel_ind] != 0:
                #print(image[0].replace(".mif", ".txt"))
                fixel_attributes[fixel_ind][3].append(image[0].replace(".mif", ''))
                fixel_attributes[fixel_ind][2][0] = "*" + str(int(fixel_attributes[fixel_ind][2][0].replace('*', '')) + 1) + "*"
        
    print("=========================================")
    
    f = open("fixelattributes.txt", "w")
    for fixel in fixel_attributes:
        for attribute in fixel:
            for value in attribute:
                f.write(str(value))
                f.write("/")
            f.write(" | ")
        f.write("\n")
    f.close()