# load the astrochron package, please use version 1.2
library(astrochron)
library(readxl)

ex <- read_excel('Stack_untuned_uniform_age_exclusion_expanded_1172_removed_Hobart2023.xlsx')

# conduct an initial time-frequency analysis using 
#  evolutive harmonic analysis (eha).
#  use option 'genplot=4', which provides a useful normalization
#  for visualizing the stability of the bedding cycles and
#  evaluating changes in the relative dominance
eha(ex,win=500,fmax=0.1,ydir=-1,genplot=4,pl=2,ylab="Age (ka)",xlab="Frequency (cycles/ka)")

#  the astronomical target comes from Laskar et al. (2004)
# targetP contains the dominant obliquity term.
targetP=c(41.08463)
# targetE contains the amplitude modulation terms for obliquity.
targetE=c(174.8252,106.6098,97.08738)
#  we will use a 400 ka window.
res=eTimeOpt(ex,targetP=targetP,targetE=targetE,sedmin=80,sedmax=120,win=400,fitModPwr=F,flow=1/70,fhigh=1/25, roll=10^9, output=1,ydir=-1)			

# extract the optimal sedimentation rates from the eTimeOpt results
#  we will focus on the spectral power fit (middle panel in above figure),
#  which appears most reliable in this specific application.
sedrates=eTimeOptTrack(res[2])

# integrate the sedimentation rate history to create a depth-time map.
control=sedrate2time(sedrates)

# use the eTimeOpt depth-time map to 'tune' the oxygen isotope data.
#  note that we are extrapolating the sedimentation rate for the
#  lowermost and uppermost 200 ka of the data set.
dat2=tune(ex,control=control,extrapolate=T)

# interpolate to even sampling grid (use median sampling interval)
dat2_lin=linterp(dat2)

# conduct a new eha analysis on the tuned record
eha(dat2_lin,win=500,fmax=0.1,ydir=-1,genplot=4,pl=2,ylab="Age (ka)",xlab="Frequency (cycles/ka)")
