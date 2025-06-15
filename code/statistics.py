import json
from collections import defaultdict
import matplotlib.pyplot as plt
import math

with open('all_evaluation_results.json', 'r') as f:
    data = json.load(f)

# Helper to parse prompt_type into parts (e.g., "zer_bas" -> ["zer", "bas"])
def split_prompt_type(pt):
    return pt.split('_')

# Enhanced grouping to store individual values for variance/stdev calculation
grouped = defaultdict(lambda: {
    "relevance": [],
    "specificity": [],
    "creativity": [],
    "feasibility": [],
    "alignment": []
})

group_bas_det = defaultdict(lambda: {
    "relevance": [],
    "specificity": [],
    "creativity": [],
    "feasibility": [],
    "alignment": []
})

group_zer_one_few = defaultdict(lambda: {
    "relevance": [],
    "specificity": [],
    "creativity": [],
    "feasibility": [],
    "alignment": []
})

# Collect all individual values
for item in data:
    pt = item["prompt_type"]
    # Store individual values by full prompt_type
    for key in ["relevance", "specificity", "creativity", "feasibility", "alignment"]:
        grouped[pt][key].append(item[key])
    
    # Parse parts
    parts = split_prompt_type(pt)
    if len(parts) == 2:
        shot, detail = parts
        # Store by bas vs det
        for key in ["relevance", "specificity", "creativity", "feasibility", "alignment"]:
            group_bas_det[detail][key].append(item[key])
        
        # Store by zer/one/few shot
        for key in ["relevance", "specificity", "creativity", "feasibility", "alignment"]:
            group_zer_one_few[shot][key].append(item[key])

# Function to compute statistics from list of values
def compute_statistics(group):
    stats = {}
    for g, value_lists in group.items():
        # Calculate means for each metric
        means = {}
        for metric, values in value_lists.items():
            means[metric] = sum(values) / len(values) if values else 0
        
        # Calculate overall averages for each data point (average across all 5 metrics per item)
        count = len(value_lists['relevance']) if 'relevance' in value_lists else 0
        overall_scores = []
        
        for i in range(count):
            item_avg = sum(value_lists[metric][i] for metric in ['relevance', 'specificity', 'creativity', 'feasibility', 'alignment']) / 5
            overall_scores.append(item_avg)
        
        # Calculate overall statistics
        if overall_scores:
            overall_mean = sum(overall_scores) / len(overall_scores)
            overall_variance = sum((x - overall_mean) ** 2 for x in overall_scores) / len(overall_scores)
            overall_stdev = math.sqrt(overall_variance)
        else:
            overall_mean = overall_variance = overall_stdev = 0
        
        stats[g] = {
            'means': means,
            'overall_mean': overall_mean,
            'overall_variance': overall_variance,
            'overall_stdev': overall_stdev,
            'count': count
        }
    
    return stats

# Compute statistics for all groups
stats_full = compute_statistics(grouped)
stats_bas_det = compute_statistics(group_bas_det)
stats_zer_one_few = compute_statistics(group_zer_one_few)

# Helper function to print statistics nicely
def print_statistics(stats_dict, title):
    print(f"{title}:\n")
    for category, stats in stats_dict.items():
        print(f"{category.capitalize()}:")
        # Print individual metric means
        for metric, mean_val in stats['means'].items():
            print(f"  {metric}: {mean_val:.3f}")
        # Print overall statistics
        print(f"  Overall Mean: {stats['overall_mean']:.3f}")
        print(f"  Overall Std Dev: {stats['overall_stdev']:.3f}")
        print(f"  Overall Variance: {stats['overall_variance']:.3f}")
        print(f"  Count: {stats['count']}")
        print()

# Print results
print_statistics(stats_bas_det, "1. Statistics for Basic vs Detailed")
print_statistics(stats_zer_one_few, "2. Statistics for Zero vs One vs Few Shot")
print_statistics(stats_full, "3. Statistics per Prompt Type")