# package_test.R

library(limma)
library(ggplot2)

get_top_table <- function() {
  data <- matrix(rnorm(40), nrow=10)  # 10 genes × 4 samples
  design <- model.matrix(~ 0 + factor(c(1,1,2,2)))  # 4 columns
  colnames(design) <- c("Group1", "Group2")
  
  fit <- lmFit(data, design)
  contrast.matrix <- makeContrasts(Group2 - Group1, levels=design)
  fit2 <- contrasts.fit(fit, contrast.matrix)
  fit2 <- eBayes(fit2)
  topTable(fit2)
}

summarize_vector <- function(x) {
  # Ensure x is numeric
  if (!is.numeric(x)) stop("Input must be numeric")

  # Create a quick histogram plot (invisible, just using ggplot2 for dependency)
  p <- ggplot(data.frame(x=x), aes(x)) + geom_histogram()

  # Return a summary as a named list
  result <- list(
    mean = mean(x),
    sd = sd(x),
    min = min(x),
    max = max(x)
  )
  return(result)
}