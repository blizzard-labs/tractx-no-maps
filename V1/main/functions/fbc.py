from . import scripts

def action(title):
    homepath = "/Users/krishna/Local/TractX"
    dataset = "/" + title

    scripts.set(dataset, homepath, 2)

    #
    # Finds weights of each fiber
    #
    
    scripts.do("tcksift2 tracks_2_million_sift.tck wmfod.mif siftweights.txt -proc_mask mask.mif")