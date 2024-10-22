import pandas as pd
import numpy as np
from scipy import stats

# Constants
COST_BOX = 75
COST_TEST = 100
TESTS_PER_BOX = 6  # Number of tests per box

# Read the CSV data
df = pd.read_csv('L3158974.csv')

# Calculate average weight for each test
df['avg_weight'] = df[['n1', 'n2', 'n3', 'n4']].mean(axis=1)

# Random sampling: select TESTS_PER_BOX random tests per box
sampled_df = df.groupby('Box', group_keys=False).apply(lambda x: x.sample(n=min(TESTS_PER_BOX, len(x)), random_state=42))

# Group by Box and calculate the number of tests per box (which is now limited to 6)
tests_per_box = sampled_df['Box'].value_counts()

# Total cost calculation (now using fewer tests per box)
total_cost = tests_per_box.size * COST_BOX + len(sampled_df) * COST_TEST

# ANOVA test across boxes
f_stat, p_value = stats.f_oneway(*(sampled_df[sampled_df['Box'] == box]['avg_weight'] for box in sampled_df['Box'].unique()))

# Overall statistics for sampled data
overall_avg = sampled_df['avg_weight'].mean()
overall_std = sampled_df['avg_weight'].std()
overall_min = sampled_df['avg_weight'].min()
overall_max = sampled_df['avg_weight'].max()

# Detect outliers (3 standard deviations from the mean)
outliers = sampled_df[np.abs(sampled_df['avg_weight'] - overall_avg) > 3 * overall_std]

# Output results
print(f"Total cost of investigation: {total_cost} DKK")
print(f"Number of boxes tested: {tests_per_box.size}")
print(f"Total number of tests performed: {len(sampled_df)}")
print(f"\nOne-way ANOVA results:")
print(f"F-statistic: {f_stat:.2f}")  # Use f_stat instead of f_statistic
print(f"p-value: {p_value:.4f}")      # Use p_value for p-value

if p_value < 0.05:
    print("There is a statistically significant difference in average weights between boxes.")
else:
    print("No statistically significant difference in average weights between boxes.")

print(f"\nOverall average weight: {overall_avg:.2f}")
print(f"Standard deviation: {overall_std:.2f}")
print(f"Lowest average weight: {overall_min:.2f}")
print(f"Highest average weight: {overall_max:.2f}")

if not outliers.empty:
    print("\nOutliers detected:")
    print(outliers[['Box', 'Test', 'avg_weight']])
else:
    print("\nNo significant outliers detected.")
