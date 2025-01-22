###############################################
# R script for processing a single BMA log file
# and computing posterior probabilities & logBF
###############################################

# 1) Install and load 'tidyverse' if not already installed
# install.packages("tidyverse")
library(tidyverse)

# 2) Read the log file (tab-delimited), ignoring lines starting with '#'
#    Adjust the file path as appropriate
log_file_path <- "../L86.log"
df <- read_tsv(log_file_path, comment = "#")

# 3) Inspect column names to confirm I and I_na fields are present
colnames(df)

# (Optional) Check total MCMC samples
n_total <- nrow(df)
print(paste("Total MCMC samples (including burn-in) =", n_total))

# 4) Define the burn-in fraction (example: 10%)
burnin_frac <- 0.1
start_idx <- floor(n_total * burnin_frac)

# Discard the first 10% of samples, keep the remaining 90%
df_post <- df %>%
  slice((start_idx + 1):n_total)

# 5) Map (I, I_na) to a specific ModelName
map_model <- function(I_val, I_na_val){
  dplyr::case_when(
    I_val == 0 & I_na_val == 0 ~ "Constant",
    I_val == 1 & I_na_val == 0 ~ "Exponential",
    I_val == 1 & I_na_val == 1 ~ "Exponential Expansion",
    I_val == 2 & I_na_val == 0 ~ "Logistic",
    I_val == 2 & I_na_val == 1 ~ "Logistic Expansion",
    I_val == 3 & I_na_val == 0 ~ "Gompertz (f0)",
    I_val == 3 & I_na_val == 1 ~ "Gompertz (f0) Expansion",
    TRUE ~ "Unknown"
  )
}

# 6) Count occurrences per model and compute posterior probabilities
df_posterior <- df_post %>%
  mutate(ModelName = map_model(I, I_na)) %>%
  group_by(ModelName) %>%
  summarise(Count = n()) %>%
  mutate(
    Posterior = Count / sum(Count)
  ) %>%
  arrange(desc(Posterior))

# Display posterior results
df_posterior

# 7) Identify the best model (highest posterior)
best_model <- df_posterior %>% slice_max(Posterior, n=1)
best_model_name <- best_model$ModelName
best_model_posterior <- best_model$Posterior
print(paste("Best model:", best_model_name, "with posterior =", best_model_posterior))

# 8) Compute logBF for each model relative to the best model
df_posterior <- df_posterior %>%
  mutate(
    logBF = if_else(
      Posterior > 0,
      log(Posterior / best_model_posterior),  # log(p_i / p_best)
      -Inf
    )
  )

# Final results: posterior probabilities and logBF
df_posterior

###############################################
# End of script
###############################################
