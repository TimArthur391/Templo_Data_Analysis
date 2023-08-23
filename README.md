# Templo_Data_Analysis
Contemplas' montion analysis software Templo is routinely used for 2D gait analysis. The syncronisation with a ground reaction force vector provides clinicians with useful qualititive data regrading the location of the vector with respect to joint. However, it does not output any quantitative information. This tool takes the video file and forceplate metadata from Templo, and, with some user input, outputs approximate external joint moments.

Having these external joint moments helps give more evidence for clinical desicion making.

The software package is written in python 3.9, and uses the tkinkter, numpy and open CV libraries.