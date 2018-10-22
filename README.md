# ecorrect
ecorrect

============================================ ecorrect ============================================

                                               ...Description... 

 ecorrect splits a target spectrum into chunks, and if chunks are part of 
 continuum regions then RMSE flux and mean error values are calculated 
 for each chunk. Data points and lines of best fit are plotted. RMSE flux 
 should be equal to mean error values from the error array. If not, a 
 scaling factor is given by which the error array should be scaled.

 Red and orange markers indicate RMSE flux and mean error, respectively, 
 for saturated regions of absorption. These data points are not used in 
 calculating mean lines of best fit.

=================================================================================================

 Usage:  ecorrect [ASCII spectum filename] [--options]

=================================================================================================

                              ...Options... 

     --cc ....... : Followed by a percentage (e.g. 0.01). Chunks will be 
     ............ : rejected as a continuum region if 
     ............ : (1.0 - cc) < mean flux < (1.0 + cc). Default value 
     ............ : is 0.01
     --chunks.... : Followed by a chunk size. Spectrum will be split into
     ............ : this many chunks. Default number of chunks is 800.
     --pix....... : Followed by a pixel number. Spectrum will be split 
     ............ : into chunks of this pixel size.
     --wav....... : Followed by a wavelength size in Angstroms. Spectrum 
     ............ : will be split into chunks of this wavelength.
     --s......... : Followed by a filetype: pdf, png or eps. This option 
     ............ : bypasses the interactive plot and instead saves the 
     ............ : plot to file.

=================================================================================================
