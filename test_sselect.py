import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score, RepeatedStratifiedKFold

FEAT = './features_srm'; load = lambda s, n: np.load(f'{FEAT}/{s}__{n}.npy')
Xc = load('natural', 'cover'); Xs = load('natural', 'uniward_p0.4')
n = min(len(Xc), len(Xs)); X = np.vstack([Xc[:n], Xs[:n]]); y = np.r_[np.zeros(n), np.ones(n)]
Xn = StandardScaler().fit_transform(X)
A = PCA(n_components=50, svd_solver='randomized', random_state=42).fit(Xn).components_.T
K = 100
km = KMeans(n_clusters=K, n_init=5, random_state=42).fit(A)
idx = sorted({np.where(km.labels_ == g)[0][np.argmin(np.linalg.norm(A[km.labels_ == g] - km.cluster_centers_[g], axis=1))] for g in range(K)})
cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=2, random_state=42)
auc = cross_val_score(make_pipeline(StandardScaler(), LogisticRegression(max_iter=5000)), X[:, idx], y, cv=cv, scoring='roc_auc').mean()
print(f'uniward PFA {len(idx)} caracteristiques -> AUC {auc:.3f}') 
