"""
Expérience D (stéganalyse multi-classe, attribution d'algorithme) en script.

Sur la source naturelle, classe cover, LSB, S-UNIWARD, HILL. Écrit le rapport de
classification et la matrice de confusion, teste le critère non supervisé à k
égal au nombre de classes, et la sélection supervisée par PFA. Enregistre la
matrice de confusion en figure.

Usage : python src/run_experiment_D_vps.py
"""

import os, gc, warnings
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_predict, StratifiedKFold, cross_val_score
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix, classification_report
from sklearn.metrics import silhouette_score, adjusted_rand_score
from sklearn.exceptions import ConvergenceWarning
warnings.filterwarnings('ignore', category=ConvergenceWarning)

# ===================== CONFIGURATION =====================
FEAT_DIR = './features_srm'
OUT      = './resultats_D'
SOURCE   = 'natural'
CLASSES  = ['cover', 'lsb', 'uniward', 'hill']
PAYLOAD  = 0.4
N_PCA    = 300
SEED     = 42
M_SEL    = 600           # sous-echantillon par classe pour le volet selection
# ========================================================

os.makedirs(OUT, exist_ok=True)
pp = str(PAYLOAD).replace('.', '')
RESU = f'{OUT}/resultats_D.txt'


def journal(ligne):
    print(ligne, flush=True)
    with open(RESU, 'a') as f:
        f.write(ligne + '\n')


def charger(setname):
    return np.load(f'{FEAT_DIR}/{SOURCE}__{setname}.npy').astype(np.float32)


def classifieur():
    return make_pipeline(StandardScaler(copy=False),
                         PCA(n_components=N_PCA, svd_solver='randomized', random_state=SEED),
                         LogisticRegression(max_iter=2000))


def pfa_indices(Xmat, n_feats, q=200, seed=SEED):
    Z = StandardScaler(copy=False).fit_transform(Xmat.copy())
    comp = PCA(n_components=min(q, Xmat.shape[0], Xmat.shape[1]), svd_solver='randomized', random_state=seed).fit(Z)
    A = comp.components_.T
    km = KMeans(n_clusters=n_feats, random_state=seed, n_init=10).fit(A)
    idx = []
    for c in range(n_feats):
        membres = np.where(km.labels_ == c)[0]
        d = np.linalg.norm(A[membres] - km.cluster_centers_[c], axis=1)
        idx.append(membres[np.argmin(d)])
    return np.array(sorted(idx))


if __name__ == '__main__':
    journal(f'# Experience D, multi-classe, {SOURCE}, {PAYLOAD} bpp, PCA {N_PCA}')
    blocs = {'cover': charger('cover')}
    for a in ['lsb', 'uniward', 'hill']:
        blocs[a] = charger(f'{a}_p{PAYLOAD}')
    n = min(len(blocs[c]) for c in CLASSES)
    X = np.vstack([blocs[c][:n] for c in CLASSES]).astype(np.float32)
    y = np.concatenate([[i] * n for i in range(len(CLASSES))])
    del blocs; gc.collect()
    journal(f'{n} images par classe, {len(y)} au total, {X.shape[1]} dimensions')

    # classification multi-classe et matrice de confusion
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED)
    y_pred = cross_val_predict(classifieur(), X, y, cv=cv)
    journal(f'exactitude globale : {accuracy_score(y, y_pred):.3f}')
    journal(f'F1 macro           : {f1_score(y, y_pred, average="macro"):.3f}')
    journal(classification_report(y, y_pred, target_names=CLASSES, digits=3))
    C = confusion_matrix(y, y_pred, normalize='true')

    fig, ax = plt.subplots(figsize=(6.5, 5.5))
    im = ax.imshow(C, cmap='Blues', vmin=0, vmax=1)
    ax.set_xticks(range(len(CLASSES))); ax.set_xticklabels(CLASSES)
    ax.set_yticks(range(len(CLASSES))); ax.set_yticklabels(CLASSES)
    ax.set_xlabel('classe predite'); ax.set_ylabel('vraie classe')
    for i in range(len(CLASSES)):
        for j in range(len(CLASSES)):
            ax.text(j, i, f'{C[i, j]:.2f}', ha='center', va='center',
                    color='white' if C[i, j] > 0.5 else 'black')
    ax.set_title(f'Matrice de confusion, {SOURCE}, {PAYLOAD} bpp, SRM')
    fig.colorbar(im, fraction=0.046, pad=0.04)
    plt.tight_layout(); plt.savefig(f'{OUT}/expD_srm_confusion_{SOURCE}_p{pp}.png', dpi=150); plt.close()
    journal(f'figure enregistree : expD_srm_confusion_{SOURCE}_p{pp}.png')

    # volet selection sur sous-echantillon
    sel = np.concatenate([np.where(y == i)[0][:M_SEL] for i in range(len(CLASSES))])
    Xs, ys = X[sel], y[sel]
    k = len(CLASSES)
    Zs = PCA(n_components=N_PCA, svd_solver='randomized', random_state=SEED).fit_transform(
        StandardScaler(copy=False).fit_transform(Xs.copy()))
    labels_ns = KMeans(n_clusters=k, random_state=SEED, n_init=10).fit_predict(Zs)
    journal(f'\ncritere non supervise, k = {k} : silhouette {silhouette_score(Zs, labels_ns):.3f}, '
            f'ARI avec vraies classes {adjusted_rand_score(ys, labels_ns):.3f}')

    ref = cross_val_score(classifieur(), Xs, ys, cv=3, scoring='accuracy').mean()
    journal(f'reference toutes caracteristiques (PCA {N_PCA}) : {ref:.3f}')
    for nf in [24, 50, 100]:
        idx = pfa_indices(Xs, nf)
        pipe = make_pipeline(StandardScaler(copy=False), LogisticRegression(max_iter=2000))
        acc = cross_val_score(pipe, Xs[:, idx], ys, cv=3, scoring='accuracy').mean()
        journal(f'PFA + supervise, {nf:3d} caracteristiques : {acc:.3f}')
    journal('\nEXPERIENCE D TERMINEE')
