import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import normalize
from sentence_transformers import SentenceTransformer
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter

def main():
    # Load your data
    data = pd.read_json('aggregated_catalyst_data.json')

    # Combine title and problem fields
    data['combined_text'] = data['title'] + " " + data['problem']

    # Load pre-trained SBERT model
    # model = SentenceTransformer('all-MiniLM-L6-v2')
    # model = SentenceTransformer('dunzhang/stella_en_400M_v5', trust_remote_code=True)
    model = SentenceTransformer('dunzhang/stella_en_1.5B_v5', trust_remote_code=True)

    # Generate embeddings
    embeddings = model.encode(data['combined_text'].tolist(), show_progress_bar=True)

    # Normalize the embeddings
    embeddings = normalize(embeddings)

    # Perform K-means clustering
    n_clusters = 10  # adjust as needed
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    data['cluster'] = kmeans.fit_predict(embeddings)

    # Analyze results and generate keywords
    for i in range(n_clusters):
        cluster_data = data[data['cluster'] == i]
        print(f"Cluster {i}:")
        print("Sample titles:")
        print(cluster_data['title'].tolist()[:5])  # Print first 5 titles in each cluster

        # Get keywords for the cluster
        cluster_texts = cluster_data['combined_text'].tolist()
        keywords = get_cluster_keywords(cluster_texts)
        print("Top keywords:", [word for word, score in keywords])
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


# Function to get top keywords for a cluster
def get_cluster_keywords(cluster_texts, n_keywords=5):
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(cluster_texts)
    feature_names = tfidf.get_feature_names_out()

    # Sum TF-IDF scores for each word across all documents in the cluster
    word_scores = tfidf_matrix.sum(axis=0).A1
    word_score_pairs = list(zip(feature_names, word_scores))

    # Sort words by score and return top n
    return sorted(word_score_pairs, key=lambda x: x[1], reverse=True)[:n_keywords]


if __name__ == "__main__":
    main()
