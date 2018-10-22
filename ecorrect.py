#!/usr/bin/env python
import numpy as np
import sys
import warnings
import matplotlib.pyplot as plt
import os
from datetime import datetime
from numpy import nan
from matplotlib.patches import Rectangle

# Welcome page
def welcome_page():
    print ""
    print "================================ ecorrect ================================"
    print ""
    print "                             ...Description... "
    print ""
    print " ecorrect splits a target spectrum into chunks, and if chunks are part of "
    print " continuum regions then RMSE flux and mean error values are calculated "
    print " for each chunk. Data points and lines of best fit are plotted. RMSE flux "
    print " should be equal to mean error values from the error array. If not, a "
    print " scaling factor is given by which the error array should be scaled."
    print ""
    print " Red and orange markers indicate RMSE flux and mean error, respectively, "
    print " for saturated regions of absorption. These data points are not used in "
    print " calculating mean lines of best fit."
    print ""
    print "=========================================================================="
    print ""
    print " Usage:  ecorrect <ASCII spectum filename> [--options]"
    print ""
    print "=========================================================================="
    print ""
    print "                              ...Options... "
    print ""
    print "     --cc ....... : Followed by a percentage (e.g. 0.01). Chunks will be "
    print "     ............ : rejected as a continuum region if "
    print "     ............ : (1.0 - cc) < mean flux < (1.0 + cc). Default value "
    print "     ............ : is 0.01"
    print "     --chunks.... : Followed by a chunk size. Spectrum will be split into"
    print "     ............ : this many chunks. Default number of chunks is 800."
    print "     --pix....... : Followed by a pixel number. Spectrum will be split "
    print "     ............ : into chunks of this pixel size."
    print "     --wav....... : Followed by a wavelength size in Angstroms. Spectrum "
    print "     ............ : will be split into chunks of this wavelength."
    print "     --s......... : Followed by a filetype: pdf, png or eps. This option "
    print "     ............ : bypasses the interactive plot and instead saves the "
    print "     ............ : plot to file."
    print ""
    print "=========================================================================="
    print ""

# Show welcome screen if ecorrect.py is only argument used
if len(sys.argv) == 1:
    welcome_page()
    quit()

# Help option
for i in range(len(sys.argv)):
    if sys.argv[i] == "--help":
        welcome_page()
        quit()

# Get the total number of args passed to the rms_flux_vs_mean_error.py
total = len(sys.argv)
 
# Get the arguments list 
cmdargs = str(sys.argv)

# Load user-input ASCII file as data
data = np.loadtxt(sys.argv[1])

# Remember filename
filename = sys.argv[1]

# Print args
#print ("The total numbers of args passed to the script: %d " % total)
#print ("Args list: %s " % cmdargs)

# Starting timer to calculate how long script takes to execute
startTime = datetime.now()
                                      
# define wav as col 1, flux as col 2, err as col 3 and cont as col 4 in data file
wav,flux,err,cont = data[:,0], data[:,1], data[:,2], data[:,3]

# Replace flux values of 0 with nan. This is important as regions or pixels cut from spectrum will
# produce spurious mean error values and flux values. If many pixels are cut from spectrum at short 
# intervals then all chunks of spectrum will be rejected by the mean flux filter.
# https://stackoverflow.com/questions/27778299/replace-zeros-in-a-numpy-array-with-nan
flux[flux==0.] = np.nan
err[err==0.] = np.nan

# np.nan has type 'float'. Need to reassign array types.
flux=flux.astype('float')
err=err.astype('float')

# subplots
fig,ax = plt.subplots()

# Default chunk size and continuum condition
chunks = 800
cc = 0.01

# Parse args for user input continuum condition and chunk size
for i in range(len(sys.argv)):
    if sys.argv[i] == '--cc':
        try:
            sys.argv[i+1] = float(sys.argv[i+1])
            cc = sys.argv[i+1]
        except IndexError:
            print "=========================================================================="
            print " No argument for --cc specified. Using default value of 0.01"
            print "=========================================================================="
    if sys.argv[i] == '--chunks':
        try:
            sys.argv[i+1] = int(sys.argv[i+1])
            chunks = sys.argv[i+1]
        except IndexError:
            print "=========================================================================="
            print " No argument for --chunks specified. Using default value of 800."
            print "=========================================================================="
    if sys.argv[i] == '--wav':
        try:
            sys.argv[i+1] = float(sys.argv[i+1])
            chunks = int((wav[-1] - wav[0])/(sys.argv[i+1]))
            print (wav[-1] - wav[0])/(sys.argv[i+1])
        except IndexError:
            print "=========================================================================="
            print " No argument for --wav specified. Using default calculated from chunks."
            print "=========================================================================="
    if sys.argv[i] == '--pix':
        try:
            sys.argv[i+1] = float(sys.argv[i+1])
            chunks = int(len(data)/(sys.argv[i+1]))
            print chunks
        except IndexError:
            print "=========================================================================="
            print " No argument for --pix specified. Using default calculated from chunks."
            print "=========================================================================="

