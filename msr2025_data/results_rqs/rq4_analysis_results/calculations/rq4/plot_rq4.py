import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from glob import glob

data = {}
for file in glob('rq4_results_*.json'):
    with open(file) as f:
        cluster_data = json.load(f)
        cluster = list(cluster_data.keys())[0]
        data[cluster] = cluster_data[cluster]


# RQ4-1: Stacked Bar Chart (Description Length)

rq1_df = pd.DataFrame({cluster: [
    data[cluster]['rq4-1']['long_desc'],
    data[cluster]['rq4-1']['short_desc'],
    data[cluster]['rq4-1']['None']
] for cluster in data}).T
rq1_df.columns = ['Long Description', 'Short Description', 'None']

plt.figure(figsize=(12, 6))
ax = rq1_df.plot(kind='bar', stacked=True, 
                color=['#4c72b0', '#55a868', '#c44e52'],
                edgecolor='none')  # No borders

plt.title('RQ4-1: Software Description Length Distribution', pad=20)
plt.xlabel('Research Cluster')
plt.ylabel('Percentage (%)')
plt.xticks(rotation=45)
plt.grid(axis='y', alpha=0.3)


for container in ax.containers:
    ax.bar_label(container, 
                label_type='center', 
                fmt='%.1f%%', 
                color='black',
                fontsize=10)

plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()


# RQ4-2: Grouped Bar Chart (License Adoption)

license_data = []
for cluster in data:
    license_data.append({
        'Cluster': cluster.upper(),
        'SPDX': data[cluster]['rq4-2']['spdx'],
        'Other': data[cluster]['rq4-2']['other'],
        'No License': data[cluster]['rq4-2']['no_license']
    })

license_df = pd.DataFrame(license_data)

plt.figure(figsize=(12, 6))
x = np.arange(len(license_df['Cluster']))
width = 0.25


colors = {
    'SPDX': '#2ca02c',
    'Other': '#ff7f0e',
    'No License': '#d62728'
}


bars1 = plt.bar(x - width, license_df['SPDX'], width, 
               label='SPDX', color=colors['SPDX'], edgecolor='none')
bars2 = plt.bar(x, license_df['Other'], width, 
               label='Other', color=colors['Other'], edgecolor='none')
bars3 = plt.bar(x + width, license_df['No License'], width, 
               label='No License', color=colors['No License'], edgecolor='none')

plt.title('RQ4-2: License Adoption Across Clusters', pad=20)
plt.xlabel('Research Cluster')
plt.ylabel('Percentage (%)')
plt.xticks(x, license_df['Cluster'])
plt.ylim(0, 100)
plt.grid(axis='y', alpha=0.3)


for bars in [bars1, bars2, bars3]:
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                 f'{height:.1f}%',
                 ha='center', va='bottom',
                 color='black')

plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()


# RQ4-3: Small Multiple Bar Charts (Documentation)

docs_df = pd.DataFrame({cluster: [
    data[cluster]['rq4-3']['requirements'],
    data[cluster]['rq4-3']['installation'],
    data[cluster]['rq4-3']['documentation']
] for cluster in data}).T
docs_df.columns = ['Requirements', 'Installation', 'Documentation']

fig, axes = plt.subplots(1, 3, figsize=(18, 6))
colors = ['#1f77b4', '#ff7f0e', '#2ca02c']

for idx, (col, ax) in enumerate(zip(docs_df.columns, axes)):
    bars = docs_df[col].plot(kind='bar', ax=ax, 
                            color=colors[idx], 
                            edgecolor='none')  
    ax.set_title(f'{col}', pad=15)
    ax.set_ylabel('Percentage (%)')
    ax.set_ylim(0, 100)
    ax.grid(axis='y', alpha=0.3)
    ax.set_xticklabels(docs_df.index, rotation=45)
    
    for bar in bars.patches:
        ax.annotate(f"{bar.get_height():.1f}%", 
                    (bar.get_x() + bar.get_width() / 2., bar.get_height()),
                    ha='center', va='center', 
                    xytext=(0, 5), 
                    textcoords='offset points',
                    color='black')

plt.suptitle('RQ4-3: Documentation Quality Across Clusters', y=1.02, fontsize=14)
plt.tight_layout()
plt.show()