"""
Figures de la Partie I du mémoire (chapitre 1).

Usage : python src/figures_partie1.py [chemin_image_niveaux_de_gris]
Sans argument, une image du domaine public fournie avec matplotlib est utilisée.
Pour la version finale, passer une image BOSSbase (.pgm), par exemple :
    python src/figures_partie1.py data/natural/00001.pgm
Les figures sont écrites dans memoire/figures/.
"""
import os, sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from PIL import Image

OUT = os.path.join(os.path.dirname(__file__), '..', 'memoire', 'figures')
os.makedirs(OUT, exist_ok=True)
rng = np.random.default_rng(42)
plt.rcParams.update({'font.size': 11, 'font.family': 'DejaVu Sans'})

def charger(path=None, taille=256, centre=0.5, haut=False):
    """Recadre le plus grand carré possible (centré horizontalement en `centre`,
    en haut de l'image si `haut`), puis le met à la taille voulue en niveaux de gris."""
    if path is None:
        path = os.path.join(matplotlib.get_data_path(), 'sample_data', 'grace_hopper.jpg')
    img = Image.open(path).convert('L')
    w, h = img.size; c = min(w, h)
    x0 = int(min(max(centre * w - c / 2, 0), w - c))
    y0 = 0 if haut else (h - c) // 2
    img = img.crop((x0, y0, x0 + c, y0 + c))
    if taille and c != taille:
        img = img.resize((taille, taille), Image.LANCZOS)
    return np.array(img).astype(np.int32)

# ---------- simulateur d'insertion ternaire (émetteur à charge fixée) ----------
def h3(p):
    p = np.clip(p, 1e-12, 1/3); q = 1-2*p
    return -2*p*np.log2(p) - q*np.log2(np.clip(q, 1e-12, 1))

def simuler(x, rho, charge_bpp):
    m = charge_bpp * x.size
    lo, hi = 1e-6, 1e4
    for _ in range(60):
        lam = np.sqrt(lo*hi)
        p = np.exp(-lam*rho) / (1 + 2*np.exp(-lam*rho))
        if h3(p).sum() > m: lo = lam
        else: hi = lam
    p = np.exp(-lam*rho) / (1 + 2*np.exp(-lam*rho))
    u = rng.random(x.shape)
    y = x.copy()
    y[u < p] += 1
    y[(u >= p) & (u < 2*p)] -= 1
    y[(x == 255) & (y == 256)] = 254; y[(x == 0) & (y == -1)] = 1
    return y

def filtrer(x, k):
    kh, kw = k.shape; ph, pw = kh//2, kw//2
    xp = np.pad(x.astype(float), ((ph, ph), (pw, pw)), mode='symmetric')
    out = np.zeros(x.shape)
    for i in range(kh):
        for j in range(kw):
            out += k[i, j] * xp[i:i+x.shape[0], j:j+x.shape[1]]
    return out

def cout_hill(x):
    kb = np.array([[-1, 2, -1], [2, -4, 2], [-1, 2, -1]], float)
    r = np.abs(filtrer(x, kb))
    xi = 1.0 / (filtrer(r, np.ones((3, 3))/9) + 1e-10)
    return filtrer(xi, np.ones((15, 15))/225)

# ---------- Figure 1.1 : chaîne stéganographique ----------
def fig_chaine():
    fig, ax = plt.subplots(figsize=(11, 3.6)); ax.axis('off'); ax.set_xlim(-0.2, 11.1); ax.set_ylim(0, 3.6)
    def boite(x, y, w, h, txt, c):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.05', fc=c, ec='black'))
        ax.text(x+w/2, y+h/2, txt, ha='center', va='center')
    def fleche(a, b):
        ax.add_patch(FancyArrowPatch(a, b, arrowstyle='-|>', mutation_scale=15, lw=1.3))
    boite(0.1, 2.3, 1.7, 0.8, '« RDV à Gorée »\n(payload)', '#fde9c9')
    boite(0.0, 0.45, 1.9, 0.9, 'Image de\ncouverture\n(cover)', '#dbe9f6')
    boite(2.6, 1.4, 1.6, 0.9, 'Insertion', '#e8e8e8')
    boite(5.0, 1.4, 1.7, 0.9, 'Stégo-objet\n(stego)', '#dbe9f6')
    boite(7.5, 1.4, 1.6, 0.9, 'Extraction', '#e8e8e8')
    boite(9.5, 1.4, 1.5, 0.9, '« RDV à\nGorée »', '#fde9c9')
    boite(4.75, 0.05, 2.2, 0.75, 'Le gardien\n(stéganalyste)', '#f6d5d5')
    ax.text(3.4, 3.0, 'clé secrète', ha='center'); ax.text(8.3, 3.0, 'clé secrète', ha='center')
    ax.text(3.4, 1.15, 'Awa (émettrice)', ha='center', fontsize=9, style='italic'); ax.text(8.3, 1.15, 'Moussa (destinataire)', ha='center', fontsize=9, style='italic')
    fleche((1.85, 2.7), (2.6, 2.0)); fleche((1.95, 0.9), (2.6, 1.7))
    fleche((3.4, 2.85), (3.4, 2.3)); fleche((8.3, 2.85), (8.3, 2.3))
    fleche((4.2, 1.85), (5.0, 1.85)); fleche((6.7, 1.85), (7.5, 1.85)); fleche((9.1, 1.85), (9.6, 1.85))
    ax.text(7.1, 1.45, 'canal\nsurveillé', ha='center', fontsize=8)
    fleche((5.85, 1.4), (5.85, 0.8))
    fig.savefig(f'{OUT}/fig1_1_chaine.png', dpi=200, bbox_inches='tight'); plt.close(fig)

