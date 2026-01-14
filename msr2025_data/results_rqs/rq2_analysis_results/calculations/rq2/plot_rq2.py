import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from glob import glob

data = {}
for file in glob('rq2_results_*.json'):
    with open(file) as f:
        cluster_data = json.load(f)
        cluster_name = list(cluster_data.keys())[0]
        data[cluster_name] = cluster_data[cluster_name]

df = pd.DataFrame(data).T.reset_index().rename(columns={'index': 'Cluster'})
df = pd.melt(df, id_vars='Cluster', var_name='Metric', value_name='Percentage')

metric_labels = {'swh': 'Deposited in SWH', 'zenodo_doi': 'Zenodo DOI'}
df['Metric'] = df['Metric'].map(metric_labels)

plt.figure(figsize=(12, 6))
sns.set_theme(style="whitegrid")

ax = sns.barplot(
    x="Cluster",
    y="Percentage",
    hue="Metric",
    data=df,
    palette=["#4C72B0", "#DD8452"],
    edgecolor=".2"
)

for p in ax.patches:
    ax.annotate(
        f"{p.get_height():.1f}%",
        (p.get_x() + p.get_width() / 2., p.get_height()),
        ha='center', va='center',
        xytext=(0, 5),
        textcoords='offset points'
    )

plt.title("RQ2: Archival Infrastructure Adoption Across Clusters", pad=20, fontsize=14)
plt.xlabel("Research Cluster", labelpad=15)
plt.ylabel("Percentage (%)", labelpad=15)
plt.ylim(0, 100)
plt.legend(title='Metric', bbox_to_anchor=(1.05, 1), loc='upper left')

plt.tight_layout()
plt.show()