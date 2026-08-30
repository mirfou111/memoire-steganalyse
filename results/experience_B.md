# Expérience B : interférence des artefacts

## Objectif

Tester l'hypothèse H2 : sur les images générées, la trace de l'insertion est masquée par les artefacts de
génération, ce qui rend le déplacement cover vers stégo plus faible que sur le naturel. La mesure ne demande
aucun détecteur entraîné, ce qui la rend valable même pour les algorithmes adaptatifs.

## Une première mesure écartée

Une tentative par moments globaux du résidu (variance, asymétrie, kurtosis, entropie) et taille d'effet de
Cohen donnait des effets négligeables sur toutes les sources. Ces statistiques globales sont trop
grossières pour capter une insertion adaptative, ce qui est précisément la raison pour laquelle la
stéganalyse a délaissé les statistiques simples. Cette piste est donc écartée.

## Mesure retenue : distance multivariée sur SRM

On mesure l'ampleur du déplacement cover vers stégo par la distance de Mahalanobis entre les deux
distributions. SRM ayant des dizaines de milliers de dimensions, sa covariance complète saturerait la
mémoire ; on réduit donc d'abord par PCA à quelques centaines de composantes, avec la même réduction pour
toutes les sources, ce qui garde la comparaison valable. Une distance plus faible sur une source générée
que sur le naturel signale un masquage de l'insertion.

## Résultats (SRM, 0,4 bpp)

| Algorithme | naturel | Stable Diffusion | SDXL | ADM |
|---|---|---|---|---|
| LSB | 1,56 | 1,31 | 1,76 | 1,65 |
| S-UNIWARD | 0,74 | 0,55 | 1,05 | 1,10 |
| HILL | 0,58 | 0,50 | 0,84 | 0,90 |

Résultat stable que la réduction garde 100 ou 200 composantes.

Figures : `expB_srm_maha_<algo>_p04.png` (distances par source) et `expB_srm_proj2d_<algo>_p04.png`
(projection 2D, illustrative uniquement).

## Interprétation

Sur Stable Diffusion, la distance passe sous le niveau naturel pour les trois algorithmes : l'insertion y
est effectivement masquée. L'effet est net pour LSB et S-UNIWARD, plus marginal pour HILL. Sur SDXL et ADM,
la distance reste au-dessus du naturel, l'insertion y ressort même davantage, donc pas de masquage.

Ce résultat converge avec l'Expérience A : parmi les trois générateurs, Stable Diffusion est le seul qui
perturbe la stéganalyse, tandis que SDXL et ADM se comportent comme des images naturelles. Le passage à SRM
apporte ici un gain décisif par rapport à SPAM : l'interférence est mesurée aussi sur les algorithmes
adaptatifs, ce que SPAM ne permettait pas.

Note sur les projections 2D : elles écrasent 34000 dimensions sur deux axes, dominés par le contenu et la
source, pas par l'insertion. Le fort chevauchement des classes y est donc attendu et n'infirme pas le
résultat ; la preuve tient à la distance multivariée, pas au nuage. Les projections restent illustratives.

## Limites

Stable Diffusion provenant de DiffusionDB, l'effet observé pourrait tenir en partie au pipeline de la base
plutôt qu'au seul générateur. À vérifier avec une autre source Stable Diffusion.
