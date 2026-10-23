"""
Expérience C (adaptation du détecteur, H3) en script.

Sur une partition de test commune, compare quatre stratégies sur les sources
générées : détecteur naturel seul, réentraînement mixte, détection consciente
de la source, et détecteur apparié comme borne haute. Ajoute un volet de
généralisation à un générateur non vu. Écrit résultats et figures.

Cas LSB par défaut, là où le décalage de domaine est lisible.
Usage : python src/run_experiment_C_vps.py
"""

import os, gc, warnings
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
from sklearn.exceptions import ConvergenceWarning
warnings.filterwarnings('ignore', category=ConvergenceWarning)

# ===================== CONFIGURATION =====================
FEAT_DIR  = './features_srm'
OUT       = './resultats_C'
NATUREL   = 'natural'
GENERES   = ['sd', 'midjourney', 'adm']
ALGOS     = ['lsb', 'uniward', 'hill']
PAYLOAD   = 0.4
N_PCA     = 300
TEST_SIZE = 0.3
MAX_PAR_SOURCE = 5000    # sous-echantillon par source, pour tenir dans 32 Go
SEED      = 42
# ========================================================

os.makedirs(OUT, exist_ok=True)
pp = str(PAYLOAD).replace('.', '')
RESU = f'{OUT}/resultats_C.txt'
SOURCES = [NATUREL] + GENERES


def journal(ligne):
    print(ligne, flush=True)
    with open(RESU, 'a') as f:
        f.write(ligne + '\n')


def charger(source, setname):
    return np.load(f'{FEAT_DIR}/{source}__{setname}.npy').astype(np.float32)


def detecteur():
    # copy=True (defaut) : indispensable ici, les memes tableaux servent a plusieurs
    # detecteurs ; en mode sur place le scaler corromprait les donnees partagees.
    return make_pipeline(StandardScaler(),
                         PCA(n_components=N_PCA, svd_solver='randomized', random_state=SEED),
                         LogisticRegression(max_iter=2000))


def partition(source, algo):
    Xc = charger(source, 'cover'); Xs = charger(source, f'{algo}_p{PAYLOAD}')
    n = min(len(Xc), len(Xs), MAX_PAR_SOURCE); Xc, Xs = Xc[:n], Xs[:n]
    X = np.vstack([Xc, Xs]); y = np.concatenate([np.zeros(n), np.ones(n)])
    return train_test_split(X, y, test_size=TEST_SIZE, random_state=SEED, stratify=y)


