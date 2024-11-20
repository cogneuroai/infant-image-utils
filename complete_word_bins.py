#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 13:22:45 2024

@author: akashdas
"""

import os
import re
import pandas as pd
from collections import defaultdict
import json
import glob
import argparse
from utils import categories, month_intervals, calculate_month, get_month_group, bins, categorize_into_bins


def process_transcription_files(input_dir, output_json, output_excel):
    global categories
    global bins
    # Find all .srt files in the directory and subdirectories
    srt_files = glob.glob(os.path.join(input_dir, '**/*.srt'), recursive=True)

    # Create a list to store the filename and corresponding group
    file_group_data = []
    for srt_file_path in srt_files:
        filename = os.path.basename(srt_file_path)
        month = calculate_month(filename)
        group = get_month_group(month, month_intervals)
        file_group_data.append({'Filename': filename, 'Group': group})

    # Create a DataFrame from the data
    file_group_df = pd.DataFrame(file_group_data)
    file_group_df.sort_values(by='Group', inplace=True)

    # Dictionary to store word indices for each group and category with associated filenames
    group_word_indices = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

    subdirectories = ['first_half', 'second_half']
    for _, row in file_group_df.iterrows():
        filename = row['Filename']
        group = row['Group']

        # Check if the file has a .srt extension
        if not filename.endswith('.srt'):
            continue

        for subdirectory in subdirectories:
            full_path = os.path.join(input_dir, subdirectory, filename)

            if os.path.exists(full_path):
                with open(full_path, 'r', encoding='utf-8') as file:
                    # Read file content and filter out timestamp and numbering lines
                    lines = file.readlines()
                    file_content = ' '.join(
                        line.strip() for line in lines
                        if not re.match(r'^\d+$', line.strip()) and
                        not re.match(r'\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}', line.strip())
                    ).lower()
                    words_with_indices = [
                        (index, word) for index, word in enumerate(re.split(r'\W+', file_content)) if word
                    ]

                    word_count = 0
                    for category_name, words in categories.items():
                        for word in words:
                            pattern = r'\b' + re.escape(word) + r'\b'
                            indices = [index for index, w in words_with_indices if w == word]

                            if indices:
                                group_word_indices[group][filename][category_name].append({
                                    'Word': word,
                                    'Indices': indices
                                })
                                word_count += len(indices)

                    group_word_indices[group][filename]['word_count'] = word_count

    # Write results to a JSON file
    with open(output_json, 'w', encoding='utf-8') as json_file:
        json.dump(group_word_indices, json_file, indent=4)
    print('JSON is created')

    # Load the JSON data from the file
    with open(output_json, 'r', encoding='utf-8') as f:
        group_action_word_indices = json.load(f)

    # Dictionary to store index differences by bins for each group
    group_diff_bins = {}

    for group_id, srt_data in group_action_word_indices.items():
        group_diff_bins[group_id] = {}
        for srt_file, categories in srt_data.items():
            for category, words in categories.items():
                if category not in ['word_count', 'people']:
                    for word_data in words:
                        word = word_data['Word']
                        indices = word_data['Indices']
                        if len(indices) > 1:
                            differences = [indices[i] - indices[i-1] for i in range(1, len(indices))]
                            if word not in group_diff_bins[group_id]:
                                group_diff_bins[group_id][word] = {}
                            group_diff_bins[group_id][word][category] = categorize_into_bins(differences, bins)

    # Create a Pandas Excel writer using XlsxWriter as the engine
    with pd.ExcelWriter(output_excel, engine='xlsxwriter') as excel_writer:
        for group, words in group_diff_bins.items():
            data = []
            for word, categories in words.items():
                for category, bins in categories.items():
                    row = [word, category] + list(bins.values())
                    data.append(row)

            columns = ["Word", "Category"] + list(bins.keys())
            df = pd.DataFrame(data, columns=columns)
            df.to_excel(excel_writer, sheet_name=group, index=False)

    print('Excel is created')


def main():
    parser = argparse.ArgumentParser(description='Process transcription files and analyze word categories.')
    parser.add_argument('--input_dir', type=str, help='Path to the directory containing transcription files', required=True)
    parser.add_argument('--output_json', type=str, help='Path for the output JSON file', required=True)
    parser.add_argument('--output_excel', type=str, help='Path for the output Excel file', required=True)
    args = parser.parse_args()

    process_transcription_files(args.input_dir, args.output_json, args.output_excel)


if __name__ == "__main__":
    main()