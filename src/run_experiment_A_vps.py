"""
Expérience A (décalage de domaine) en script, pour tourner sans notebook.

Lit les caractéristiques SRM déjà extraites, calcule pour chaque algorithme la
référence sur le naturel, la chute en cross-domaine, l'AUC appariée et le taux
de faux positifs par source, écrit les résultats au fil de l'eau dans un fichier
texte et enregistre les figures. Conçu pour tmux : une coupure ne fait rien
perdre des algorithmes déjà terminés.

Mémoire maîtrisée : simple précision, PCA randomisée, un modèle à la fois,
libération explicite entre les algorithmes. Tient dans 16 Go.

Usage :
    python src/run_experiment_A_vps.py
Régler la configuration ci-dessous. Pour n'obtenir que la réponse adaptative,
mettre ALGOS = ['uniward', 'hill'].
"""

import os, gc, warnings
import numpy as np
import matplotlib
matplotlib.use('Agg')                      # pas d'affichage, on enregistre les figures
import matplotlib.pyplot as plt
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score, RepeatedStratifiedKFold, train_test_split
from sklearn.metrics import roc_auc_score, roc_curve
from sklearn.exceptions import ConvergenceWarning
warnings.filterwarnings('ignore', category=ConvergenceWarning)

# ===================== CONFIGURATION =====================
FEAT_DIR  = './features_srm'
OUT       = './resultats_A'
NATUREL   = 'natural'
GENERES   = ['sd', 'midjourney', 'adm']
ALGOS     = ['lsb', 'uniward', 'hill']     # pour l'adaptatif seul : ['uniward', 'hill']
PAYLOAD   = 0.4
N_PCA     = 300
N_SPLITS  = 5
N_REPEATS = 1                              # 1 suffit a 10000 images ; 3 pour l'ecart type
SEED      = 42
# ========================================================

os.makedirs(OUT, exist_ok=True)
pp = str(PAYLOAD).replace('.', '')
RESU = f'{OUT}/resultats_A.txt'
palette = {'natural':'tab:blue', 'sd':'tab:orange', 'midjourney':'tab:green', 'adm':'tab:red'}


def journal(ligne):
    print(ligne, flush=True)
    with open(RESU, 'a') as f:
        f.write(ligne + '\n')


def charger(source, setname):
    return np.load(f'{FEAT_DIR}/{source}__{setname}.npy').astype(np.float32)


def detecteur():
    return make_pipeline(StandardScaler(copy=False),
                         PCA(n_components=N_PCA, svd_solver='randomized', random_state=SEED),
                         LogisticRegression(max_iter=2000))


def jeu(source, algo):
    Xc = charger(source, 'cover')
    Xs = charger(source, f'{algo}_p{PAYLOAD}')
    n = min(len(Xc), len(Xs)); Xc, Xs = Xc[:n], Xs[:n]
    X = np.vstack([Xc, Xs]); y = np.concatenate([np.zeros(n), np.ones(n)])
    return X, y, Xc


def auc_croisee(X, y):
    cv = RepeatedStratifiedKFold(n_splits=N_SPLITS, n_repeats=N_REPEATS, random_state=SEED)
    s = cross_val_score(detecteur(), X, y, cv=cv, scoring='roc_auc')
    return s.mean(), s.std()


