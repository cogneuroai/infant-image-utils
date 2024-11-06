#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 13:22:45 2024

@author: akashdas
"""

import os
import re
import pandas as pd
from collections import defaultdict, Counter
import json
import glob
import argparse

parser = argparse.ArgumentParser(description='Process transcription files and analyze word categories.')
parser.add_argument('--input_dir', type=str, help='Path to the directory containing transcription files', required=True)
parser.add_argument('--output_json', type=str, help='Path for the output JSON file', required=True)
parser.add_argument('--output_excel', type=str, help='Path for the output Excel file', required=True)
args = parser.parse_args()

# Define the function to calculate the month based on the filename
def calculate_month(filename):
    weeks = int(filename[:3])
    months = weeks // 4
    return months

# Function to map a month to its interval group
def get_month_group(month, month_intervals):
    for group, interval in month_intervals.items():
        if month in interval:
            return group
    return None

# Define the month intervals for grouping
month_intervals = {
    3: [0, 1, 2, 3],
    6: [4, 5, 6],
    9: [7, 8, 9],
    12: [10, 11, 12],
    18: [13, 14, 15, 16, 17, 18],
    24: [19, 20, 21, 22, 23, 24],
    30: [25, 26, 27, 28, 29, 30]
}

# Directory path for the .srt files (replace with actual path)
directory_path = args.input_dir

# Find all .srt files in the directory and subdirectories
srt_files = glob.glob(os.path.join(directory_path, '**/*.srt'), recursive=True)

# Create a list to store the filename and corresponding group
file_group_data = []

# Calculate the group for each file
for srt_file_path in srt_files:
    filename = os.path.basename(srt_file_path)
    month = calculate_month(filename)
    group = get_month_group(month, month_intervals)
    file_group_data.append({'Filename': filename, 'Group': group})

# Create a DataFrame from the data
file_group_df = pd.DataFrame(file_group_data)
file_group_df.sort_values(by='Group')

#-------------------------------#
categories = {
    'action_words': [
        "bite", "blow", "break", "bring", "build", "bump", "buy", "carry", "catch", "chase",
        "clap", "clean", "climb", "close", "cook", "cover", "cry", "cut", "dance", "draw",
        "drink", "drive", "drop", "dry", "dump", "eat", "fall", "feed", "find", "finish",
        "fit", "fix", "get", "give", "go", "have", "hear", "help", "hide", "hit",
        "hold", "hug", "hurry", "jump", "kick", "kiss", "knock", "lick", "like", "listen",
        "look", "love", "make", "open", "paint", "pick", "play", "pour", "pretend", "pull",
        "push", "put", "read", "ride", "rip", "run", "say", "see", "shake", "share",
        "show", "sing", "sit", "skate", "sleep", "slide", "smile", "spill", "splash", "stand",
        "stay", "stop", "sweep", "swim", "swing", "take", "talk", "taste", "tear", "think",
        "throw", "tickle", "touch", "wait", "wake", "walk", "wash", "watch", "wipe", "wish",
        "work", "write"
    ],
    'animal_sounds': [
        "baa baa", "meow", "uh oh", "choo choo", "moo", "vroom", "cockadoodledoo", "ouch", "woof woof",
        "grr", "quack quack", "yum yum"
    ],
    'animals': [
        "alligator", "animal", "ant", "bear", "bee", "bird", "bug", "bunny", "butterfly", "cat",
        "chicken", "cow", "deer", "dog", "donkey", "duck", "elephant", "fish", "frog", "giraffe",
        "goose", "hen", "horse", "kitty", "lamb", "lion", "monkey", "moose", "mouse", "owl",
        "penguin", "pig", "pony", "puppy", "rooster", "sheep", "squirrel", "teddybear", "tiger",
        "turkey", "turtle", "wolf", "zebra"
    ],

    'vehicles':[
        "airplane", "bicycle", "boat", "bus", "car", "firetruck", "helicopter", "motorcycle", "sled",
        "stroller", "tractor", "train", "tricycle", "truck"
    ],

    'toys' : [
        "ball", "balloon", "bat", "block", "book", "bubbles", "chalk", "crayon", "doll", "game",
        "glue", "pen", "pencil", "play dough", "present", "puzzle", "story", "toy"
    ],

    'food_and_drink' : [
        "apple", "applesauce", "banana", "beans", "bread", "butter", "cake", "candy", "carrots", "cereal",
        "cheerios", "cheese", "chicken", "chocolate", "coffee", "coke", "cookie", "corn", "cracker", "donut",
        "drink", "egg", "fish", "food", "french fries", "grapes", "green beans", "gum", "hamburger", "ice",
        "ice cream", "jello", "jelly", "juice", "lollipop", "meat", "melon", "milk", "muffin", "noodles",
        "nuts", "orange", "pancake", "peanut butter", "peas", "pickle", "pizza", "popcorn", "popsicle", "potato",
        "potato chip", "pretzel", "pudding", "pumpkin", "raisin", "salt", "sandwich", "sauce", "soda/pop", "soup",
        "spaghetti", "strawberry", "toast", "tuna", "vanilla", "vitamins", "water", "yogurt"
    ],

    'clothing' : [
        "beads", "belt", "bib", "boots", "button", "coat", "diaper", "dress", "gloves", "hat",
        "jacket", "jeans", "mittens", "necklace", "pajamas", "pants", "scarf", "shirt", "shoe",
        "shorts", "slipper", "sneaker", "snowsuit", "sock", "sweater", "tights", "underpants", "zipper"
    ],

    'body_parts' : [
        "ankle", "arm", "belly button", "buttocks/bottom", "cheek", "chin", "ear", "eye", "face", "feet",
        "finger", "hair", "hand", "head", "knee", "leg", "lips", "mouth", "nose", "owie/boo boo", "penis",
        "shoulder", "tooth", "toe", "tongue", "tummy", "vagina"
    ],

    'small_household_items' : [
        "basket", "blanket", "bottle", "box", "bowl", "broom", "brush", "bucket", "camera", "can",
        "clock", "comb", "cup", "dish", "fork", "garbage", "glass", "glasses", "hammer", "jar",
        "keys", "knife", "lamp", "light", "medicine", "money", "mop", "nail", "napkin", "paper",
        "penny", "picture", "pillow", "plate", "plant", "purse", "radio", "scissors", "soap", "spoon",
        "tape", "telephone", "tissue/kleenex", "toothbrush", "towel", "trash", "tray", "vacuum", "walker", "watch"
    ],

    'furniture_and_rooms' : [
        "basement", "bathroom", "bathtub", "bed", "bedroom", "bench", "chair", "closet", "couch", "crib",
        "door", "drawer", "dryer", "garage", "high chair", "kitchen", "living room", "oven", "play pen",
        "porch", "potty", "refrigerator", "rocking chair", "room", "shower", "sink", "sofa", "stairs", "stove",
        "table", "TV", "washing machine", "window"
    ],

    'outside_things' : [
        "backyard", "cloud", "flag", "flower", "garden", "grass", "hose", "ladder", "lawn mower", "moon",
        "pool", "rain", "rock", "roof", "sandbox", "shovel", "sidewalk", "sky", "slide", "snow",
        "snowman", "sprinkler", "star", "stick", "stone", "street", "sun", "swing", "tree", "water", "wind"
    ],

    'places_to_go' : [
        "beach", "camping", "church", "circus", "country", "downtown", "farm", "gas station", "home", "house",
        "movie", "outside", "park", "party", "picnic", "playground", "school", "store", "woods", "work", "yard", "zoo"
    ],

    'people' : [
        "aunt", "baby", "babysitter", "babysitter's name", "boy", "brother", "child", "child's own name", "clown", "cowboy",
        "daddy", "doctor", "fireman", "friend", "girl", "grandma", "grandpa", "lady", "mailman", "man", "mommy", "nurse",
        "people", "person", "pet's name", "police", "sister", "teacher", "uncle"
    ],

    'games_and_routine' : [
        "bath", "breakfast", "bye", "call (on phone)", "dinner", "give me five!", "gonna get you!", "go potty", "hello", "hi",
        "lunch", "nap", "night night", "no", "patty cake", "peekaboo", "please", "shopping", "shh/shush/hush", "snack",
        "so big!", "thank you", "this little piggy", "turn around", "yes"
    ]
}


#file_path = '/Users/akashdas/Desktop/Professor Linda/Professor Zoran/filename_group_mapping.xlsx'
data = file_group_df

# Directory where the transcription files are stored
base_directory = directory_path
subdirectories = ['first_half', 'second_half']

# Dictionary to store word indices for each group and category with associated filenames
group_word_indices = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

for _, row in data.iterrows():
    filename = row['Filename']
    group = row['Group']
    
    # Check if the file has a .srt extension
    if not filename.endswith('.srt'):
        continue  # Skip files that are not .srt
    
    for subdirectory in subdirectories:
        full_path = os.path.join(base_directory, subdirectory, filename)
        
        if os.path.exists(full_path):
            with open(full_path, 'r', encoding='utf-8') as file:
                # Read file content and filter out timestamp and numbering lines
                lines = file.readlines()
                file_content = ' '.join(
                    line.strip() for line in lines 
                    if not re.match(r'^\d+$', line.strip()) and  # Exclude line numbers
                    not re.match(r'\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}', line.strip())  # Exclude timestamps
                ).lower()
                # Convert file_content into a list of words with index for each word
                words_with_indices = [(index, word) for index, word in enumerate(re.split(r'\W+', file_content)) if word]
                print(f"Words with indices for {filename}: {words_with_indices}")
                
                # Reset word count for each file
                word_count = 0
                print(filename)
                
                # Iterate over each category and word in the categories
                for category_name, words in categories.items():
                    for word in words:
                        pattern = r'\b' + re.escape(word) + r'\b'
                        
                        # Get indices where the word appears in the words_with_indices list
                        indices = [index for index, w in words_with_indices if w == word]
                        
                        if indices:
                            group_word_indices[group][filename][category_name].append({
                                'Word': word,
                                'Indices': indices
                            })
                            word_count += len(indices)  # Update count with the number of occurrences

                # Optionally store the word count for each file
                group_word_indices[group][filename]['word_count'] = word_count

# Write results to a JSON file
json_path = args.output_json
with open(json_path, 'w', encoding='utf-8') as json_file:
    json.dump(group_word_indices, json_file, indent=4)
print('JSON is created')

#----------------------------------------#

import json
import pandas as pd

# Load the JSON data from the file
json_filename = json_path
with open(json_filename, 'r', encoding='utf-8') as f:
    group_action_word_indices = json.load(f)

# Define bins for the index differences
bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 200, 300, 500, 1000]  # Extend this list if needed

# Function to categorize index differences into bins
def categorize_into_bins(differences, bins):
    bin_counts = {f"{bins[i]}-{bins[i+1]}": 0 for i in range(len(bins)-1)}
    bin_counts[f"{bins[-1]}+"] = 0
    for diff in differences:
        placed = False
        for i in range(len(bins) - 1):
            if bins[i] <= diff < bins[i + 1]:
                bin_counts[f"{bins[i]}-{bins[i+1]}"] += 1
                placed = True
                break
        if not placed:
            bin_counts[f"{bins[-1]}+"] += 1
    return bin_counts

# Dictionary to store index differences by bins for each group
group_diff_bins = {}

# Calculate index differences for each action word in each group and categorize them
for group_id, srt_data in group_action_word_indices.items():
    group_diff_bins[group_id] = {}
    for srt_file, categories in srt_data.items():
        for category, words in categories.items():
            if category not in ['word_count', 'people']:  # Exclude non-action word categories
                for word_data in words:
                    word = word_data['Word']
                    indices = word_data['Indices']
                    if len(indices) > 1:
                        differences = [indices[i] - indices[i-1] for i in range(1, len(indices))]
                        if word not in group_diff_bins[group_id]:
                            group_diff_bins[group_id][word] = {}
                        group_diff_bins[group_id][word][category] = categorize_into_bins(differences, bins)

# Create a Pandas Excel writer using XlsxWriter as the engine
excel_writer = pd.ExcelWriter(args.output_excel, engine='xlsxwriter')

# Iterate over each group and convert the nested dictionaries into a DataFrame
for group, words in group_diff_bins.items():
    # Flatten the dictionary to a list of tuples suitable for DataFrame creation
    data = []
    for word, categories in words.items():
        for category, bins in categories.items():
            row = [word, category] + list(bins.values())
            data.append(row)

    # Define the column names based on the bins keys from any category (all should be the same)
    columns = ["Word", "Category"] + list(bins.keys())
    
    # Create DataFrame and write to Excel
    df = pd.DataFrame(data, columns=columns)
    df.to_excel(excel_writer, sheet_name=group, index=False)

# Save the Excel file
excel_writer.close()
print('Excel is created')