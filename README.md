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

Example output:  
  
Number of pixels in spectrum: 174533  
Number of Angstroms in spectrum: 4546.16526537  
Dividing spectrum into 800 chunks.  
Each chunk is 5.68270658172 Angstroms in size.  
Each chunk is 218 pixels in size.  
Chunk is rejected if 0.99  < mean flux < 1.01  
Value of RMSE flux is 0.117595487145  
Value of mean error is 0.0911740201817  
Equation of line of best fit for RMSE flux is:  
[  1.44730696e-06   1.07922478e-01]  
Equation of line of best fit for mean error is:  
[  2.52224239e-08   9.10054473e-02]  

![Example plot output (pdf image)](https://github.com/mwilczynska/ecorrect/files/2503987/ecorrect.pdf)
