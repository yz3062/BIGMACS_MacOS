# Part 1
# load the astrochron package, please use version 1.2
library(astrochron)
library(astroBayes)

win_size = 400

# the error received was fixed when columns names are changed to position and value
dat=read.csv("Stack_untuned_uniform_age_exclusion_expanded_1172_removed_Hobart2023_global_interp_AstroBayes.csv", header=TRUE)
# convert "position" to millions of years
dat[c('position')] = dat[c('position')]/1000

# conduct an initial time-frequency analysis using 
#  evolutive harmonic analysis (eha).
#  use option 'genplot=4', which provides a useful normalization
#  for visualizing the stability of the bedding cycles and
#  evaluating changes in the relative dominance
amp_output = eha(dat,win=500,fmax=0.1,ydir=-1,genplot=4,pl=2,ylab="Age (ka)",xlab="Frequency (cycles/ka)", output=2)

dates = read.csv("AstroBayes_untuned_reversal_dates.csv", header=TRUE)
layers = read.csv("AstroBayes_untuned_layer_boundaries.csv", header=TRUE)
data("target_frequencies")

age_model <- astro_bayes_model(geochron_data = dates,
                               cyclostrat_data = dat,
                               target_frequency = target_frequencies,
                               layer_boundaries = layers,
                               iterations = 10000,
                               burn = 1000)

plot(age_model, type = 'age_depth')
plot(age_model, type = 'periodogram')