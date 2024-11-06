# -*- coding: utf-8 -*-
"""Plot_occurrence_rate.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1EkFs7Nf_hgUpbLx3LufwFi706B_HWhX9
"""

import pandas as pd

# Load the Excel file
file_path = './MCDI_word_counts_for_age_groups.xlsx'
xls = pd.ExcelFile(file_path)

# Age groups represented by their upper limits
age_groups = [3, 6, 9, 12, 18, 24, 30]

# Initialize empty dataframes
mcdi_df = pd.DataFrame()
non_mcdi_df = pd.DataFrame()

# Loop through each age group and process the data
for age in age_groups:
    # Load MCDI and All_Words data for the current age group
    mcdi_words = pd.read_excel(xls, sheet_name=f'{age}_MCDI_Words')
    all_words = pd.read_excel(xls, sheet_name=f'{age}_All_Words')

    # Add an Age_group column to both dataframes
    mcdi_words['Age_group'] = age
    all_words['Age_group'] = age

    # Append MCDI words to mcdi_df
    mcdi_df = pd.concat([mcdi_df, mcdi_words], ignore_index=True)

    # Filter out MCDI words from All_Words to get non-MCDI words
    non_mcdi_words = all_words[~all_words['Word'].isin(mcdi_words['Word'])]
    non_mcdi_df = pd.concat([non_mcdi_df, non_mcdi_words], ignore_index=True)

# Add a 'Category' column to distinguish MCDI and NON-MCDI data
mcdi_df['Category'] = 'MCDI'
non_mcdi_df['Category'] = 'NON-MCDI'

age_group_data = {
        'Age_group': [3, 6, 9, 12, 18, 24, 30],
        'Total Duration (min)': [1605.721667, 1912.675667, 2083.6075, 1511.8625, 1655.442667, 2105.196167, 1339.991167],
        'wake_time': [8, 8, 12, 12, 14, 14, 14]
    }

df_age_group = pd.DataFrame(age_group_data)

mcdi_df = pd.merge(df_age_group, mcdi_df, on='Age_group')
non_mcdi_df = pd.merge(df_age_group, non_mcdi_df, on='Age_group')

# Calculate the extended count
mcdi_df['extended count'] = (mcdi_df['wake_time'] * mcdi_df['Count']) / (mcdi_df['Total Duration (min)'] / 60)
non_mcdi_df['extended count'] = (non_mcdi_df['wake_time'] * non_mcdi_df['Count']) / (non_mcdi_df['Total Duration (min)'] / 60)

# Sort data by Word and Age_group to ensure cumulative calculation across age progression
mcdi_df = mcdi_df.sort_values(['Word', 'Age_group'])
non_mcdi_df = non_mcdi_df.sort_values(['Word', 'Age_group'])

# Calculate the cumulative count across age progression for each word in MCDI and NON-MCDI data
mcdi_df['Cumulative_count'] = mcdi_df.groupby('Word')['Count'].cumsum()
mcdi_df['Extended Cumulative_count'] = mcdi_df.groupby('Word')['extended count'].cumsum()

non_mcdi_df['Cumulative_count'] = non_mcdi_df.groupby('Word')['Count'].cumsum()
non_mcdi_df['Extended Cumulative_count'] = non_mcdi_df.groupby('Word')['extended count'].cumsum()

# Save the DataFrames to an Excel file with respective sheet names
output_file_path = './extended_count_for_age_groups.xlsx'
with pd.ExcelWriter(output_file_path) as writer:
    mcdi_df.to_excel(writer, index=False, sheet_name='MCDI_Words')
    non_mcdi_df.to_excel(writer, index=False, sheet_name='Non_MCDI_Words')

print(f"Data successfully saved to {output_file_path}")