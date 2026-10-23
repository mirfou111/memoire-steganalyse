"""
Expérience B (interférence des artefacts) en script.

Mesure, sans détecteur entraîné, la distance de Mahalanobis cover vers stégo par
source et par algorithme, après réduction PCA commune. Une distance plus faible
que le naturel signale un masquage de l'insertion. Écrit les résultats au fil de
l'eau et une figure en barres par algorithme. Pas de projection 2D, écartée.

Usage : python src/run_experiment_B_vps.py
"""

import os, gc
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.covariance import LedoitWolf
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# ===================== CONFIGURATION =====================
FEAT_DIR = './features_srm'
OUT      = './resultats_B'
SOURCES  = ['natural', 'sd', 'midjourney', 'adm']
ALGOS    = ['lsb', 'uniward', 'hill']
PAYLOAD  = 0.4
K_PCA    = 200
SEED     = 42
# ========================================================

os.makedirs(OUT, exist_ok=True)
pp = str(PAYLOAD).replace('.', '')
RESU = f'{OUT}/resultats_B.txt'
palette = {'natural':'tab:blue', 'sd':'tab:orange', 'midjourney':'tab:green', 'adm':'tab:red'}


def journal(ligne):
    print(ligne, flush=True)
    with open(RESU, 'a') as f:
        f.write(ligne + '\n')


def charger(source, setname):
    return np.load(f'{FEAT_DIR}/{source}__{setname}.npy').astype(np.float32)


def distance(source, algo):
    Xc = charger(source, 'cover')
    Xs = charger(source, f'{algo}_p{PAYLOAD}')
    n = min(len(Xc), len(Xs)); Xc, Xs = Xc[:n], Xs[:n]
    Z = PCA(n_components=K_PCA, svd_solver='randomized', random_state=SEED).fit_transform(
        StandardScaler(copy=False).fit_transform(np.vstack([Xc, Xs])))
    Zc, Zs = Z[:n], Z[n:]
    cov = LedoitWolf().fit(Z).covariance_
    diff = Zs.mean(0) - Zc.mean(0)
    d = float(np.sqrt(diff @ np.linalg.pinv(cov) @ diff))
    del Xc, Xs, Z, Zc, Zs, cov; gc.collect()
    return d


if __name__ == '__main__':
    journal(f'# Experience B, SRM, {PAYLOAD} bpp, PCA {K_PCA}')
    D = {}
    entete = f"{'algo':10s} " + ' '.join(f'{s:>10s}' for s in SOURCES)
    journal(entete)
    for a in ALGOS:
        D[a] = {}
        for s in SOURCES:
            try:
                D[a][s] = distance(s, a)
            except Exception as e:
                D[a][s] = float('nan'); journal(f'  ECHEC {a} {s} : {e}')
        journal(f'{a:10s} ' + ' '.join(f'{D[a][s]:10.3f}' for s in SOURCES))

    for a in ALGOS:
        fig, ax = plt.subplots(figsize=(7, 5))
        vals = [D[a][s] for s in SOURCES]
        ax.bar(SOURCES, vals, color=[palette[s] for s in SOURCES])
        if not np.isnan(D[a]['natural']):
            ax.axhline(D[a]['natural'], ls='--', color='gray', label='niveau naturel')
        ax.set_ylabel('distance cover vers stego'); ax.legend()
        ax.set_title(f'Interference, {a} {PAYLOAD} bpp, SRM')
        plt.tight_layout(); plt.savefig(f'{OUT}/expB_srm_maha_{a}_p{pp}.png', dpi=150); plt.close()
        journal(f'figure enregistree : expB_srm_maha_{a}_p{pp}.png')
    journal('\nEXPERIENCE B TERMINEE')
