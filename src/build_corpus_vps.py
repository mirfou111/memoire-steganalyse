"""
Construction du corpus a 10000 images par source, pour le VPS.

Quatre sources, traitees a l'identique : naturel (BOSSbase), SD (DiffusionDB),
ADM et Midjourney (GenImage via depots bitmind). Aucun redimensionnement : on
recadre au centre en 256x256 puis on enregistre en PGM sans perte, pour ne pas
corrompre les statistiques que lit la stéganalyse.

Le script est reprenable. Chaque source compte ses fichiers deja presents et
reprend la ou elle s'etait arretee. On peut donc le relancer sans risque apres
une coupure. Concu pour tourner en session detachee (tmux ou nohup) sur le VPS,
il ne depend pas de la connexion locale.
"""

import os
import io
import sys
import time
import zipfile
import subprocess

from PIL import Image, ImageFile

# tolere les images legerement tronquees plutot que de lever une erreur
ImageFile.LOAD_TRUNCATED_IMAGES = True

# ================= CONFIGURATION =================
TARGET_SIZE = 256                 # cote du recadrage central, en pixels
N_PAR_SOURCE = 10000              # images visees par source
BASE_DIR = os.path.abspath("./corpus_10k")
# URLs candidates pour BOSSbase, essayees dans l'ordre
BOSSBASE_URLS = [
    "http://dde.binghamton.edu/download/ImageDB/BOSSbase_1.01.zip",
    "http://agents.fel.cvut.cz/boss/data/BOSSbase_1.01.zip",
]
# ================================================


def recadrer_centre(img):
    """Convertit en niveaux de gris et recadre au centre en TARGET_SIZE.
    Renvoie None si l'image est trop petite, pour ne jamais avoir a redimensionner."""
    if img.mode != "L":
        img = img.convert("L")
    l, h = img.size
    if l < TARGET_SIZE or h < TARGET_SIZE:
        return None
    gauche = (l - TARGET_SIZE) // 2
    haut = (h - TARGET_SIZE) // 2
    return img.crop((gauche, haut, gauche + TARGET_SIZE, haut + TARGET_SIZE))


def compter(dossier):
    if not os.path.isdir(dossier):
        return 0
    return len([f for f in os.listdir(dossier) if f.endswith(".pgm")])


def enregistrer(img, dossier, index):
    crop = recadrer_centre(img)
    if crop is None:
        return False
    crop.save(os.path.join(dossier, f"{index:05d}.pgm"))
    return True


# ---------------------------------------------------------------- naturel

def construire_naturel():
    dossier = os.path.join(BASE_DIR, "cover_natural")
    os.makedirs(dossier, exist_ok=True)
    fait = compter(dossier)
    if fait >= N_PAR_SOURCE:
        print(f"[natural] deja complet ({fait}).")
        return
    print(f"[natural] {fait} presentes, cible {N_PAR_SOURCE}.")

    zip_path = os.path.join(BASE_DIR, "BOSSbase_1.01.zip")
    if not os.path.exists(zip_path):
        ok = False
        for url in BOSSBASE_URLS:
            print(f"[natural] telechargement reprenable depuis {url}")
            # wget -c reprend un telechargement interrompu
            code = subprocess.call(["wget", "-c", "-O", zip_path, url])
            if code == 0 and os.path.getsize(zip_path) > 100_000_000:
                ok = True
                break
            print(f"[natural] echec sur {url}, essai suivant.")
        if not ok:
            print("[natural] aucune URL n'a fonctionne. Depose BOSSbase_1.01.zip "
                  f"manuellement dans {BASE_DIR} puis relance.")
            return

    print("[natural] extraction et recadrage.")
    with zipfile.ZipFile(zip_path) as z:
        pgms = [n for n in z.namelist() if n.endswith(".pgm")]
        index = fait
        for n in pgms:
            if index >= N_PAR_SOURCE:
                break
            cible = os.path.join(dossier, f"{index + 1:05d}.pgm")
            if os.path.exists(cible):
                index += 1
                continue
            try:
                with z.open(n) as f:
                    img = Image.open(io.BytesIO(f.read()))
                if enregistrer(img, dossier, index + 1):
                    index += 1
            except Exception:
                continue
            if index % 500 == 0:
                print(f"[natural] {index}/{N_PAR_SOURCE}")
    print(f"[natural] termine : {compter(dossier)} images.")


