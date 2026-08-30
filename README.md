# Stéganalyse à l'ère des images générées par IA

Et si les images qui inondent aujourd'hui le web, celles que produisent les modèles de diffusion,
mettaient en défaut les outils qui traquent les messages cachés ? Ce dépôt est le cas pratique d'un
mémoire de master qui pose la question et y répond par l'expérience : il démontre, chiffres à l'appui, que
la stéganalyse classique se trompe face aux images d'IA, explique pourquoi, et montre comment y remédier.

## L'histoire en une phrase

Une image générée par IA n'est pas une image naturelle : elle porte ses propres traces, et ces traces
suffisent à dérégler un détecteur de stéganographie entraîné sur des photos réelles.

## Ce que le travail établit

Trois expériences, menées sur un même corpus et avec les mêmes outils, racontent une histoire cohérente.

Le décalage de domaine. Un détecteur entraîné sur des images naturelles s'effondre sur les images
générées : sur Stable Diffusion, il crie au message caché sur 83 % d'images pourtant vierges. Le problème
vient du changement de domaine, pas de la méthode, puisque réentraîner le détecteur sur la bonne source le
remet d'aplomb.

L'interférence. En mesurant directement l'écart entre une image vierge et sa version porteuse, on voit que
Stable Diffusion masque l'insertion, là où SDXL et ADM ne la masquent pas. Stable Diffusion est ainsi la
seule source à cumuler les deux difficultés.

La solution. Adapter le détecteur, en le réentraînant sur un mélange de naturel et de généré ou en
l'aiguillant selon la source reconnue, restaure l'essentiel de la performance perdue et ramène Stable
Diffusion au niveau atteignable en conditions idéales.

En parallèle, le dépôt met en œuvre et prolonge la méthode de réduction de caractéristiques de
l'encadrant, PFA et S-SELECT, avec une variante supervisée qui ramène les 34000 descripteurs SRM à
quelques dizaines sans presque rien perdre.

## Le corpus

Quatre sources d'images traitées à l'identique, pour que seule leur origine les distingue : naturel
(BOSSbase), Stable Diffusion (DiffusionDB), SDXL et ADM. Trois algorithmes d'insertion, du plus naïf au
plus fin : LSB, S-UNIWARD, HILL. Caractéristiques SRM mises en cache. Cible de 1500 images par source, et
une extension du naturel à 5000 pour pousser le cas difficile des algorithmes adaptatifs.

## Structure du dépôt

```
notebooks/   les expériences, prêtes à exécuter sur Colab
src/         fonctions réutilisables, dont l'implémentation de PFA
data/        corpus et caches, non versionnés, sauvegardés sur Google Drive
results/     tables, figures et fiches explicatives
memoire/     la rédaction du mémoire
```

## Les notebooks

| Fichier | Rôle |
|---|---|
| 00_preparation_corpus.ipynb | Constitution du corpus |
| 01_extraction_features.ipynb | Extraction et cache des caractéristiques SRM |
| 02_experience_A_domain_shift.ipynb | Décalage de domaine (H1) |
| 03_experience_B_interference.ipynb | Interférence des artefacts (H2) |
| 04_experience_C_solution.ipynb | Adaptation du détecteur (H3) |

## Pour aller au fond

Les fiches de `results/` détaillent chaque brique : le protocole et les résultats de chaque expérience,
la méthode du détecteur et le choix assumé de ne pas recourir au deep learning, la mécanique de PFA et
S-SELECT, et un historique des détecteurs en stéganalyse. La synthèse chiffrée se trouve dans
`results/synthese_resultats.md`.

## Reproductibilité

Graine aléatoire fixée dans tous les notebooks, versions des bibliothèques dans `requirements.txt`, corpus
et caches archivés sur Google Drive. L'extraction lourde de SRM a été menée sur un serveur seize cœurs,
dont la mise en place est décrite dans `VPS_SETUP.md`.
