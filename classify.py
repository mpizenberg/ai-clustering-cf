import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import normalize
from sentence_transformers import SentenceTransformer
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE

def main():
    # Load your data
    data = pd.read_json('aggregated_catalyst_data.json')

    # Load pre-trained SBERT model
    model = SentenceTransformer('all-MiniLM-L6-v2')
    # model = SentenceTransformer('dunzhang/stella_en_400M_v5', trust_remote_code=True)

    # Generate embeddings
    embeddings = model.encode(data['problem'].tolist(), show_progress_bar=True)

    # Normalize the embeddings
    embeddings = normalize(embeddings)

    # Perform K-means clustering
    n_clusters = 10  # adjust as needed
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    data['cluster'] = kmeans.fit_predict(embeddings)

    # Analyze results
    for i in range(n_clusters):
        cluster_data = data[data['cluster'] == i]
        print(f"Cluster {i}:")
        print(cluster_data['title'].tolist()[:5])  # Print first 5 titles in each cluster
        print("\n")

    # Dimensionality reduction for visualization
    tsne = TSNE(n_components=2, random_state=42)
    low_dim_embeds = tsne.fit_transform(embeddings)

    # Visualize
    plt.figure(figsize=(10, 8))
    scatter = plt.scatter(low_dim_embeds[:, 0], low_dim_embeds[:, 1], c=data['cluster'], cmap='viridis')
    plt.colorbar(scatter)
    plt.title('Cluster Visualization')
    plt.show()

if __name__ == "__main__":
    main()