# Define chunk range as number of pixels / chunk size
pixel_start = 0
pixel_end = len(wav)/chunks
welcome_page()
print " Number of pixels in spectrum:", len(data)
wavstart = wav[0]
wavend = wav[-1]
total_wav = wavend - wavstart
print " Number of Angstroms in spectrum:", total_wav

# Calculate chunk size
chunksize = total_wav/chunks

# Create empty lists which will be used to calculate means since in the for loop mean values change
meanrmsept = []
meanrmsepto = []
meanerrpt = []
meanwavpt = []

meanrmsepts = []
meanrmseptos = []
meanerrpts = []
meanwavpts = []

meanfluxpt = []

print " Dividing spectrum into", chunks, "chunks."
print " Each chunk is", chunksize,"Angstroms in size."
print " Each chunk is", len(data)/chunks,"pixels in size."
print " Chunk is rejected if", 1. - cc, " < mean flux <", 1. + cc

# Loop over chunks, building lists of RMSE of flux points and mean wavelength point at that chunk given certain conditions
for num in range(0,chunks):
    with warnings.catch_warnings(): # Supress warnings from calculating means of empty chunks
# Lists below are for chunks of pure continuum
        warnings.simplefilter("ignore", category=RuntimeWarning)
        meanwav = np.nanmean(wav[pixel_start:pixel_end])
        meanerr = np.nanmean(err[pixel_start:pixel_end]) # Calculate mean error for one chunk
        meanflux = np.nanmean(flux[pixel_start:pixel_end]) # Calculate mean flux for one chunk
        rmsflux = ((1./(len(wav)/chunks))*(np.nansum(np.square(flux[pixel_start:pixel_end]-1))))**0.5 #Calculate RMSE flux for one chunk
# Lists below are only for chunks at the bases of saturated absorption features
        meanwavs = np.nanmean(wav[pixel_start:pixel_end])
        meanerrs = np.nanmean(err[pixel_start:pixel_end]) # Calculate mean flux for one chunk
        meanfluxs = np.nanmean(flux[pixel_start:pixel_end]) # Calculate mean flux for one chunk
        rmsfluxs = ((1./(len(wav)/chunks))*(np.nansum(np.square(flux[pixel_start:pixel_end]-0))))**0.5 #Calculate RMSE flux for one chunk
# If (1.0 - cc) < mean flux < (1.0 + cc) then plot markeres for RMSE flux and mean error
# This avoids using segments which are not pure continuum. Mean error < 1 cuts out outliers
# from spectrum articacts.
        if (1. + cc) > meanflux > (1. - cc): 
# Subaru spectra have continuum set to 1 for sections of spectrum with no data. This condition prevents 
# those points from being included in lists
                if meanflux != 1. and meanerr < 1.:
                    meanwavpt.append(meanwav)
                    meanerrpt.append(meanerr)
                    meanrmsept.append(rmsflux)
# This section builds up points at saturated lines
        else:       
            if -cc < meanfluxs < cc: 
# Missing pixels in many spectra have their error value set to zero. This condition rejects a chunk 
# that is wholly composed of such regions
                if meanfluxs != 0. and meanerrs < 1.:
# Condition that does not include data points within 10% of edges of spectrum length
                    if wavstart+total_wav*0.1 < meanwavs < wavstart+total_wav*0.9:
                        meanwavpts.append(meanwavs)
                        meanerrpts.append(meanerrs)
                        meanrmsepts.append(rmsfluxs)
    pixel_start += len(wav)/chunks
    pixel_end += len(wav)/chunks

# Plots of points at saturated lines - NOTE NO OUTLIER REMOVAL PRESENT. Sections of spectra which have been 
# cut register as points with zero values for the error array. Additionally the error blows up at the red 
# end of the spectrum non-linearly. Both of these areas should not be used but since there are so few total 
# data points that are saturated it is difficult to remove then algorithmically.
meanerrplots = ax.plot(meanwavpts, meanerrpts,'ro', color='r')
rmscontplots = ax.plot(meanwavpts, meanrmsepts, 'ro', color='orange')

