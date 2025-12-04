from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from sklearn.neighbors import NearestNeighbors
import numpy as np
import umap
import hdbscan
from sklearn.metrics import silhouette_score
from sklearn.cluster import DBSCAN
from sklearn.cluster import KMeans

def build_frequency_matrix(df, card_col="tessera", product_col="descr_liv4", quantity_col="r_qta_pezzi"):
    """
    Costruisce una matrice tessere x prodotti aggregando le quantità acquistate per ogni tessera
    
    :param df: Dataframe dei dati
    :param card_col: Nome della colonna relativa alla tessera
    :param product_col: Nome della colonna relativa ai prodotti
    :param quantity_col: Nome della colonna relativa alla quantità dei prodotti
    """

    df_clean = df[df[card_col].notna() & (df[card_col] != "")]
    # Cast della tessera in stringa per evitare problemi di arrotondamento coi numeri grandi
    df_clean[card_col] = df_clean[card_col].astype(str).str.strip()
    
    grouped = df_clean.groupby([card_col, product_col])[quantity_col].sum()
    matrix = grouped.unstack(fill_value=0)
    row_totals = matrix.sum(axis=1)
    freq_matrix = matrix.div(row_totals.replace(0, 1), axis=0)
    return matrix

def apply_pca(df, num_components):
    """
    Applica ad un dataframe la riduzione PCA
    
    :param df: Dataframe dei dati
    :param num_components: Numeri di componenti della PCA
    """

    X = df.values  # converto in array
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    pca = PCA(n_components=num_components)
    X_pca = pca.fit_transform(X_scaled)
    return X_pca

def apply_umap(X, num_components):
   """
   Applica ad un dataframe la riduzione UMAP
   
   :param X: Dataframe dei dati
   :param num_components: Numeri componenti di UMAP
   """

   reducer = umap.UMAP(n_components=num_components, random_state=42)
   X_umap = reducer.fit_transform(X)
   return X_umap

def plot_data(X, title, x_label, y_label):
    """
    Disegna un plot per visualizzare la distribuzione nello spazio delle prime due componenti dei dati 
    
    :param X: Dataframe dei dati
    :param title: titolo del grafico
    :param x_label: etichetta asse x
    :param y_label: etichetta asse y
    """

    plt.figure(figsize=(8,6))
    plt.scatter(X[:,0], X[:,1], alpha=0.5, s=5)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.show()

def plot_k_distance(X, k):
    """
    Disegna un plot per visualizzare la distanza di ogni punto rispetto al suo k-esimo punto più vicino
    
    :param X: Dataframe dei dati
    :param k: Numero da considerare come k-esimo vicino più vicino
    """
    nbrs = NearestNeighbors(n_neighbors=k).fit(X)
    distances, _ = nbrs.kneighbors(X)
    k_dist = np.sort(distances[:, k-1])  # ordina le distanze e prende quella all'indice (k-1)
    plt.figure(figsize=(8,4))
    plt.plot(k_dist)
    plt.ylabel(f"{k}-distance")
    plt.xlabel("points sorted by distance")
    plt.title(f"k-distance plot (k={k})")
    plt.grid(alpha=0.3)
    plt.show()
    return k_dist

def apply_hdbscan(X,min_pts):
    """
    Applica l'algoritmo hdbscan
    
    :param X: Dataframe dei dati
    :param min_pts: Numero minimo di punti che un cluster deve contenere
    """

    clusterer = hdbscan.HDBSCAN(min_cluster_size=min_pts)
    labels = clusterer.fit_predict(X)
    return labels

def apply_dbscan(X, epsilon, min_pts):
    """
    Applica l'algoritmo dbscan
    
    :param X: Dataframe dei dati
    :param epsilon: Raggio dell'intorno da considerare
    :param min_pts: Numero minimo di punti che un cluster deve contenere
    """

    dbscan = DBSCAN(eps=epsilon, min_samples= min_pts)  
    labels = dbscan.fit_predict(X)
    return labels

def apply_kmeans(X,k):
    """
    Applica l'algoritmo k-means
    
    :param X: Dataframe dei dati
    :param k: Numero di cluster
    """

    kmeans = KMeans(n_clusters=k, random_state= 42, init='k-means++', n_init=10)
    labels = kmeans.fit_predict(X)
    return labels 

def show_statistics(labels):
    """
    Mostra il conteggio degli elementi presenti in ogni cluster
    
    :param labels: Etichette che associano i punti ai cluster
    """

    unique, counts = np.unique(labels, return_counts=True)
    print(f"{'Label':<10} {'Count':<10}")
    print("-" * 22)
    for label, count in zip(unique, counts):
       name = "Noise" if label == -1 else f"Cluster {label}"
       print(f"{name:<10} {count:<10}")

def plot_clusters(X, labels, title, x_label, y_label):
    """
    Disegna un plot della distribuzione dei dati per visualizzare i cluster trovati
    
    :param X: Dataframe dei dati
    :param labels: Etichette che associano i punti ai cluster
    :param title: Titolo del grafico
    :param x_label: Etichetta dell'asse x
    :param y_label: Etichetta dell'asse y
    """

    plt.figure(figsize=(8,6))
    scatter = plt.scatter(X[:, 0], X[:, 1], c=labels, cmap='tab10', s=5)

    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    unique_labels = np.unique(labels)

    handles = []
    for label in unique_labels:
        color = scatter.cmap(scatter.norm(label))
        label_name = "Noise" if label == -1 else f"Cluster {label}"

        handles.append(
            plt.Line2D([], [], marker='o', color=color, linestyle='', markersize=6, label=label_name)
        )

    plt.legend(handles=handles, title="Clusters", loc="best")
    plt.tight_layout()
    plt.show()
