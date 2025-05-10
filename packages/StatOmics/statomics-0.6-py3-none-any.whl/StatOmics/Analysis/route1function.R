# route1function.R

## Author: Tingyu Yin
## Date: April 25th, 2025
options(repos = c(CRAN = "https://cloud.r-project.org"))
library(dplyr)
library(tidyr)
library(fdrtool)

final_data_r1 <- function(norm_imputed_plasma, case_control, protein_gene) {
  
  # Prepare the long format for t-test
  data_long <- norm_imputed_plasma %>%
    pivot_longer(cols = where(is.numeric), names_to = "Patient", values_to = "Value") %>%
    mutate(Case_Control = case_control)
  
  test_column = "Protein"
  value_column = "Value"
  group_column = "Case_Control"
  unique_proteins <- unique(data_long[[test_column]])
  
  results <- lapply(unique_proteins, function(protein) {
    subset_data <- data_long %>%
      filter(!!sym(test_column) == protein)
    
    group1 <- subset_data %>% filter(!!sym(group_column) == "Case") %>% pull(!!sym(value_column))
    group2 <- subset_data %>% filter(!!sym(group_column) == "Control") %>% pull(!!sym(value_column))
    
    if (length(group1) > 1 && length(group2) > 1) {
      t_test_result <- tryCatch(
        t.test(group1, group2),
        error = function(e) NULL
      )
      
      if (!is.null(t_test_result)) {
        log2fd <- mean(group1, na.rm = TRUE) - mean(group2, na.rm = TRUE)
        mean_diff <- 2^mean(group1, na.rm = TRUE) - 2^mean(group2, na.rm = TRUE)
        
        return(data.frame(
          Protein = protein,
          t_statistic = t_test_result$statistic,
          p_value = t_test_result$p.value,
          log2fd = log2fd,
          mean_difference = mean_diff
        ))
      }
    }
    
    return(data.frame(
      Protein = protein,
      t_statistic = NA,
      p_value = NA,
      log2fd = NA,
      mean_difference = NA
    ))
  })
  
  # Combine results
  ttest_results <- bind_rows(results)
  
  # Merge with gene info
  ttest_results <- merge(protein_gene, ttest_results, by = "Protein")
  
  # Handle NA values
  ttest_results$p_value[is.na(ttest_results$p_value)] <- 1
  ttest_results$t_statistic[is.na(ttest_results$t_statistic)] <- 0
  
  # FDR adjustment
  derived_p <- 2 * pnorm(-abs(ttest_results$t_statistic))
  fdr_res <- fdrtool(derived_p, statistic = "pvalue", plot = FALSE)
  ttest_results$FDR <- fdr_res$lfdr
  ttest_results$q_value <- fdr_res$qval
  
  return(ttest_results)
}