if __name__ == '__main__':
    journal(f'# Experience A, SRM, {PAYLOAD} bpp, PCA {N_PCA}, cv {N_SPLITS}x{N_REPEATS}')
    for algo in ALGOS:
        try:
            Xn, yn, cover_nat = jeu(NATUREL, algo)
            auc_ref_m, auc_ref_s = auc_croisee(Xn, yn)
            det_nat = detecteur().fit(Xn, yn)
            seuil = np.quantile(det_nat.predict_proba(cover_nat)[:, 1], 0.95)

            journal(f'\n=== {algo} {PAYLOAD} bpp ===')
            journal(f'reference naturel AUC {auc_ref_m:.3f} +/- {auc_ref_s:.3f}')

            lignes = []
            for g in GENERES:
                Xg, yg, cover_g = jeu(g, algo)
                auc_cross = roc_auc_score(yg, det_nat.predict_proba(Xg)[:, 1])
                am, asd = auc_croisee(Xg, yg)
                fpr_g = float(np.mean(det_nat.predict_proba(cover_g)[:, 1] > seuil))
                lignes.append((g, auc_cross, am, fpr_g))
                journal(f'  {g:11s} cross {auc_cross:.3f}  apparie {am:.3f}  FPR {fpr_g:.3f}')
                del Xg, yg, cover_g; gc.collect()

            # Figure 1 : courbes ROC
            fig, ax = plt.subplots(figsize=(7, 6))
            Xtr, Xte, ytr, yte = train_test_split(Xn, yn, test_size=0.3, random_state=SEED, stratify=yn)
            det_ref = detecteur().fit(Xtr, ytr)
            f, t, _ = roc_curve(yte, det_ref.predict_proba(Xte)[:, 1])
            ax.plot(f, t, lw=2, label=f'reference (AUC={roc_auc_score(yte, det_ref.predict_proba(Xte)[:,1]):.2f})')
            for g in GENERES:
                Xg, yg, _ = jeu(g, algo)
                sc = det_nat.predict_proba(Xg)[:, 1]
                f, t, _ = roc_curve(yg, sc)
                ax.plot(f, t, label=f'cross vers {g} (AUC={roc_auc_score(yg, sc):.2f})')
                del Xg, yg; gc.collect()
            ax.plot([0, 1], [0, 1], 'k--', alpha=0.4)
            ax.set_xlabel('faux positifs'); ax.set_ylabel('vrais positifs')
            ax.set_title(f'ROC, {algo} {PAYLOAD} bpp, SRM'); ax.legend()
            plt.tight_layout(); plt.savefig(f'{OUT}/expA_srm_roc_{algo}_p{pp}.png', dpi=150); plt.close()

            # Figure 2 : barres d'AUC
            fig, ax = plt.subplots(figsize=(8, 5))
            labels = ['ref'] + [f'{g}\ncross' for g in GENERES] + [f'{g}\napparie' for g in GENERES]
            vals = [auc_ref_m] + [l[1] for l in lignes] + [l[2] for l in lignes]
            couleurs = ['#2a9d8f'] + ['#e76f51'] * len(GENERES) + ['#264653'] * len(GENERES)
            ax.bar(labels, vals, color=couleurs); ax.axhline(0.5, ls='--', color='gray')
            ax.set_ylim(0.4, 1.0); ax.set_title(f'AUC par condition, {algo} {PAYLOAD} bpp, SRM')
            plt.tight_layout(); plt.savefig(f'{OUT}/expA_srm_aucbars_{algo}_p{pp}.png', dpi=150); plt.close()

            # Figure 3 : distribution cumulee des scores sur images vierges
            fig, ax = plt.subplots(figsize=(9, 5))
            for s in [NATUREL] + GENERES:
                cov = charger(s, 'cover')
                sc = det_nat.predict_proba(cov)[:, 1]; xs = np.sort(sc)
                ax.plot(xs, np.arange(1, len(xs) + 1) / len(xs), color=palette.get(s, 'gray'), lw=2, label=f'{s} vierge')
                del cov, sc; gc.collect()
            ax.axvline(seuil, ls='--', color='gray', label='seuil 5% FPR naturel')
            ax.set_xlabel('score du detecteur'); ax.set_ylabel('proportion cumulee')
            ax.set_title(f'Scores sur images vierges, {algo} {PAYLOAD} bpp, SRM'); ax.legend()
            plt.tight_layout(); plt.savefig(f'{OUT}/expA_srm_fprcdf_{algo}_p{pp}.png', dpi=150); plt.close()

            journal(f'  figures enregistrees pour {algo}')
            del Xn, yn, cover_nat, det_nat; gc.collect()
        except Exception as e:
            journal(f'  ECHEC sur {algo} : {e}')
    journal('\nEXPERIENCE A TERMINEE')
