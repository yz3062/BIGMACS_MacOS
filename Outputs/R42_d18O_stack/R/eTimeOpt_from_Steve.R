# Part 1
# load the astrochron package, please use version 1.2
library(astrochron)

win_size = 400

dat=read("Stack_untuned_uniform_age_exclusion_expanded_1172_removed_Hobart2023.csv")

# conduct an initial time-frequency analysis using 
#  evolutive harmonic analysis (eha).
#  use option 'genplot=4', which provides a useful normalization
#  for visualizing the stability of the bedding cycles and
#  evaluating changes in the relative dominance
eha(dat,win=500,fmax=0.1,ydir=-1,genplot=4,pl=2,ylab="Age (ka)",xlab="Frequency (cycles/ka)")

#  the astronomical target comes from Laskar et al. (2004)
# targetP contains the dominant obliquity term.
targetP=c(41.08463)
# targetE contains the amplitude modulation terms for obliquity.
targetE=c(174.8252,106.6098,97.08738)
#  we will use a 400 ka window.
res=eTimeOpt(dat,targetP=targetP,targetE=targetE,sedmin=80,sedmax=120,win=win_size,fitModPwr=F,flow=1/70,fhigh=1/25, roll=10^9, output=1,ydir=-1)			

# extract the optimal sedimentation rates from the eTimeOpt results
#  we will focus on the spectral power fit (middle panel in above figure),
#  which appears most reliable in this specific application.
sedrates=eTimeOptTrack(res[2])

# integrate the sedimentation rate history to create a depth-time map.
control=sedrate2time(sedrates)

# use the eTimeOpt depth-time map to 'tune' the oxygen isotope data.
#  note that we are extrapolating the sedimentation rate for the
#  lowermost and uppermost 200 ka of the data set.
dat2=tune(dat,control=control,extrapolate=T)

# anchor the floating time scale to the present
dat2[1]=dat2[1]-dat2[1,1]

# interpolate to even sampling grid (use median sampling interval)
dat2_lin=linterp(dat2)

# conduct a new eha analysis on the tuned record
eha(dat2_lin,win=500,fmax=0.1,ydir=-1,genplot=4,pl=2,ylab="Age (ka)",xlab="Frequency (cycles/ka)")

# compare oxygen isotope data on depth-derived and eTimeOpt timescales
plot(dat2_lin,type="l",col="red",xlab="Age (ka)",ylab="d18O", main="red=eTimeOpt timescale        black=depth-derived timescale"); lines(dat)

# this is a histogram of the temporal adjustments between the eTimeOpt and depth-derived timescales
hist(dat2[,1]-dat[,1],xlab="ka",main="Temporal adjustments")

# this is a plot of the difference between the eTimeOpt and depth-derived timescales at each datum
plot(dat2[,1],dat2[,1]-dat[,1],xlab="eTimeOpt timescale (ka)",ylab="eTimeOpt - depth derived timescale (ka)",main="Temporal adjustments")

plot(dat2[,1],dat2[,1]-dat[,1]-10.0614,xlab="eTimeOpt timescale (ka)",ylab="eTimeOpt - depth derived timescale (ka)",main="Temporal adjustments"); abline(h=0,lty=2)

dat3=tune(dat,control=control,extrapolate=F)
# anchor the floating time scale so that the youngest (non extrapolated) value is 200 ka
#### change the number below depending on window size #####
dat3[1]=dat3[1]+dat[win_size/2+1,1]
# interpolate to even sampling grid (use median sampling interval)
dat3_lin=linterp(dat3)
# compare oxygen isotope data on depth-derived and eTimeOpt timescales
plot(dat3_lin,type="l",col="red",lwd=1.5,xlab="Age (ka)",ylab="d18O", main="red=eTimeOpt timescale        black=depth-derived timescale"); lines(dat)

# take out dat first and last 200 observations to be comparable in length to dat3
# then find the age diff between dat and dat3
dat = dat[-(1:200),]
dat = dat[-(2372:2578),]
# diff = dat3[,1] - dat[,1]
output = cbind(dat3[,1], dat[,1])
output_df = as.data.frame(output)

# # save diff to excel
# library(writexl)
# write_xlsx(output_df, './untuned_intermediate_tuned_ages.xlsx')

# save data frames to excel
#### change the filename below depending on window size #####
# library(writexl)
# write_xlsx(dat3_lin, './tuned_stack_unextrapolated_win150.xlsx')

# # DOESN'T WORK
# # this is a plot of the difference between the uninterpolated eTimeOpt and depth-derived timescales at each datum
# plot(dat3[,1],dat3[,1]-dat[,1],xlab="eTimeOpt timescale (ka)",ylab="eTimeOpt - depth derived timescale (ka)",main="Temporal adjustments")