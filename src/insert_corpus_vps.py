"""
Insertion stéganographique sur le corpus 10k, pour le VPS.

Prend les covers deja telecharges et recadres dans corpus_10k/cover_<source>/,
et produit les versions stego dans la structure attendue par l'extracteur SRM :

    corpus/<source>/cover/NNNNN.pgm        (lien vers les covers d'origine)
    corpus/<source>/<algo>/NNNNN_p0.4.pgm  (stego generes)

Trois algorithmes, une charge. Parallele sur tous les coeurs, reprenable :
un stego deja present n'est pas recalcule. Lancer en tmux :
    python src/insert_corpus_vps.py
"""

import os, glob
import numpy as np
from concurrent.futures import ProcessPoolExecutor
import imageio.v2 as imageio
import conseal as cl

# ===================== CONFIGURATION =====================
COVERS_ROOT = './corpus_10k'                       # dossiers cover_<source>
OUT_ROOT    = './corpus'                           # structure de sortie
SOURCES     = ['natural', 'sd', 'adm', 'midjourney']
ALGOS       = ['lsb', 'uniward', 'hill']
PAYLOAD     = 0.4
SEED        = 42
N_WORKERS   = os.cpu_count()
# ========================================================


def charger_gris(p):
    x = np.asarray(imageio.imread(p))
    if x.ndim == 3:
        x = x[..., 0]
    return x.astype(np.uint8)


def graine_de(base):
    # graine deterministe tiree du numero de fichier, pour la reproductibilite
    chiffres = ''.join(c for c in base if c.isdigit())
    return SEED + (int(chiffres) if chiffres else 0)


def inserer(args):
    p, algo, out_dir = args
    base = os.path.basename(p).replace('.pgm', '')
    cible = f'{out_dir}/{base}_p{PAYLOAD}.pgm'
    if os.path.exists(cible):        # reprise : deja fait
        return
    try:
        x = charger_gris(p)
        s = graine_de(base)
        if algo == 'lsb':
            # cette version de conseal attend l'image en premier argument positionnel
            y = cl.lsb.simulate(x, PAYLOAD, seed=s)
        elif algo == 'uniward':
            y = cl.suniward.simulate_single_channel(x0=x, alpha=PAYLOAD, seed=s)
        else:
            y = cl.hill.simulate_single_channel(x0=x, alpha=PAYLOAD, seed=s)
        imageio.imwrite(cible, np.asarray(y).astype(np.uint8))
    except Exception as e:
        print('echec', p, algo, e, flush=True)


def lien_covers(src):
    # rend les covers visibles a l'extracteur sans les copier
    dst = f'{OUT_ROOT}/{src}/cover'
    srcdir = os.path.abspath(f'{COVERS_ROOT}/cover_{src}')
    os.makedirs(f'{OUT_ROOT}/{src}', exist_ok=True)
    if not os.path.exists(dst):
        os.symlink(srcdir, dst)


def autotest():
    # verifie en quelques secondes que les appels conseal fonctionnent, avant les heures de calcul
    echantillon = None
    for src in SOURCES:
        g = sorted(glob.glob(f'{COVERS_ROOT}/cover_{src}/*.pgm'))
        if g:
            echantillon = g[0]; break
    if echantillon is None:
        raise SystemExit('Aucun cover trouve dans ' + COVERS_ROOT)
    x = charger_gris(echantillon)
    cl.lsb.simulate(x, PAYLOAD, seed=1)
    cl.suniward.simulate_single_channel(x0=x, alpha=PAYLOAD, seed=1)
    cl.hill.simulate_single_channel(x0=x, alpha=PAYLOAD, seed=1)
    print('Autotest conseal OK sur', echantillon, flush=True)


if __name__ == '__main__':
    autotest()
    print('Coeurs :', N_WORKERS, '| sources :', SOURCES, '| charge :', PAYLOAD, flush=True)
    for src in SOURCES:
        covers = sorted(glob.glob(f'{COVERS_ROOT}/cover_{src}/*.pgm'))
        if not covers:
            print(f'{src}: aucun cover, ignore', flush=True); continue
        lien_covers(src)
        for algo in ALGOS:
            out_dir = f'{OUT_ROOT}/{src}/{algo}'
            os.makedirs(out_dir, exist_ok=True)
            taches = [(p, algo, out_dir) for p in covers]
            with ProcessPoolExecutor(max_workers=N_WORKERS) as ex:
                list(ex.map(inserer, taches, chunksize=16))
            faits = len(glob.glob(f'{out_dir}/*_p{PAYLOAD}.pgm'))
            print(f'{src} {algo}: {faits} stego', flush=True)
    print('INSERTION TERMINEE', flush=True)
