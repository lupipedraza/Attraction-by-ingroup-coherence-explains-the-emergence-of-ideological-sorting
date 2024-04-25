# Load necessary libraries
library(readr)
library(lme4)
library(ggplot2)

# Load the dataset
setwd(dirname(rstudioapi::getActiveDocumentContext()$path))
surveyData <- read_csv("SurveyResponses.csv")

# We prepare the survey data for the linear model
surveyData$isPolitical <- as.factor(surveyData$isPolitical)
surveyData$rating <- as.integer(surveyData$rating)
# Run the linear mixed-effects model on the  data
model <- lmer(rating ~ isPolitical + (1|ID), data = surveyData)
summary(model)

# Calculate mean and SEM of rating for each isPolitical category
summary_stats <- surveyData %>%
  dplyr::group_by(isPolitical) %>%
  dplyr::summarise(
    mean_rating = mean(rating, na.rm = TRUE),
    sem_rating = sd(rating, na.rm = TRUE) / sqrt(dplyr::n())
  )


# Load the dataset with the k-values per each dataset
datasets_k = read_csv("Ks_final.csv")
datasets_k$k_avg <- (datasets_k$k_inf + datasets_k$k_sup) / 2

# We compute the mean and sem values per dataset
average_rating_per_label <- surveyData %>%
  dplyr::group_by(label) %>%
  dplyr::summarise(
    average_rating = mean(rating, na.rm = TRUE),
    SEM = sd(rating, na.rm = TRUE) / sqrt(n())
  )
# We order the values
ordered_labels <- c("ANES16", "ANES20", "TEDX_A", "TEDX_B", "COVID", "PEW_P", "TEDX_H", "PEW_H")
average_rating_per_label <- average_rating_per_label %>%
  dplyr::mutate(label = factor(label, levels = ordered_labels)) %>%
  dplyr::arrange(label)

# We duplicate the rows for "COVID" and "TEDX_H" as they corresponde to multiple values of K
covid_rows <- filter(average_rating_per_label, label == "COVID")
tedx_h_rows <- filter(average_rating_per_label, label == "TEDX_H")
# 3 additional "COVID" and 1 additional "TEDX_H"
additional_rows <- rbind(
  covid_rows,
  covid_rows,
  covid_rows,
  tedx_h_rows
)
average_rating_per_label_expanded <- bind_rows(average_rating_per_label, additional_rows)
# We reorder the dataframe based on the specified order, accounting for duplicates
average_rating_per_label_expanded <- average_rating_per_label_expanded %>%
  dplyr::mutate(label = factor(label, levels = ordered_labels)) %>%
  dplyr::arrange(label)

# Same procedure for the k values
average_rating_per_label_k <- datasets_k %>%
  dplyr::group_by(cohLabel) %>%
  dplyr::summarise(
    average_rating = mean(k_avg, na.rm = TRUE),
    SEM = mean((k_sup - k_inf) / 2, na.rm = TRUE)
  )

# We order the values and we only consider 12 out of the 16 datasets as these are the ones we have their perceived politicalness
ordered_groups <- c("cohAnes2016Binary", "cohAnes2020Binary", "cohZimmOnlinePolA", "cohZimmOnlinePolB","cohFreiraArg", "cohFreiraBra", "cohFreiraUSA", "cohFreiraUru", "cohPew2020","cohZimmSt1NonPol", "cohZimmOnlineHedB", "cohPew2014")

average_rating_per_label_k <- average_rating_per_label_k %>%
  dplyr::mutate(cohLabel = factor(cohLabel, levels = ordered_groups)) %>%
  dplyr::arrange(cohLabel)
average_rating_per_label_k <- average_rating_per_label_k %>%
  slice(1:12)

# Now we are able to compute their correlation and plot them
plot_data <- data.frame(
  x_average_rating = average_rating_per_label_expanded$average_rating,
  x_SEM = average_rating_per_label_expanded$SEM,
  y_average_rating = average_rating_per_label_k$average_rating,
  y_SEM = average_rating_per_label_k$SEM
)
plot_data$label <- c("D10", "D15", "D9", "D11", "D8", "D14", "D5", "D6", "D13", "D3", "D4", "D2")

ggplot(plot_data, aes(x = x_average_rating, y = y_average_rating)) +
  geom_errorbar(aes(ymin = y_average_rating - y_SEM, ymax = y_average_rating + y_SEM), 
                width = 0.1, color = "darkgray", alpha = 0.8) +
  geom_errorbarh(aes(xmin = x_average_rating - x_SEM, xmax = x_average_rating + x_SEM), 
                 height = 0.05, color = "darkgray", alpha = 0.8) +
  geom_point(color = "black", size = 4, fill = "black", shape = 21) +
  geom_text(aes(label = label), nudge_x = 0.02, nudge_y = 0.02, check_overlap = TRUE) +
  xlab("Perceived politicalness") + 
  ylab("k") + 
  xlim(1,7) +
  ylim(min(0, min(plot_data$y_average_rating - plot_data$y_SEM)), max(plot_data$y_average_rating + plot_data$y_SEM)) +
  scale_x_continuous(breaks = 1:7) +
  theme_minimal(base_size = 14) + 
  theme(panel.background = element_rect(fill = "white", colour = "white"))

correlationResult = cor.test(plot_data$x_average_rating, plot_data$y_average_rating, method = "spearman", exact = FALSE)
print(correlationResult)
