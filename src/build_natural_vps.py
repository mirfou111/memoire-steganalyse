"""
Construit la source naturelle a grande echelle sur le VPS.

Telecharge BOSSbase, pretraite N images en niveaux de gris 256x256 sans perte,
puis insere les trois algorithmes a 0.4 bpp, en parallele. Ecrit dans ./corpus/natural.

Sert a renforcer la detection des algorithmes adaptatifs, qui a besoin de beaucoup d'images.
Regler N ci-dessous, puis : python src/build_natural_vps.py
"""

import os, glob, urllib.request, zipfile
import numpy as np
from concurrent.futures import ProcessPoolExecutor
from PIL import Image
import imageio.v2 as imageio
import conseal as cl

# ===================== CONFIGURATION =====================
N        = 5000                 # nombre d'images naturelles (max 10000 avec BOSSbase)
IMG      = 256
PAYLOAD  = 0.4
ALGOS    = ['lsb', 'uniward', 'hill']
SEED     = 42
ROOT     = './corpus/natural'
RAW      = './raw_boss'
# ========================================================


def telecharger_bossbase():
    os.makedirs(RAW, exist_ok=True)
    if glob.glob(f'{RAW}/**/*.pgm', recursive=True):
        return
    url = 'http://dde.binghamton.edu/download/ImageDB/BOSSbase_1.01.zip'
    print('Telechargement de BOSSBase...', flush=True)
    urllib.request.urlretrieve(url, 'boss.zip')
    with zipfile.ZipFile('boss.zip') as z:
        z.extractall(RAW)
    print('Extraction terminee.', flush=True)


def pretraiter(n):
    os.makedirs(f'{ROOT}/cover', exist_ok=True)
    fichiers = sorted(glob.glob(f'{RAW}/**/*.pgm', recursive=True))
    covers = []
    for p in fichiers:
        if len(covers) >= n:
            break
        try:
            im = Image.open(p).convert('L'); w, h = im.size
            if min(w, h) < IMG:
                continue
            l, t = (w - IMG) // 2, (h - IMG) // 2
            im = im.crop((l, t, l + IMG, t + IMG))
            out = f'{ROOT}/cover/{len(covers):05d}.pgm'
            im.save(out); covers.append(out)
        except Exception:
            pass
    return covers


def inserer(args):
    p, algo = args
    x = imageio.imread(p).astype(np.uint8)
    s = int(np.random.default_rng(SEED + hash(p) % 10000).integers(1e6))
    if algo == 'lsb':
        y = cl.lsb.simulate(x0=x, alpha=PAYLOAD, seed=s)
    elif algo == 'uniward':
        y = cl.suniward.simulate_single_channel(x0=x, alpha=PAYLOAD, seed=s)
    else:
        y = cl.hill.simulate_single_channel(x0=x, alpha=PAYLOAD, seed=s)
    base = os.path.basename(p).replace('.pgm', '')
    imageio.imwrite(f'{ROOT}/{algo}/{base}_p{PAYLOAD}.pgm', y.astype(np.uint8))


if __name__ == '__main__':
    telecharger_bossbase()
    covers = pretraiter(N)
    print(len(covers), 'covers pretraites', flush=True)
    for algo in ALGOS:
        os.makedirs(f'{ROOT}/{algo}', exist_ok=True)
        with ProcessPoolExecutor() as ex:
            list(ex.map(inserer, [(p, algo) for p in covers], chunksize=8))
        print('insertion terminee :', algo, flush=True)
    print('SOURCE NATURELLE PRETE', flush=True)
