"""
PFA et S-SELECT : selection de caracteristiques pour la steganalyse universelle.

Reference : F. K. Gomis, M. S. Camara, I. Diop, "Feature Reduction Algorithm for
Universal Steganalysis", EMENA-ISTL, 2019 ; et Lu et al., ACM Multimedia, 2007.

Idee : garder un petit nombre de caracteristiques d'origine, choisies sans etiquettes,
qui separent le plus proprement les images en deux groupes (cover contre stego).

Usage :
    from src.pfa import s_select
    idx, sil, histo = s_select(X, m=10, p=30)   # X : une seule source, cover + stego
    X_reduit = X[:, idx]                         # a donner ensuite au classifieur
"""

import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


def pfa(X, n_features, var_gardee=0.95, seed=42):
    """Choisit n_features caracteristiques representatives (Principal Feature Analysis).

    On regroupe les caracteristiques qui se ressemblent, puis on garde un representant
    par groupe. Cela enleve les redondances et laisse un ensemble varie et informatif.

    X          : matrice (images, caracteristiques), de preference deja standardisee
    n_features : nombre de caracteristiques a garder, soit le nombre de groupes
    var_gardee : part de variance conservee, fixe la dimension du sous-espace PCA
    Retour     : indices des caracteristiques choisies
    """
    # Chaque caracteristique est decrite par ses poids sur les axes principaux
    pca = PCA(n_components=var_gardee, svd_solver="full", random_state=seed).fit(X)
    A = pca.components_.T                       # forme (caracteristiques, axes)

    # On regroupe les caracteristiques en n_features familles
    km = KMeans(n_clusters=n_features, n_init=10, random_state=seed).fit(A)

    # Dans chaque famille, on garde la caracteristique la plus proche du centre
    choisies = []
    for g in range(n_features):
        membres = np.where(km.labels_ == g)[0]
        d = np.linalg.norm(A[membres] - km.cluster_centers_[g], axis=1)
        choisies.append(membres[np.argmin(d)])
    return np.array(sorted(choisies))


def s_select(X, m, p, var_gardee=0.95, seed=42):
    """Cherche entre m et p caracteristiques celles qui separent le mieux en deux groupes.

    Pour chaque taille n, on demande n caracteristiques a PFA, on lance un k-means a
    deux groupes, et on mesure la nettete de la separation par le score de silhouette.
    On garde la taille qui donne la meilleure silhouette. Aucune etiquette n'est utilisee.

    X        : matrice (images, caracteristiques), une seule source, cover puis stego
    m, p     : nombre minimum et maximum de caracteristiques a essayer
    Retour   : (meilleurs_indices, meilleure_silhouette, historique des scores)
    """
    # PFA et k-means demandent des caracteristiques a la meme echelle
    Xs = StandardScaler().fit_transform(X)
    meilleur_idx, meilleure_sil, historique = None, -1.0, []

    for n in range(m, p + 1):
        idx = pfa(Xs, n, var_gardee, seed)
        labels = KMeans(n_clusters=2, n_init=10, random_state=seed).fit_predict(Xs[:, idx])
        sil = silhouette_score(Xs[:, idx], labels)
        historique.append((n, sil))
        if sil > meilleure_sil:
            meilleure_sil, meilleur_idx = sil, idx

    return meilleur_idx, meilleure_sil, historique
