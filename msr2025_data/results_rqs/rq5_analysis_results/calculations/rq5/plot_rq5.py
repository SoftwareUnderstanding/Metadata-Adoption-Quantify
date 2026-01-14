import json
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np  
from glob import glob

clusters = []
data = {'Bib': [], 'CFF': [], 'README': [], 'Total': []}

for file in glob('rq5_results_*.json'):
    with open(file) as f:
        cluster_data = json.load(f)
        cluster = list(cluster_data.keys())[0].upper()
        clusters.append(cluster)
        data['Bib'].append(cluster_data[cluster.lower()]['bib'])
        data['CFF'].append(cluster_data[cluster.lower()]['cff'])
        data['README'].append(cluster_data[cluster.lower()]['readme'])
        data['Total'].append(cluster_data[cluster.lower()]['total'])

df = pd.DataFrame(data, index=clusters)

sns.set_style("darkgrid")  
plt.figure(figsize=(14, 8))

palette = {
    'Bib': '#FF6B6B',
    'CFF': '#4ECDC4',
    'README': '#45B7D1',
    'Total': '#666666'
}

for metric in ['Bib', 'CFF', 'README', 'Total']:
    plt.plot(
        clusters, 
        df[metric], 
        marker='o', 
        markersize=10,
        linewidth=2.5,
        color=palette[metric],
        label=metric
    )
    for i, val in enumerate(df[metric]):
        plt.text(
            i, 
            val + 1.5, 
            f'{val:.1f}%', 
            ha='center', 
            color=palette[metric],
            fontweight='bold'
        )

plt.title('RQ5: Citation Practices Across Research Clusters', 
         fontsize=16, pad=20, fontweight='bold')
plt.ylabel('Percentage (%)', fontsize=12)
plt.ylim(0, 100)
plt.legend(loc='upper left', bbox_to_anchor=(1, 1), frameon=True)
plt.grid(True, alpha=0.4)

for spine in plt.gca().spines.values():
    spine.set_visible(False)

plt.tight_layout()
plt.show()