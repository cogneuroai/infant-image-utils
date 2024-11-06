**MCDI_word_counts_for_age_groups.py**  
**Input**: transcriptions directory  
**Output**: MCDI_word_counts_for_age_groups.xlsx  
This code takes the input parameter and processes all the `.srt` files in the directory to get the word counts by grouping ages and writes the result to the output file.

---

**MCDI_word_counts_for_each_age.py**  
**Input**: transcriptions directory  
**Output**: MCDI_word_counts_for_each_age.xlsx  
This code takes the input parameter and processes all the `.srt` files in the directory to get the word counts for each age (without grouping the ages) and writes the result to the output file.

---

**Consolidated_mcdi_word_counts_for_age_groups.py**  
**Input**: MCDI_word_counts_for_age_groups.xlsx  
**Output**: Consolidated_mcdi_word_counts_for_age_group.xlsx  
This code takes the input file and consolidates all the Summary sheets into a single output file.

---

**Extended_count_for_age_groups.py**  
**Input**: MCDI_word_counts_for_age_groups.xlsx (hard-coded)  
**Output**: extended_count_for_age_groups.xlsx  
This code takes the input file and calculates the extended count (count considering wake time), cumulative count, and cumulative extended count for the age groups, then writes the result to the output file.

---

**Extended_count_for_each_age.py**  
**Input**: MCDI_word_counts_for_each_age.xlsx (hard-coded)  
**Output**: extended_count_for_each_age.xlsx  
This code takes the input file and calculates the extended count (count considering wake time), cumulative count, and cumulative extended count for each age (without grouping the ages), then writes the result to the output file.

---

**Bookeh_plot_for_age_groups.py**  
**Input**: MCDI_word_counts_for_age_groups.xlsx (hard-coded)  
**Output**: bookeh_tab_layout.html  
This code takes the input file and generates a Bokeh plot with tabs layout for the age groups, saving the interactive plot as an HTML file.

---

**Bookeh_Exposures_VS_AoA.py**  
**Input**: MCDI_word_counts_for_each_age.xlsx (hard-coded)  
**Output**: Bookeh_Exposures_VS_AoA.html  
This code takes the input file and generates a Bokeh plot comparing exposures versus Age of Acquisition (AoA) and saves it as an HTML file.