# ---------- Figure : l'image vue comme une matrice ----------
def fig_matrice(x, y0=None, x0=None, n=6, cadre=None):
    if cadre is not None:     # chercher le bloc le plus contrasté dans une zone donnée (y1, y2, x1, x2)
        y1, y2, x1, x2 = cadre; best = -1
        for i in range(y1, y2 - n):
            for j in range(x1, x2 - n):
                v = x[i:i+n, j:j+n].std()
                if v > best: best, y0, x0 = v, i, j
    if y0 is None:   # zone la plus contrastée, pour un exemple parlant
        best, y0, x0 = -1, 0, 0
        for i in range(0, x.shape[0]-n, 4):
            for j in range(0, x.shape[1]-n, 4):
                v = x[i:i+n, j:j+n].std()
                if v > best: best, y0, x0 = v, i, j
    bloc = x[y0:y0+n, x0:x0+n]
    fig = plt.figure(figsize=(11, 4.6))
    a1 = fig.add_axes([0.0, 0.05, 0.4, 0.9]); a1.imshow(x, cmap='gray', vmin=0, vmax=255); a1.axis('off')
    a1.add_patch(plt.Rectangle((x0-0.5, y0-0.5), n, n, fill=False, ec='red', lw=2))
    from matplotlib.patches import ConnectionPatch
    a2 = fig.add_axes([0.45, 0.05, 0.5, 0.9]); a2.imshow(bloc, cmap='gray', vmin=0, vmax=255); a2.set_xticks([]); a2.set_yticks([])
    for i in range(n):
        for j in range(n):
            v = bloc[i, j]; a2.text(j, i, str(v), ha='center', va='center', fontsize=11, color='white' if v < 128 else 'black')
    for k in range(n+1):
        a2.axhline(k-0.5, color='red', lw=0.6); a2.axvline(k-0.5, color='red', lw=0.6)
    for (ya, yb) in [(y0-0.5, -0.5), (y0+n-0.5, n-0.5)]:
        fig.add_artist(ConnectionPatch(xyA=(x0+n-0.5, ya), coordsA=a1.transData, xyB=(-0.5, yb), coordsB=a2.transData, ls='--', color='red', lw=0.8))
    fig.savefig(f'{OUT}/fig1_2_matrice.png', dpi=200, bbox_inches='tight'); plt.close(fig)

# ---------- Figure 1.3 : LSB, du pixel à l'image ----------
def fig_lsb(x):
    fig = plt.figure(figsize=(11, 4.2))
    ax = fig.add_subplot(1, 3, 1); ax.axis('off')
    vals = [154, 97, 200, 63, 121, 88, 173, 42]
    bits = [int(b) for b in format(ord('T'), '08b')]   # lettre T de « Teranga »
    rows = []
    for v, b in zip(vals, bits):
        nv = (v & ~1) | b
        rows.append([str(v), f'{v:08b}', str(b), f'{nv:08b}', str(nv)])
    t = ax.table(cellText=rows, colLabels=['Avant', 'Binaire', 'Bit', 'Après', 'Valeur'], loc='center', cellLoc='center')
    t.auto_set_font_size(False); t.set_fontsize(9); t.scale(1.15, 1.35)
    for i, (v, b) in enumerate(zip(vals, bits), start=1):
        if (v & 1) != b: t[i, 3].set_facecolor('#f6c6c6'); t[i, 4].set_facecolor('#f6c6c6')
    ax.set_title('(a) Cacher la lettre « T » (01010100)\ndans huit pixels', fontsize=10)
    ax2 = fig.add_subplot(1, 3, 2); ax2.imshow(x, cmap='gray', vmin=0, vmax=255); ax2.axis('off')
    ax2.set_title('(b) Image en niveaux de gris', fontsize=10)
    ax3 = fig.add_subplot(1, 3, 3); ax3.imshow(x & 1, cmap='gray', interpolation='nearest'); ax3.axis('off')
    ax3.set_title('(c) Plan des bits de poids faible', fontsize=10)
    fig.tight_layout(); fig.savefig(f'{OUT}/fig1_3_lsb.png', dpi=200, bbox_inches='tight'); plt.close(fig)

