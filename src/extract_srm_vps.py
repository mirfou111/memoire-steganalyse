"""
Extraction SRM parallele, pensee pour tourner sur un VPS sans interface.

Elle lit le corpus dans un dossier local, extrait les caracteristiques sur tous les coeurs,
et met chaque ensemble en cache. Une coupure ne fait perdre qu'un bloc, le calcul reprend.

Usage sur le VPS :
    python src/extract_srm_vps.py
Regler la configuration ci-dessous avant de lancer.
"""

import os, glob, time
import numpy as np
from concurrent.futures import ProcessPoolExecutor
import imageio.v2 as imageio
import sealwatch as sw

# ===================== CONFIGURATION =====================
ROOT      = './corpus'          # dossier ou se trouve le corpus decompresse
OUT       = './features_srm'    # dossier de sortie des caracteristiques
FEATURE   = 'srm'               # 'srm' complet ou 'srmq1' plus leger
SOURCES   = ['natural', 'sd', 'sdxl', 'adm']
ALGOS     = ['lsb', 'uniward', 'hill']
PAYLOADS  = [0.4]               # ajouter 0.2 pour la courbe de sensibilite
INCLURE_COVER = True
N_WORKERS = os.cpu_count()
SEED      = 42
# ========================================================

os.makedirs(OUT, exist_ok=True)
EXTRACTEUR = sw.srmq1 if FEATURE == 'srmq1' else sw.srm


def load_gray(p):
    x = np.asarray(imageio.imread(p))
    return x[..., 0] if x.ndim == 3 else x


def to_vec(f):
    if isinstance(f, dict):
        return np.asarray(sw.tools.flatten(f), dtype=np.float32).ravel()
    return np.asarray(f, dtype=np.float32).ravel()


def extract(p):
    return to_vec(EXTRACTEUR.extract(load_gray(p)))


def extract_set(paths, cache, bloc=200):
    if os.path.exists(cache):
        return
    tmp = cache + '.part.npy'
    feats = list(np.load(tmp)) if os.path.exists(tmp) else []
    with ProcessPoolExecutor(max_workers=N_WORKERS) as ex:
        i = len(feats)
        while i < len(paths):
            lot = paths[i:i + bloc]
            feats.extend(ex.map(extract, lot, chunksize=4))
            i += len(lot)
            np.save(tmp, np.array(feats, dtype=np.float32))   # point de reprise
            print(f'   {i}/{len(paths)}', flush=True)
    np.save(cache, np.array(feats, dtype=np.float32))
    if os.path.exists(tmp):
        os.remove(tmp)


def paths_of(src, setname):
    if setname == 'cover':
        return sorted(glob.glob(f'{ROOT}/{src}/cover/*.pgm'))
    a, p = setname.split('_p')
    return sorted(glob.glob(f'{ROOT}/{src}/{a}/*_p{p}.pgm'))


if __name__ == '__main__':
    sets = (['cover'] if INCLURE_COVER else []) + [f'{a}_p{p}' for a in ALGOS for p in PAYLOADS]
    print('Coeurs :', N_WORKERS, '| caracteristiques :', FEATURE, '| ensembles :', sets, flush=True)
    for src in SOURCES:
        for s in sets:
            paths = paths_of(src, s)
            if not paths:
                print(f'{src} {s}: aucune image, ignore', flush=True); continue
            cache = f'{OUT}/{src}__{s}.npy'
            if os.path.exists(cache):
                print(f'{src} {s}: deja en cache', flush=True); continue
            t = time.time()
            print(f'{src} {s}: {len(paths)} images', flush=True)
            extract_set(paths, cache)
            print(f'   termine en {(time.time() - t) / 60:.1f} min', flush=True)
    print('EXTRACTION TERMINEE', flush=True)
