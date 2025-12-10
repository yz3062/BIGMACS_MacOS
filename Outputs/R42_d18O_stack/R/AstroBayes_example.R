library(astroBayes)

data("target_frequencies")
data("radioisotopic_dates")
data("cyclostratigraphic_data")
data("layer_boundaries")

age_model <- astro_bayes_model(geochron_data = dates,
                               cyclostrat_data = cyclostrat,
                               target_frequency = target_frequencies,
                               layer_boundaries = layer_boundaries,
                               iterations = 10000,
                               burn = 1000)

plot(age_model, type = 'age_depth')
plot(age_model, type = 'sed_rate')
plot(age_model, type = 'trace')