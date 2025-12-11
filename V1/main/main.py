import functions.pre_proc as pre_proc
import functions.sdTempMask as sdTemMask
import functions.fod_gen as fod_gen
import functions.fba as fba
import functions.id_bottle as id_bottle
import functions.reorient as reorient

displaytitle = '''

    __ __|                  |  \ \  /
       |   __|  _` |   __|  __| \  / 
       |  |    (   |  (     |      \ 
      _| _|   \__,_| \___| \__| _/\_\ 
      
=======================================================

Welcome to TractX, or the Streamlines Exclusion System for Accurate White Matter Reconstruction

*FEATURES*
    - Multi-tissue CSD Tractography
    - Fiber Density analysis for streamline matching in bottleneck regions

Credits: MRtrix, Nibabel, Dipy

=======================================================

'''
print(displaytitle)

title = input("Enter Title of the Dataset: ")
proceed = input("Once data is prepared, press [enter] to continue.")

pre_proc.action(title) #Pre-processing
fod_gen.action(title) #Generate FOD
sdTemMask.action(title) #Warp to Standard Template
reorient.action(title) # Reorient fixels


