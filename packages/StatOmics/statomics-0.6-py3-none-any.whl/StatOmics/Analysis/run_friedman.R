# Friedman's test for non-normal and paired data
library(dplyr)
library(matrixStats)
# library(tidyverse)
# library(Hmisc)
# library(ggplot2)
library(tidyr)
# library(VIM)
# library(mice)
# library(caret)
# library(tidyr)
# library(car)

run_friedman_test <- function(data, group_info = NULL) {
  
  character_cols <- data %>% select(where(is.character))
  numeric_data <- data %>% select(where(is.numeric))
  
  if (!is.null(group_info)) {
    
    if (length(group_info) != ncol(numeric_data)) {
      stop("Length of group_info must match the number of numeric columns")
    }
    
    group_info <- unname(unlist(group_info))
    
  } else {
    
    group_info <- sub("_.*", "", colnames(numeric_data))
    
  }
  
  # Initialize results dataframe
  results <- data.frame(
    Protein = character(),
    statistic = numeric(),
    p_value = numeric(),
    stringsAsFactors = FALSE
  )
  
  # do Friedman test for each feature
  for (i in 1:nrow(data)) {
    protein <- data[i, 1]  # First column is the protein identifier
    
    each_test <- long_sample %>%
      filter(Protein == protein)  # Ensure proper filtering
    
    # Check if both groups have sufficient samples
    group_counts <- each_test %>% group_by(Group) %>% summarise(n = sum(!is.na(Value)))
    
    if (any(group_counts$n < 4)) {
      warning(paste("Skipping", protein, "- insufficient sample size (need at least", 4, "per group)"))
      results <- rbind(results, data.frame(Protein = protein, statistic = NA, p_value = NA))
      next
    }
    
    # Perform Friedman test
    test <- tryCatch({
      friedman.test(Value ~ Group, data = each_test)
    }, error = function(e) {
      warning(paste("Error in Mann-Whitney U-test:", e$message))
      return(NULL)
    })
    
    if (!is.null(test)) {
      results <- rbind(results, data.frame(
        Protein = protein,
        statistic = test$statistic,
        p_value = test$p.value
      ))
    } else {
      results <- rbind(results, data.frame(
        Protein = protein,
        statistic = NA,
        p_value = NA
      ))
    }
  }
  
  final_results <- left_join(character_cols, results, by = "Protein")
  
}