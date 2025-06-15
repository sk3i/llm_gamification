import json
from collections import defaultdict
import matplotlib.pyplot as plt

with open('all_evaluation_results.json', 'r') as f:
    data = json.load(f)


# Grouping and summing scores
grouped = defaultdict(lambda: {
    "relevance": 0,
    "specificity": 0,
    "creativity": 0,
    "feasibility": 0,
    "alignment": 0,
    "count": 0
})

for item in data:
    pt = item["prompt_type"]
    grouped[pt]["relevance"] += item["relevance"]
    grouped[pt]["specificity"] += item["specificity"]
    grouped[pt]["creativity"] += item["creativity"]
    grouped[pt]["feasibility"] += item["feasibility"]
    grouped[pt]["alignment"] += item["alignment"]

    grouped[pt]["count"] += 1

# Calculate averages
averages = {}
for pt, scores in grouped.items():
    count = scores.pop("count")
    averages[pt] = {k: v / count for k, v in scores.items()}

# Define subplot grid size: 2 rows, 3 columns
rows, cols = 2, 3

fig, axs = plt.subplots(rows, cols, figsize=(18, 8))  # wider figure
axs = axs.flatten()

# Your naming convention order
expected_order = [
    'zer_bas', 'one_bas', 'few_bas',
    'zer_det', 'one_det', 'few_det'
]

for i, pt in enumerate(expected_order):
    ax = axs[i]
    if pt in averages:
        scores = averages[pt]
        labels = list(scores.keys())
        values = list(scores.values())
        ax.bar(labels, values, color='skyblue')
        ax.set_ylim(0, 5)  # Assuming 1-5 scale
        ax.set_title(f'Prompt Type: {pt}')
        ax.set_ylabel('Average Score')
        ax.grid(axis='y', linestyle='--', alpha=0.7)
    else:
        ax.axis('off')

# Hide any leftover axes if fewer than 6 prompt_types
for j in range(len(expected_order), rows * cols):
    axs[j].axis('off')

plt.tight_layout()
plt.show()