# Median filtering. Aim is to filter RMSE flux points and remove highly deviant points from list.
# Here I am replacing the mean with the more robust median and standard deviation with the absolute 
# distance from the mean. Distances are scaled by the median value so that the deviations are 
# on a reasonable relative scale.
mediancut = np.abs(meanrmsept - np.nanmedian(meanrmsept))
mdev = np.nanmean(mediancut)
dist_from_mean = mediancut/mdev
dist_from_mean2 = np.array(dist_from_mean).tolist()

# Removing common elements from lists for which RMSE flux > 3 median deviations from mean
var = (i for i,x in enumerate(dist_from_mean2) if x > 3)
for i in var:
    del dist_from_mean2[i]
    del meanwavpt[i]
    del meanerrpt[i]
    del meanrmsept[i]

# Mean error filtering. As above.
mediancut = np.abs(meanerrpt - np.nanmedian(meanerrpt))
mdev = np.nanmean(mediancut)
dist_from_mean = mediancut/mdev
dist_from_mean2 = np.array(dist_from_mean).tolist()

# Removing common elements from lists for which mean error > 3 median deviations from mean
var = (i for i,x in enumerate(dist_from_mean2) if x > 3)
for i in var:
    del dist_from_mean2[i]
    del meanwavpt[i]
    del meanerrpt[i]
    del meanrmsept[i]

# Plot RMSE flux points and mean error points. Deviation of RMSE flux points can be plotted  if required.
# dist_from_mean_plot = ax.plot(meanwavpt, dist_from_mean2, 'ro', color='m', label="Error distance\nfrom mean")
meanerrplot = ax.plot(meanwavpt, meanerrpt,'ro', color='b')
rmscontplot = ax.plot(meanwavpt, meanrmsept, 'ro', color='g')

# Calculate mean line of best fit for RMSE flux and mean error
meanerrline = [np.nanmean(meanerrpt) for i in meanerrpt]
meanrmseline  = [np.nanmean(meanrmsept) for i in meanrmsept]

# Pick out points from mean line of best fit
meanrmselineval = meanrmseline[0]
meanerrlineval = meanerrline[0]
error_scaling = meanrmselineval/meanerrlineval

print " Value of RMSE flux is", meanrmselineval
print " Value of mean error is", meanerrlineval

# Plot mean lines of best fit for RMSE flux and mean error
mean_line_rmse = ax.plot(meanwavpt, meanrmseline, linestyle='solid', color='g', label="Flux RMSE=%.4f" % meanrmselineval)
mean_line_err = ax.plot(meanwavpt, meanerrline, linestyle='solid', color='b', label = "Mean error=%.4f" % meanerrlineval)

# Invisible dummy line to make room in legend for text
dummylineplot = ax.plot(meanwavpt, meanrmseline, linewidth=0, label="Error array to be\nscaled by %.4f" % error_scaling)

# Plot lines of best fit to data
fit_meanrmseline = np.polyfit(meanwavpt, meanrmsept, 1)
fit_meanrmseline2 = np.poly1d(fit_meanrmseline)
fit_errline = np.polyfit(meanwavpt, meanerrpt, 1)
fit_errline2 = np.poly1d(fit_errline)

print " Equation of line of best fit for RMSE flux is:"
print fit_meanrmseline
print " Equation of line of best fit for mean error is:"
print fit_errline

# Plot equation of lines of best fit for RMSE flux and mean error
plt.plot(meanwavpt, fit_errline2(meanwavpt), '--k', color='b')
plt.plot(meanwavpt, fit_meanrmseline2(meanwavpt), '--k', color='g',)

print "=========================================================================="
print " Error array needs to be scaled by", meanrmseline[0]/meanerrline[0]
print "=========================================================================="

#print "Total time script processed for was", datetime.now() - startTime

plt.xlabel('Wavelength (Angstroms)')
plt.ylabel('Mean error and RMSE flux')
plt.locator_params(axis='x', nbins=15)
plt.locator_params(axis='y', nbins=15)
plt.title("Mean error and RMSE flux for %s" % filename)
plt.legend()

# Save to file options
for i in range(len(sys.argv)):
    if sys.argv[i] == "--s":
        try:
            if sys.argv[i+1] == "pdf":
                plt.savefig('ecorrect.pdf')
            if sys.argv[i+1] == "eps":
                plt.savefig('ecorrect.eps')
            if sys.argv[i+1] == "png":
                plt.savefig('ecorrect.png')
        except IndexError:
            print "=========================================================================="
            print " No argument for --s specified."
            print "=========================================================================="
        quit()

# Uncomment to show interactive plot
plt.show()

# Comment out when using interactive plot
#plt.savefig('ecorrect.pdf')
