# Fiche du corpus

Manifeste du corpus du cas pratique. Les données ne sont pas versionnées dans git, elles sont sauvegardées
sur Google Drive. Ce fichier trace ce que contient le corpus et où le trouver.

## Vue d'ensemble

Quatre sources d'images traitées à l'identique, trois algorithmes d'insertion, charge principale 0,4 bpp.
Taille retenue : 10000 images par source.

## Sources

| Source | Origine | Type | Résolution native | Taille |
|---|---|---|---|---|
| natural | BOSSbase 1.01 | Photos naturelles | 512, gris | 10000 |
| sd | DiffusionDB | Stable Diffusion 1.x, diffusion latente | 512 | 10000 |
| midjourney | GenImage (dépôt bitmind) | Midjourney, générateur commercial | variable | 10000 |
| adm | GenImage (dépôt bitmind) | ADM, diffusion espace pixel | 256 | 10000 |

Midjourney a remplacé SDXL, qui n'était pas extensible à 10000 depuis une source unique et cohérente. Il
apporte en plus une source commerciale au panel. Midjourney et ADM partagent la lignée GenImage, contenu
ImageNet, ce qui les rend directement comparables.

## Prétraitement

Identique pour toutes les sources : conversion en niveaux de gris, recadrage centré 256x256, enregistrement
en PGM sans perte. Jamais de redimensionnement, qui corromprait les statistiques lues par la stéganalyse.
C'est ce qui rend les sources comparables.

## Insertion

Trois algorithmes simulés via conseal : LSB matching, S-UNIWARD, HILL. Charge principale 0,4 bit par pixel.

## Emplacement des données (Google Drive)

Dossier `memoire_data` sur le Drive, envoyé depuis le VPS par rclone :

- `features_srm_10k.tgz` : les caractéristiques SRM des seize ensembles (quatre sources, cover plus trois
  algorithmes), à 10000 images.
- `images_avant_insertion.tgz` : les 40000 covers.
- `images_apres_insertion.tgz` : le jeu complet, covers et stégo.

## Reproductibilité

- Graine aléatoire : 42
- Scripts de production : `src/build_corpus_vps.py`, `src/insert_corpus_vps.py`, `src/extract_srm_vps.py`
- Versions des bibliothèques : `requirements.txt`

## Journal

| Date | Événement |
|---|---|
| 2026-07 | Test à 200 images, chaîne validée, empreintes de sources distinctes |
| 2026-08 | Extraction SRM à 1500 puis extension du naturel à 5000 sur VPS |
| 2026-09 | Corpus final à 10000 par source, Midjourney à la place de SDXL, extraction SRM des seize ensembles, sauvegarde sur Drive |
