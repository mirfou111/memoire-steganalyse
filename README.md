# Stéganalyse à l'ère des images générées par IA

Et si les images qui inondent aujourd'hui le web, celles que produisent les modèles de diffusion,
mettaient en défaut les outils qui traquent les messages cachés ? Ce dépôt est le cas pratique d'un
mémoire de master qui pose la question et y répond par l'expérience : il démontre, chiffres à l'appui, que
la stéganalyse classique se trompe face aux images d'IA, explique pourquoi, et montre comment y remédier.

## L'histoire en une phrase

Une image générée par IA n'est pas une image naturelle : elle porte ses propres traces, et ces traces
suffisent à dérégler un détecteur de stéganographie entraîné sur des photos réelles.

## Ce que le travail établit

Quatre expériences, menées sur un même corpus et avec les mêmes outils, racontent une histoire cohérente.

Le décalage de domaine. Un détecteur entraîné sur des images naturelles s'effondre sur les images
générées : sur Stable Diffusion, il crie au message caché sur plus de 70 % d'images pourtant vierges. Le
problème vient du changement de domaine, pas de la méthode, puisque réentraîner le détecteur sur la bonne
source le remet d'aplomb.

L'interférence. En mesurant directement l'écart entre une image vierge et sa version porteuse, on voit que
Stable Diffusion masque l'insertion, là où Midjourney et ADM ne la masquent pas. Stable Diffusion est ainsi
la seule source à cumuler les deux difficultés.

La solution. Adapter le détecteur, en le réentraînant sur un mélange de naturel et de généré ou en
l'aiguillant selon la source reconnue, restaure l'essentiel de la performance perdue, sauf sur Stable
Diffusion en insertion adaptative, où l'interférence masque le signal au point qu'aucun réentraînement ne
le récupère.

L'attribution. Au-delà de la question binaire, on cherche à identifier quel algorithme a servi. LSB se
reconnaît presque parfaitement, mais les schémas adaptatifs se confondent entre eux.

En parallèle, le dépôt met en œuvre et prolonge la méthode de réduction de caractéristiques de
l'encadrant, PFA et S-SELECT, avec une variante supervisée qui ramène les 34000 descripteurs SRM à
quelques dizaines sans presque rien perdre.

## Le corpus

Quatre sources d'images traitées à l'identique, pour que seule leur origine les distingue : naturel
(BOSSbase), Stable Diffusion (DiffusionDB), Midjourney et ADM (tous deux via GenImage). Trois algorithmes
d'insertion, du plus naïf au plus fin : LSB, S-UNIWARD, HILL, à 0,4 bpp. Caractéristiques SRM mises en cache.
10000 images par source, ce qui permet de pousser le cas difficile des algorithmes adaptatifs.

## Structure du dépôt

```
notebooks/   les expériences, version Colab
src/         scripts VPS (corpus, insertion, extraction, expériences) et implémentation de PFA
data/        corpus et caches, non versionnés, sauvegardés sur Google Drive
results/     tables, figures et fiches explicatives
memoire/     la rédaction du mémoire
```

## Les notebooks et scripts

| Fichier | Rôle |
|---|---|
| notebooks/00 à 05 | Version Colab des étapes, de la constitution du corpus aux quatre expériences |
| src/build_corpus_vps.py | Téléchargement et prétraitement des quatre sources |
| src/insert_corpus_vps.py | Insertion stéganographique des trois algorithmes |
| src/extract_srm_vps.py | Extraction SRM parallèle et reprenable |
| src/run_experiment_A_vps.py à D | Les quatre expériences en scripts, résultats et figures |

Les résultats définitifs à 10000 images ont été produits par les scripts `src/run_experiment_*_vps.py`, plus
fiables qu'un notebook à cette échelle ; les notebooks en sont la version pédagogique.

## Les quatre expériences

A, décalage de domaine (H1). B, interférence des artefacts (H2). C, adaptation du détecteur (H3). D,
attribution multi-classe de l'algorithme d'insertion.

## Pour aller au fond

Les fiches de `results/` détaillent chaque brique : le protocole et les résultats de chaque expérience,
la méthode du détecteur et le choix assumé de ne pas recourir au deep learning, la mécanique de PFA et
S-SELECT, et un historique des détecteurs en stéganalyse. La synthèse chiffrée se trouve dans
`results/synthese_resultats.md`.

## Reproductibilité

Graine aléatoire fixée dans tous les notebooks, versions des bibliothèques dans `requirements.txt`, corpus
et caches archivés sur Google Drive. L'extraction lourde de SRM a été menée sur un serveur seize cœurs,
dont la mise en place est décrite dans `VPS_SETUP.md`.
