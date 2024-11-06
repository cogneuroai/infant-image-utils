MCDI_word_counts_for_age_groups.py [Input parameter required]
Input: transcriptions directory
output: MCDI_word_counts_for_age_groups.xlsx
This code takes the input parameter and process all the .srt files in the directory to get the word counts by grouping ages and writes the result to the output file.

MCDI_word_counts_for_each_age.py [Input parameter required]
Input: transcriptions directory
output: MCDI_word_counts_for_each_age.xlsx
This code takes the input parameter and process all the .srt files in the directory to get the word counts for each ages(without grouping the ages) and writes the result to the output file.

Consolidated_mcdi_word_counts_for_age_groups.py [Input parameter required]
Input: MCDI_word_counts_for_age_groups.xlsx
Output: Consolidated_mcdi_word_counts_for_age_group.xlsx
This code takes the input file and consolidates all the Summary sheets into a single output file.

Extended_count_for_age_groups.py [Input parameter hard-coded]
Input: MCDI_word_counts_for_age_groups.xlsx
Output: extended_count_for_age_groups.xlsx
This code takes the input file and calculates the extended_count (count considering wake_time), cumulative count, cumulative extended count for the age groups and writes the result to output file.

Extended_count_for_each_age.py [Input parameter hard-coded]
Input: MCDI_word_counts_for_each_age.xlsx
Output: extended_count_for_each_age.xlsx
This code takes the input file and calculates the extended_count (count considering wake_time), cumulative count, cumulative extended count for each age(without grouping the ages) and writes the result to output file.

Bookeh_plot_for_age_groups.py [Input parameter hard-coded]
Input: MCDI_word_counts_for_age_groups.xlsx
Output: bookeh_tab_layout.html

Bookeh_Exposures_VS_AoA.py [Input parameter hard-coded]
Input: MCDI_word_counts_for_each_age.xlsx
Output: Bookeh_Exposures_VS_AoA.html

