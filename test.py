import numpy as np
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score, RepeatedStratifiedKFold, train_test_split
import sealwatch as sw

FEAT = './features_srm'
load = lambda s, n: np.load(f'{FEAT}/{s}__{n}.npy')
Xc = load('natural', 'cover'); Xs = load('natural', 'uniward_p0.4')
n = min(len(Xc), len(Xs)); Xc, Xs = Xc[:n], Xs[:n]
X = np.vstack([Xc, Xs]); y = np.r_[np.zeros(n), np.ones(n)]

for k in [100, 300, 800]:
    cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=2, random_state=42)
    pipe = make_pipeline(StandardScaler(), PCA(n_components=k, random_state=42),
                         LogisticRegression(max_iter=5000))
    s = cross_val_score(pipe, X, y, cv=cv, scoring='roc_auc')
    print(f'uniward PCA{k:4d} + logit -> AUC {s.mean():.3f}')

try:
    Xc_tr, Xc_te = train_test_split(Xc, test_size=0.3, random_state=42)
    Xs_tr, Xs_te = train_test_split(Xs, test_size=0.3, random_state=42)
    tr = sw.ensemble_classifier.FldEnsembleTrainer(
        Xc=np.ascontiguousarray(Xc_tr), Xs=np.ascontiguousarray(Xs_tr), seed=42, verbose=0)
    model, _ = tr.train()
    Xte = np.vstack([Xc_te, Xs_te]); yte = np.r_[-np.ones(len(Xc_te)), np.ones(len(Xs_te))]
    print('uniward ensemble FLD -> exactitude', round(model.score(Xte, yte), 3))
except Exception as e:
    print('ensemble indisponible :', str(e)[:200])
