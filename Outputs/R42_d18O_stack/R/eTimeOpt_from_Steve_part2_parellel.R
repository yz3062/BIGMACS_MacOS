# Part 2
# load the astrochron package, please use version 1.2
library(astrochron)
library(doFuture)

plan(multisession)

dat=read("Stack_untuned_uniform_age_exclusion_expanded_1172_removed_Hobart2023.csv")

# copy and paste the following function (‘runIt’) into the R console.
# the 'runIt' function will:
#  (1) conduct eTimeOpt given a specified targetP (recall that targetP contains the obliquity period!),
#  (2) track the sedimentation rate associated with the spectral power fit maximum,
#  (3) integrate the sedimentation rate curve.
#
# the function returns the resultant depth-time map.
#
# if you need to change any other eTimeOpt parameters, that must be done within the function.
# note that targetE and flow/high are hardwired, but will be ignored, as we are
# focusing on spectral power fit, and fitModPwr is set to F. 
runIt <- function(targetP)
{
  res=eTimeOpt(dat,targetP=targetP, targetE=c(174.8252,106.6098,97.08738),sedmin=80,sedmax=120,win=400,fitModPwr=F,flow=1/70,fhigh=1/25, roll=10^9, output=1,ydir=-1,genplot=F)                       	
  # extract the optimal sedimentation rates from the eTimeOpt results
  sedrates=eTimeOptTrack(res[2],genplot=F)
  # integrate the sedimentation rate history to create a depth-time map.
  control=sedrate2time(sedrates,genplot=F,check=F)
  return(cbind(control,sedrates[,2]))
}

# now we will run 1000 Monte Carlo simulations. we need to set up the matrices to store the results.
# nsim is the number of simulations to do
nsim=100
# nwin is the number of windows evaluated with eTimeOpt
nwin=238
# set up matrices for Monte Carlo results
depth<-double(nwin)
time<-double(nwin*nsim)
dim(time)<-c(nwin,nsim)
sr<-double(nwin*nsim)
dim(sr)<-c(nwin,nsim)

# draw nsim random samples from a Gaussian distribution, with mean value and standard
# deviation based on Waltham (2015) at 1388.5 ka.
obl=rnorm(n=nsim,mean=40.95,sd=0.1)
# plot histogram of obliquity periods for Monte Carlo simulation
hist(obl)

# now run the nsim Monte Carlo simulations
# I've only tried this for nsim=3 to make sure it works.
sim <- foreach(i = 1:nsim) %dofuture%
{
  cat("\n * simulation:", i, " obliquity=",obl[i],"\n")
  runIt(obl[i])
  # time[,i]=sim[,2]  
  # sr[,i]=sim[,3]  
}
# depth=sim[,1]

# from sim list to time, sr, and depth ####
for(i in 1:nsim)
{
  time[,i]=sim[[i]][,2]
  sr[,i]=sim[[i]][,3]
}
depth=sim[[1]][,1]

#Plotting ####
# the script below is for postprocessing and plotting results
# calculate standard deviation of age and sedimentation rate by row (window)
tsd=apply(time,1,sd)
srsd=apply(sr,1,sd)

# plot 2*standard deviation sedrate uncertainty by window
plot(2*srsd,type="l",lwd=2, col="red",xlab="Window Number",ylab="+/- 2 sigma uncertainty (correction factor)")

# calculate mean age and sedimentation rate by row (window)
tave=apply(time,1,mean)
srave= apply(sr,1,mean)

# plot 2*standard deviation timescale uncertainty by window
plot(2*tsd,type="l",lwd=2, col="red",xlab="Window Number",ylab="+/- 2 sigma uncertainty (ka)")

# plot depth derived times scale versus mean and 2*standard deviation of eTimeOpt-derived timescale
plot(tave,depth,type="l",lwd=2,ylim=c(2570,200),xlab="eTimeOpt-derived Timescale (ka)",ylab="Depth-derived Timescale (ka)")
lines(tave+2*tsd,depth,type="l",lwd=1,col="red")
lines(tave-2*tsd,depth,type="l",lwd=1,col="red")

# to add: plot all individual timescales from the Monte Carlo simulations

# save depth and tsd
output = cbind(depth, tsd)
output_df = as.data.frame(output)

# # save diff to excel
# library(writexl)
# write_xlsx(output_df, './untuned_intermediate_tuned_ages_uncertainty.xlsx')
