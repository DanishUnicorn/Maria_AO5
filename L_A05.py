# First, we need to read and process the CSV data
# Then, we'll analyze the data to investigate if batches of dough (Lot numbers) give the same avg. weight in pastries
# We'll keep track of the costs as we analyze the data
# Then, we'll report our findings and the total cost of the investigation
# Finally, we'll write the results and propose an optimized solution

#---------------------------------------------------------------------------------------------------------------------------
# First we need to import the necessary libraries
import pandas as pd
import numpy as np
from scipy import stats

# Defining the known constants for the costs
COST_BOX = 75
COST_TEST = 100

# Read the CSV data
df = pd.read_csv('L3158974.csv')

# Calculate the average weight for each test
df['avg_weight'] = df[['n1', 'n2', 'n3', 'n4']].mean(axis=1)

# Group by Box and calculate the number of tests per box
tests_per_box = df.groupby('Box').size()

# Calculate total cost
total_cost = (len(tests_per_box) * COST_BOX) + (len(df) * COST_TEST)

# Perform one-way ANOVA to compare means across boxes
boxes = df['Box'].unique()
box_averages = [df[df['Box'] == box]['avg_weight'] for box in boxes]
f_statistic, p_value = stats.f_oneway(*box_averages)

print(f"Total cost of investigation: {total_cost} DKK")
print(f"Number of boxes tested: {len(tests_per_box)}")
print(f"Total number of tests performed: {len(df)}")
print(f"\nOne-way ANOVA results:")
print(f"F-statistic: {f_statistic}")
print(f"p-value: {p_value}")

if p_value < 0.05:
    print("\nThere is a statistically significant difference in average weights between boxes.")
else:
    print("\nThere is no statistically significant difference in average weights between boxes.")

# Calculate overall average weight, standard deviation, minimum, and maximum
overall_avg = df['avg_weight'].mean()
overall_std = df['avg_weight'].std()
overall_min = df['avg_weight'].min()
overall_max = df['avg_weight'].max()

print(f"\nOverall average weight: {overall_avg:.2f}")
print(f"Standard deviation: {overall_std:.2f}")
print(f"Lowest average weight: {overall_min:.2f}")
print(f"Highest average weight: {overall_max:.2f}")

# Identify any outliers (weights more than 3 standard deviations from the mean)
outliers = df[(df['avg_weight'] < overall_avg - 3 * overall_std) | (df['avg_weight'] > overall_avg + 3 * overall_std)]

if not outliers.empty:
    print("\nOutliers detected:")
    print(outliers[['Box', 'Test', 'avg_weight']])
else:
    print("\nNo significant outliers detected.")
