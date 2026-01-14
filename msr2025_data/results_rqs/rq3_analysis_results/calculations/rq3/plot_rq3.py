# import json
# import pandas as pd
# import matplotlib.pyplot as plt
# import numpy as np
# from glob import glob


# data = {}
# for file in glob('rq3_results_*.json'):
#     with open(file) as f:
#         cluster_data = json.load(f)
#         cluster = list(cluster_data.keys())[0]
#         data[cluster] = cluster_data[cluster]

# # RQ3-1: Grouped Bar Chart (Release Adoption & Consistency)

# rq1_df = pd.DataFrame({cluster: [
#     data[cluster]['rq3-1']['releases'],
#     data[cluster]['rq3-1']['consistency']
# ] for cluster in data}).T
# rq1_df.columns = ['Releases', 'Consistent Version']

# plt.figure(figsize=(12, 6))
# x = np.arange(len(rq1_df))
# width = 0.35

# bars1 = plt.bar(x - width/2, rq1_df['Releases'], width, 
#                color='#1f77b4', label='Releases', edgecolor='none')
# bars2 = plt.bar(x + width/2, rq1_df['Consistent Version'], width, 
#                color='#ff7f0e', label='Consistent Version', edgecolor='none')

# plt.title('RQ3-1: Release Adoption & Consistency', pad=20)
# plt.xlabel('Research Cluster')
# plt.ylabel('Percentage (%)')
# plt.xticks(x, rq1_df.index.str.upper())
# plt.ylim(0, 100)
# plt.grid(axis='y', alpha=0.3)

# for bars in [bars1, bars2]:
#     for bar in bars:
#         height = bar.get_height()
#         plt.text(bar.get_x() + bar.get_width()/2, height,
#                  f'{height:.1f}%',
#                  ha='center', va='bottom',
#                  color='black')

# plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
# plt.tight_layout()
# plt.show()

# # RQ3-2: Small Multiples (Versioning Types)

# version_types = ['semantic', 'calendar', 'Alphanumeric', 'other']
# colors = ['#2ca02c', '#ff7f0e', '#1f77b4', '#d62728']
# labels = ['Semantic', 'Calendar', 'Alphanumeric', 'Other']

# fig, axs = plt.subplots(1, len(data), figsize=(18, 6), sharey=True)
# plt.suptitle('RQ3-2: Versioning Type Adoption by Cluster', y=1.05, fontsize=14)

# for idx, (cluster, ax) in enumerate(zip(data.keys(), axs)):
#     cluster_data = data[cluster]['rq3-2']
#     values = [cluster_data[vt] for vt in version_types]
    
#     filtered_labels = [lab for lab, val in zip(labels, values) if val > 0]
#     filtered_values = [val for val in values if val > 0]
#     filtered_colors = [col for col, val in zip(colors, values) if val > 0]
    
#     bars = ax.bar(filtered_labels, filtered_values, 
#                  color=filtered_colors, edgecolor='none')
#     ax.set_title(cluster.upper(), pad=15)
#     ax.set_ylim(0, 100)
#     ax.grid(axis='y', alpha=0.3)
    
#     for bar in bars:
#         height = bar.get_height()
#         ax.text(bar.get_x() + bar.get_width()/2, height,
#                 f'{height:.1f}%',
#                 ha='center', va='bottom',
#                 color='black')

# plt.tight_layout()
# plt.show()

import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from glob import glob

# Load data from JSON files
data = {}
for file in glob('rq3_results_*.json'):
    with open(file) as f:
        cluster_data = json.load(f)
        cluster = list(cluster_data.keys())[0]
        data[cluster] = cluster_data[cluster]

rq1_df = pd.DataFrame({cluster: [
    data[cluster]['rq3-1']['releases'],
    data[cluster]['rq3-1']['consistency']
] for cluster in data}).T
rq1_df.columns = ['Releases', 'Consistent Version']

plt.figure(figsize=(12, 6))
x = np.arange(len(rq1_df))
width = 0.35

bars1 = plt.bar(x - width/2, rq1_df['Releases'], width, 
               color='#1f77b4', label='Releases', edgecolor='none')
bars2 = plt.bar(x + width/2, rq1_df['Consistent Version'], width, 
               color='#ff7f0e', label='Consistent Version', edgecolor='none')

plt.title('RQ3-1: Release Adoption & Consistency', pad=20)
plt.xlabel('Research Cluster')
plt.ylabel('Percentage (%)')
plt.xticks(x, rq1_df.index.str.upper())
plt.ylim(0, 100)
plt.grid(axis='y', alpha=0.3)

for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, height,
                 f'{height:.1f}%',
                 ha='center', va='bottom',
                 color='black')

plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

# RQ3-2: Small Multiples

version_types = ['semantic', 'calendar', 'Alphanumeric', 'other']
labels = ['Semantic', 'Calendar', 'Alphanumeric', 'Other']
colors = ['#4c72b0', '#55a868', '#c44e52', '#ccb974']


fig, axs = plt.subplots(2, 2, figsize=(14, 10))
plt.suptitle('RQ3-2: Versioning Scheme Adoption Across Clusters', 
            y=0.98, fontsize=14)

axes = axs.flatten()

for idx, (cluster, ax) in enumerate(zip(data.keys(), axes)):
    cluster_data = data[cluster]['rq3-2']
    values = [cluster_data[vt] for vt in version_types]
    
    filtered_values = [v for v in values if v > 0]
    filtered_labels = [l for l, v in zip(labels, values) if v > 0]
    filtered_colors = [c for c, v in zip(colors, values) if v > 0]
    
    bars = ax.barh(filtered_labels, filtered_values, 
                  color=filtered_colors, height=0.6, edgecolor='none')
    
    ax.set_xlim(0, 100)
    ax.set_title(cluster.upper(), pad=12, fontsize=12, fontweight='semibold')
    ax.tick_params(axis='both', which='both', length=0)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    
    for bar in bars:
        width = bar.get_width()
        ax.text(width + 1, bar.get_y() + bar.get_height()/2,
                f'{width:.1f}%',
                va='center', ha='left',
                fontsize=10,
                color='#333333')

legend_items = [plt.Rectangle((0,0),1,1, color=colors[i], ec='none') 
               for i in range(len(labels))]
fig.legend(legend_items, labels,
          loc='upper center',
          ncol=4,
          bbox_to_anchor=(0.5, 0.96),
          frameon=False,
          fontsize=10)

plt.tight_layout()
plt.subplots_adjust(top=0.88, wspace=0.3, hspace=0.4)
plt.show()