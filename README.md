# Mémoire : stéganalyse face aux contenus générés par IA

Cas pratique du mémoire de master. Ce dépôt contient le code des expériences, la structure des
données et les documents de rédaction.

## Sujet en une phrase

Démontrer que la stéganalyse classique est perturbée par les images générées par IA (modèles de
diffusion), puis esquisser une solution.

## Structure du dépôt

```
notebooks/   code des expériences (Colab)
src/         fonctions réutilisables
data/        corpus et caches (non versionné, sauvegardé sur Google Drive)
results/     tables et figures produites
latex/       documents du mémoire
```

## Périmètre

- Générateurs : Stable Diffusion 1.5, SDXL, ADM
- Algorithmes d'insertion : LSB, S-UNIWARD, HILL
- Images naturelles : BOSSBase
- 1000 images par ensemble, caractéristiques SRM mises en cache

## Notebooks

| Fichier | Rôle |
|---|---|
| 00_preparation_corpus.ipynb | Constitution du corpus |
| 01_extraction_features.ipynb | Extraction et cache des caractéristiques SRM |
| 02_experience_A_domain_shift.ipynb | Décalage de domaine (H1) |
| 03_experience_B_interference.ipynb | Interférence des artefacts (H2) |
| 04_experience_C_solution.ipynb | Solution et généralisation (H3) |

## Journal des étapes

| Date | Phase | Fait | Données associées |
|---|---|---|---|
| 2026-07-26 | 0 | Mise en place du dépôt et de la stratégie | - |
| 2026-07-26 | 1 | Notebook 00 : chaîne validée au test 200, source ADM corrigée | voir CORPUS.md |
| 2026-07-26 | 1 | Notebook 01 : extraction SRM avec cache reprenable | features_srm/ sur Drive |

## Reproductibilité

Graine aléatoire fixée dans tous les notebooks. Versions des bibliothèques dans `requirements.txt`.
Corpus et caches sauvegardés sur Google Drive dans des dossiers datés.
