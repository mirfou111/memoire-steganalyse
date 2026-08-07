# Expérience B : interférence des artefacts

## Objectif

Tester l'hypothèse H2 : sur les images générées, la trace de l'insertion est masquée par les artefacts
de génération, ce qui rend le déplacement cover vers stégo plus faible que sur le naturel. La mesure ne
demande aucun détecteur entraîné.

## Mesure 1 : moments globaux du résidu (écartée)

Première tentative avec quatre statistiques globales du résidu haute fréquence, variance, asymétrie,
kurtosis, entropie, et la taille d'effet de Cohen entre cover et stégo.

Résultat, pour S-UNIWARD à 0,4 bpp : des tailles d'effet toutes négligeables, entre 0,02 et 0,05, sur
toutes les sources. Ces moments globaux sont trop grossiers pour capter une insertion adaptative. C'est la
raison même pour laquelle la stéganalyse a délaissé les statistiques simples au profit des modèles riches.
Cette mesure est donc écartée, elle ne révèle pas l'interférence.

## Mesure 2 : distance multivariée sur caractéristiques (retenue)

On mesure l'ampleur du déplacement cover vers stégo par la distance de Mahalanobis entre les deux
distributions, dans l'espace complet des caractéristiques SPAM, avec une covariance régularisée. C'est un
descripteur qui capte réellement l'insertion, et la mesure reste sans détecteur entraîné.

Pour l'insertion LSB à 0,4 bpp :

| Source | Distance cover vers stégo |
|---|---|
| natural | 1,607 |
| sd | 1,397 |
| sdxl | 1,718 |
| adm | 1,710 |

## Interprétation

Stable Diffusion présente la distance la plus faible, 1,397 contre 1,607 pour le naturel, soit environ
13 pour cent de masquage. L'insertion y est donc la plus difficile à distinguer, ce qui est la signature
de l'interférence. SDXL et ADM, à 1,718 et 1,710, se situent au niveau du naturel ou légèrement au dessus,
sans masquage.

Ce résultat converge avec l'Expérience A : parmi les trois générateurs, Stable Diffusion est celui qui
perturbe la stéganalyse, tandis que SDXL et ADM se comportent comme des images naturelles. L'effet est
modéré mais constant d'une expérience à l'autre.

## Limites

Comme SD provient de DiffusionDB, l'effet observé pourrait tenir en partie au pipeline de la base plutôt
qu'au seul générateur. À vérifier avec une autre source Stable Diffusion.

La mesure ne vaut que pour LSB, car SPAM ne capte pas les algorithmes adaptatifs S-UNIWARD et HILL. La
caractérisation de leur interférence demande les caractéristiques SRM à grande échelle, contrainte déjà
identifiée pour la détection. Elle reste une limite assumée à ce stade.
