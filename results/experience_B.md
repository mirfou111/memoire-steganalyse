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

La projection en deux dimensions, envisagée au départ, a été écartée : elle écrase des dizaines de milliers
de dimensions sur deux axes qui captent le contenu et la source, pas l'insertion, et donne donc un nuage
trompeur. La preuve tient à la distance multivariée, pas à la projection.

## Résultats (SRM, 0,4 bpp, 10000 images par source)

Corpus des quatre sources : naturel, Stable Diffusion, Midjourney, ADM.

| Algorithme | naturel | Stable Diffusion | Midjourney | ADM |
|---|---|---|---|---|
| LSB | 1,633 | 1,331 | 1,754 | 1,540 |
| S-UNIWARD | 0,912 | 0,534 | 1,297 | 0,974 |
| HILL | 0,772 | 0,459 | 1,169 | 0,745 |

Figures : `expB_srm_maha_<algo>_p04.png`.

## Interprétation

Stable Diffusion masque l'insertion pour les trois algorithmes, et fortement sur les adaptatifs :
S-UNIWARD passe de 0,912 à 0,534, soit 41 % sous le niveau naturel, HILL de 0,772 à 0,459, soit 40 %. Pour
LSB, 19 % sous le naturel. Le masquage est donc le plus net là où il compte le plus, sur les algorithmes
conçus pour être discrets. C'est le signal d'interférence, confirmé à grande échelle.

Midjourney fait l'inverse : ses distances sont au-dessus du niveau naturel pour tous les algorithmes,
nettement pour les adaptatifs, 1,297 et 1,169 contre 0,912 et 0,772. L'insertion y ressort donc davantage
que sur des images naturelles, sans aucun masquage. C'est vraisemblablement un effet de complexité de
contenu : des images plus lisses laissent la trace plus visible, ce qui rejoint la question de la sélection
de couverture. Une source commerciale au comportement opposé à celui de Stable Diffusion.

ADM se tient au niveau du naturel, un peu en dessous pour LSB et HILL, un peu au-dessus pour S-UNIWARD, sans
masquage marqué. Il se comporte comme une image naturelle.

Le constat d'ensemble se durcit avec le passage à 10000 : parmi les générateurs, Stable Diffusion est le
seul qui masque l'insertion, les autres non, et l'effet est le plus prononcé sur les adaptatifs.

## Limites

Stable Diffusion provient de DiffusionDB, au contenu varié et artistique, tandis que Midjourney et ADM sont
sur contenu ImageNet. L'effet du générateur et celui du contenu restent donc partiellement confondus. Une
source Stable Diffusion sur contenu comparable permettrait de trancher. À dire tel quel.