if __name__ == '__main__':
    journal(f'# Experience C, SRM, {PAYLOAD} bpp, PCA {N_PCA}')
    for algo in ALGOS:
        try:
            part = {s: partition(s, algo) for s in SOURCES}
            Xtr = {s: part[s][0] for s in SOURCES}; Xte = {s: part[s][1] for s in SOURCES}
            ytr = {s: part[s][2] for s in SOURCES}; yte = {s: part[s][3] for s in SOURCES}

            det_nat = detecteur().fit(Xtr[NATUREL], ytr[NATUREL])
            auc_nat = {g: roc_auc_score(yte[g], det_nat.predict_proba(Xte[g])[:, 1]) for g in GENERES}

            Xmix = np.vstack([Xtr[s] for s in SOURCES]); ymix = np.concatenate([ytr[s] for s in SOURCES])
            det_mix = detecteur().fit(Xmix, ymix)
            auc_mix = {g: roc_auc_score(yte[g], det_mix.predict_proba(Xte[g])[:, 1]) for g in GENERES}
            del Xmix, ymix; gc.collect()

            det_app = {s: detecteur().fit(Xtr[s], ytr[s]) for s in SOURCES}
            auc_app = {g: roc_auc_score(yte[g], det_app[g].predict_proba(Xte[g])[:, 1]) for g in GENERES}

            Xsrc = np.vstack([Xtr[s] for s in SOURCES])
            ysrc = np.concatenate([[i] * len(Xtr[s]) for i, s in enumerate(SOURCES)])
            clf_src = make_pipeline(StandardScaler(), PCA(n_components=N_PCA, svd_solver='randomized', random_state=SEED),
                                    LogisticRegression(max_iter=2000)).fit(Xsrc, ysrc)
            del Xsrc, ysrc; gc.collect()
            auc_aware, acc_src = {}, {}
            for g in GENERES:
                pred = clf_src.predict(Xte[g])
                acc_src[g] = float(np.mean(pred == SOURCES.index(g)))
                scores = np.empty(len(Xte[g]))
                for si, s in enumerate(SOURCES):
                    m = pred == si
                    if m.any():
                        scores[m] = det_app[s].predict_proba(Xte[g][m])[:, 1]
                auc_aware[g] = roc_auc_score(yte[g], scores)

            journal(f'\n=== {algo} {PAYLOAD} bpp ===')
            journal(f"{'source':11s} {'nat seul':>9s} {'mixte':>7s} {'conscient':>10s} {'apparie':>8s}  id source")
            for g in GENERES:
                journal(f'{g:11s} {auc_nat[g]:9.3f} {auc_mix[g]:7.3f} {auc_aware[g]:10.3f} {auc_app[g]:8.3f}   {acc_src[g]:.3f}')

            # figure strategies
            strategies = [('naturel seul', auc_nat, '#e76f51'), ('mixte', auc_mix, '#f4a261'),
                          ('conscient', auc_aware, '#2a9d8f'), ('apparie', auc_app, '#264653')]
            x = np.arange(len(GENERES)); largeur = 0.2
            fig, ax = plt.subplots(figsize=(9, 5))
            for k, (nom, dic, coul) in enumerate(strategies):
                ax.bar(x + (k - 1.5) * largeur, [dic[g] for g in GENERES], largeur, label=nom, color=coul)
            ax.axhline(0.5, ls='--', color='gray'); ax.set_xticks(x); ax.set_xticklabels(GENERES)
            ax.set_ylim(0.4, 1.0); ax.set_ylabel('AUC de test'); ax.legend()
            ax.set_title(f'Adaptation du detecteur, {algo} {PAYLOAD} bpp, SRM')
            plt.tight_layout(); plt.savefig(f'{OUT}/expC_srm_strategies_{algo}_p{pp}.png', dpi=150); plt.close()

            # volet generateur non vu
            journal(f'--- {algo}, generateur non vu ---')
            ligne = {}
            for held in GENERES:
                vus = [NATUREL] + [g for g in GENERES if g != held]
                Xt = np.vstack([Xtr[s] for s in vus]); yt = np.concatenate([ytr[s] for s in vus])
                det = detecteur().fit(Xt, yt)
                auc_vu = roc_auc_score(yte[held], det.predict_proba(Xte[held])[:, 1])
                ligne[held] = (auc_nat[held], auc_vu)
                journal(f'  {held:11s} naturel seul {auc_nat[held]:.3f}  ->  mixte sans {held} {auc_vu:.3f}')
                del Xt, yt, det; gc.collect()

            fig, ax = plt.subplots(figsize=(8, 5)); x = np.arange(len(GENERES)); largeur = 0.35
            ax.bar(x - largeur/2, [ligne[g][0] for g in GENERES], largeur, label='naturel seul', color='#e76f51')
            ax.bar(x + largeur/2, [ligne[g][1] for g in GENERES], largeur, label='mixte, source non vue', color='#2a9d8f')
            ax.axhline(0.5, ls='--', color='gray'); ax.set_xticks(x); ax.set_xticklabels(GENERES)
            ax.set_ylim(0.4, 1.0); ax.set_ylabel('AUC sur la source non vue'); ax.legend()
            ax.set_title(f'Generalisation a un generateur non vu, {algo} {PAYLOAD} bpp, SRM')
            plt.tight_layout(); plt.savefig(f'{OUT}/expC_srm_loso_{algo}_p{pp}.png', dpi=150); plt.close()
            journal(f'  figures enregistrees pour {algo}')
            del part, Xtr, Xte, ytr, yte, det_nat, det_mix, det_app, clf_src; gc.collect()
        except Exception as e:
            journal(f'  ECHEC sur {algo} : {e}')
    journal('\nEXPERIENCE C TERMINEE')
