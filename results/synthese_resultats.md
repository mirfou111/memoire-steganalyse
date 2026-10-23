% Cas pratique : stéganalyse face aux images générées — synthèse des résultats
% Ousmane Ndiéguène
% Septembre 2026

## Objet

Ce document synthétise le cas pratique à son état final, sur caractéristiques SRM et corpus de quatre
sources à 10000 images chacune : naturel (BOSSbase), Stable Diffusion (DiffusionDB), Midjourney et ADM
(GenImage). Trois algorithmes d'insertion, LSB, S-UNIWARD, HILL, à 0,4 bpp. Le détail par expérience est
dans les fiches `results/experience_*.md`.

## 1. Décalage de domaine (Expérience A)

Un détecteur entraîné sur le naturel est appliqué aux sources générées. Références sur le naturel : LSB
0,994, S-UNIWARD 0,784, HILL 0,711. La détection des adaptatifs a progressé avec les données, contre
environ 0,70 et 0,60 à 5000 images.

Le décalage est sévère et général : en cross-domaine, l'AUC tombe vers 0,53 à 0,89 selon la source et
l'algorithme, et les faux positifs explosent, de 47 % à 90 % contre 5 % visés. Réentraîné par source, le
détecteur récupère très bien pour LSB (0,96 à 0,99), et pour l'adaptatif sur Midjourney et ADM, mais reste
au niveau du hasard sur Stable Diffusion en adaptatif.

## 2. Interférence des artefacts (Expérience B)

Distance de Mahalanobis cover vers stégo, sans détecteur. Une distance plus faible que le naturel signale
un masquage.

| Algorithme | naturel | Stable Diffusion | Midjourney | ADM |
|---|---|---|---|---|
| LSB | 1,633 | 1,331 | 1,754 | 1,540 |
| S-UNIWARD | 0,912 | 0,534 | 1,297 | 0,974 |
| HILL | 0,772 | 0,459 | 1,169 | 0,745 |

Stable Diffusion masque l'insertion pour les trois algorithmes, fortement sur les adaptatifs, environ 40 %
sous le naturel. Midjourney fait l'inverse, la trace y ressort davantage, effet de contenu plus lisse. ADM
reste au niveau du naturel.

## 3. Adaptation du détecteur (Expérience C)

Sur LSB, l'adaptation répare le décalage de domaine partout : Stable Diffusion remonte de 0,733 à 0,95,
Midjourney à 0,99, ADM à 0,96, et un détecteur mixte unique égale les détecteurs spécialisés. Sur
l'adaptatif, elle récupère sur Midjourney et ADM (S-UNIWARD Midjourney de 0,61 à 0,88), mais bute sur
Stable Diffusion, où même le détecteur apparié reste au hasard (0,56 pour S-UNIWARD, 0,52 pour HILL). Le
réentraînement répare le décalage de domaine, pas l'interférence.

## 4. Attribution multi-classe (Expérience D)

Sur le naturel, on cherche à identifier l'algorithme parmi cover, LSB, S-UNIWARD, HILL. Exactitude 0,581
pour un hasard à 0,25. LSB est identifié presque parfaitement (F1 0,914) ; cover, S-UNIWARD et HILL se
confondent. Le critère de sélection non supervisé à k égal quatre échoue (accord nul avec les classes), ce
qui justifie la variante supervisée.

## 5. Réduction de caractéristiques (méthode PFA)

La méthode de l'encadrant, PFA et son enveloppe S-SELECT, ramène les 34000 descripteurs SRM à quelques
dizaines en conservant l'essentiel de la performance (24 caractéristiques pour environ 0,91 sur SRM en cas
LSB). Le critère non supervisé d'origine échoue quand le contenu domine la trace ; une variante supervisée,
contribution de ce travail, le corrige.

## 6. Ce que l'ensemble établit

L'image générée perturbe la stéganalyse classique sur deux plans. Le décalage de domaine est général et se
répare par adaptation du détecteur, sauf sur Stable Diffusion en adaptatif. L'interférence est portée par
Stable Diffusion seul et ne se répare pas, le signal y étant physiquement masqué. Midjourney, source
commerciale, se comporte à l'opposé, l'insertion y étant plus visible. La détection des adaptatifs progresse
avec les données.

Limite à garder en tête : Stable Diffusion vient de DiffusionDB, au contenu artistique, alors que Midjourney
et ADM sont sur contenu ImageNet ; l'effet du générateur et celui du contenu restent partiellement
confondus, à lever avec une seconde source Stable Diffusion.