# ---------- Figure 1.4 : où l'insertion modifie l'image ----------
def fig_modifs(x, charge=0.4):
    # LSB matching : coût uniforme ; HILL : coût adaptatif
    # LSB matching classique : un bit par pixel utilisé, +-1 au hasard si le bit ne correspond pas
    utilise = rng.random(x.shape) < charge
    differe = rng.random(x.shape) < 0.5
    signe = np.where(rng.random(x.shape) < 0.5, 1, -1)
    y_lsbm = x + (utilise & differe) * signe
    y_lsbm[y_lsbm > 255] = 254; y_lsbm[y_lsbm < 0] = 1
    y_hill = simuler(x, cout_hill(x), charge)
    fig, axs = plt.subplots(1, 3, figsize=(11, 4))
    axs[0].imshow(x, cmap='gray', vmin=0, vmax=255); axs[0].set_title('(a) Image de couverture', fontsize=10)
    for ax, y, t in [(axs[1], y_lsbm, '(b) LSB matching'), (axs[2], y_hill, '(c) HILL')]:
        ax.imshow((y != x), cmap='gray_r', interpolation='nearest')
        ax.set_title(f'{t}, ' + str(charge).replace('.', ',') + ' bpp\n' + f'{(y != x).mean()*100:.1f}'.replace('.', ',') + ' % de pixels modifiés', fontsize=10)
    for ax in axs: ax.axis('off')
    fig.tight_layout(); fig.savefig(f'{OUT}/fig1_4_modifications.png', dpi=200, bbox_inches='tight'); plt.close(fig)

# ---------- Figure 1.5 : histogramme avant et après substitution LSB ----------
def fig_histo(x):
    bits = np.random.default_rng(7).integers(0, 2, x.shape)
    y = (x & ~1) | bits                      # substitution LSB, charge maximale
    hh = np.bincount(x.ravel(), minlength=256).astype(float)
    def score(a):
        seg = hh[a:a+32]
        return np.abs(seg[0::2] - seg[1::2]).sum() / max(seg.sum(), 1) if seg.sum() > 0.05 * x.size else 0
    lo = max(range(0, 224, 2), key=score); hi = lo + 31
    fig, axs = plt.subplots(1, 2, figsize=(11, 3.6), sharey=True)
    for ax, im, t in [(axs[0], x, '(a) Avant insertion'), (axs[1], y, '(b) Après substitution LSB')]:
        h = np.bincount(im.ravel(), minlength=256)[lo:hi+1]
        ax.bar(np.arange(lo, hi+1), h, width=0.85, color=['#4c72b0' if v % 2 == 0 else '#dd8452' for v in range(lo, hi+1)])
        ax.set_title(t, fontsize=10); ax.set_xlabel('Valeur du pixel')
    axs[0].set_ylabel("Nombre de pixels")
    fig.tight_layout(); fig.savefig(f'{OUT}/fig1_5_histogramme.png', dpi=200, bbox_inches='tight'); plt.close(fig)

FIG = OUT
PORTRAIT = os.path.join(FIG, 'Cheikh_Anta_Diop,_late_1940s.jpg')        # domaine public
PLAT = os.path.join(FIG, 'Thiéboudiène_Boukhonk_with_tamarind.jpg')       # T.K. Naliaka, CC BY-SA 4.0
BAOBAB = os.path.join(FIG, 'Baobab_du_Sénégal_Palmarin_04.jpg')           # 4MAPS, CC BY-SA 4.0

if __name__ == '__main__':
    fig_chaine()
    fig_matrice(charger(PORTRAIT, taille=None, haut=True), cadre=(110, 160, 60, 120))
    fig_lsb(charger(PLAT, taille=512))
    fig_modifs(charger(BAOBAB, taille=512, centre=0.58))
    fig_histo(charger(BAOBAB, taille=512, centre=0.58))
    print('Figures écrites dans', os.path.abspath(OUT))