# ---------------------------------------------------------------- SD (DiffusionDB)

def construire_sd():
    from huggingface_hub import hf_hub_download
    dossier = os.path.join(BASE_DIR, "cover_sd")
    os.makedirs(dossier, exist_ok=True)
    fait = compter(dossier)
    if fait >= N_PAR_SOURCE:
        print(f"[sd] deja complet ({fait}).")
        return
    print(f"[sd] {fait} presentes, cible {N_PAR_SOURCE}.")

    index = fait
    partie = 1
    # chaque archive part-XXXXXX.zip contient environ 1000 images PNG
    while index < N_PAR_SOURCE and partie <= 30:
        nom = f"images/part-{partie:06d}.zip"
        try:
            chemin = hf_hub_download(repo_id="poloclub/diffusiondb", filename=nom,
                                     repo_type="dataset")
        except Exception as e:
            print(f"[sd] partie {partie} indisponible ({e}), suivante.")
            partie += 1
            continue
        with zipfile.ZipFile(chemin) as z:
            for n in z.namelist():
                if index >= N_PAR_SOURCE:
                    break
                if not n.lower().endswith(".png"):
                    continue
                try:
                    with z.open(n) as f:
                        img = Image.open(io.BytesIO(f.read()))
                    if enregistrer(img, dossier, index + 1):
                        index += 1
                except Exception:
                    continue
        print(f"[sd] partie {partie} traitee, {index}/{N_PAR_SOURCE}")
        partie += 1
    print(f"[sd] termine : {compter(dossier)} images.")


# ------------------------------------------------ ADM et Midjourney (GenImage)

def construire_genimage(nom_source, repo):
    from datasets import load_dataset, Image as HFImage
    dossier = os.path.join(BASE_DIR, f"cover_{nom_source}")
    os.makedirs(dossier, exist_ok=True)
    fait = compter(dossier)
    if fait >= N_PAR_SOURCE:
        print(f"[{nom_source}] deja complet ({fait}).")
        return
    print(f"[{nom_source}] {fait} presentes, cible {N_PAR_SOURCE}, depot {repo}.")

    # decode=False : datasets renvoie les octets bruts sans decoder l'image lui-meme.
    # On decode nous-memes dans un try/except, ce qui rend une image corrompue
    # rattrapable au lieu de faire planter le decodeur C et l'interpreteur.
    ds = load_dataset(repo, split="train", streaming=True)
    ds = ds.cast_column("image", HFImage(decode=False))

    index = 0          # position dans le flux
    saved = fait       # images deja enregistrees
    ignorees = 0
    for row in ds:
        if saved >= N_PAR_SOURCE:
            break
        # on saute ce qui a deja ete enregistre lors d'un run precedent
        if index < fait:
            index += 1
            continue
        index += 1
        rec = row.get("image")
        octets = rec.get("bytes") if isinstance(rec, dict) else None
        if not octets:
            ignorees += 1
            continue
        try:
            img = Image.open(io.BytesIO(octets))
            img.load()                       # force le decodage ici, sous try
            if enregistrer(img, dossier, saved + 1):
                saved += 1
            else:
                ignorees += 1
        except Exception:
            ignorees += 1
            continue
        if saved % 500 == 0 and saved > 0:
            print(f"[{nom_source}] {saved}/{N_PAR_SOURCE} (ignorees {ignorees})")
    print(f"[{nom_source}] termine : {compter(dossier)} images, {ignorees} ignorees.")


def main():
    os.makedirs(BASE_DIR, exist_ok=True)
    t0 = time.time()
    print("Construction du corpus 10k, dossier de sortie :", BASE_DIR)

    construire_naturel()
    construire_sd()
    construire_genimage("adm", "bitmind/GenImage_ADM")
    construire_genimage("midjourney", "bitmind/GenImage_MidJourney")

    print("\nRecapitulatif :")
    for s in ["natural", "sd", "adm", "midjourney"]:
        print(f"  {s:11s} {compter(os.path.join(BASE_DIR, f'cover_{s}'))}")
    print(f"Duree totale : {(time.time() - t0) / 60:.1f} min")


if __name__ == "__main__":
    main()
