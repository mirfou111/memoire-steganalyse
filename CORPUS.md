# Fiche du corpus

Manifeste du corpus du cas pratique. Les données ne sont pas versionnées dans git,
elles sont sauvegardées sur Google Drive. Ce fichier trace ce que contient le corpus et où le trouver.

## Vue d'ensemble

Quatre sources d'images traitées à l'identique, trois algorithmes d'insertion, deux charges utiles.
Cible retenue : 1500 images par source.

## Sources

| Source | Origine | Type | Résolution native | Cible | Plafond disponible |
|---|---|---|---|---|---|
| natural | BOSSBase 1.01 | Photos naturelles | 512, gris | 1500 | ~10000 |
| sd | DiffusionDB | Stable Diffusion 1.x, diffusion latente | 512 | 1500 | plusieurs millions |
| sdxl | ostris/sdxl_10_reg | SDXL, diffusion latente | 1024 | 1500 | ~2263 |
| adm | Tiny-GenImage (generator = ADM) | ADM, diffusion espace pixel | 256 | 1500 | ~1750 |

## Prétraitement

Identique pour toutes les sources : conversion en niveaux de gris, recadrage centré 256x256,
enregistrement en PGM sans perte. C'est ce qui rend les sources comparables.

## Insertion

Trois algorithmes simulés via conseal : LSB matching, S-UNIWARD, HILL.
Deux charges utiles : 0.2 et 0.4 bit par pixel.

## Empreinte statistique (contrôle)

Kurtosis moyen des résidus haute fréquence, image vierge, mesuré sur le test à 200 images.
À confirmer sur le run final à 1500.

| Source | Kurtosis |
|---|---|
| natural | 23.53 |
| sd | 16.83 |
| sdxl | 30.98 |
| adm | 52.07 |

Quatre valeurs distinctes confirment quatre domaines statistiques différents.

## Emplacement des données (Google Drive)

- Dossier racine : `https://drive.google.com/drive/folders/1UuOl6mDMaUrWVM3zUwRnRmOgRxd1c5hL?usp=drive_link`
- Archive du corpus : `https://drive.google.com/file/d/1Zn-icmoU35CT167BVpCXTeWnLoJshHEM/view?usp=drive_link`
- Caches de caractéristiques : `https://drive.google.com/drive/folders/19iVU55dI7gQ68Rgbfd9WDd8jxvqBxsfI?usp=drive_link`

## Reproductibilité

- Graine aléatoire : 42
- Notebook de production : `notebooks/00_preparation_corpus.ipynb`
- Versions des bibliothèques : `requirements.txt`

## Journal

| Date | Événement |
|---|---|
| 2026-07-26 | Test à 200 images, chaîne validée, source ADM corrigée, quatre empreintes distinctes |
| _à compléter_ | Run final à 1500 images, archive et liens Drive |
