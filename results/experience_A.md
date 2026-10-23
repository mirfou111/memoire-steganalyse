# Expérience A : décalage de domaine

## Objectif

Tester l'hypothèse H1 : un détecteur entraîné sur des images naturelles perd sa fiabilité sur des images
générées. On mesure l'AUC de référence sur le naturel, l'AUC en cross-domaine du détecteur naturel appliqué
aux sources générées, l'AUC appariée d'un détecteur réentraîné sur chaque source, et le taux de faux
positifs à seuil calibré pour 5 % de fausses alarmes sur le naturel.

## Protocole

Caractéristiques SRM, détecteur linéaire précédé d'une réduction (normalisation, PCA à 300 composantes,
régression logistique), validation croisée. Corpus des quatre sources à 10000 images : naturel, Stable
Diffusion, Midjourney, ADM. Trois algorithmes d'insertion à 0,4 bpp : LSB, S-UNIWARD, HILL.

## Résultats (SRM, 0,4 bpp, 10000 images par source)

Cas LSB. Référence naturel : AUC 0,994.

| Source | AUC cross-domaine | AUC appariée | Faux positifs |
|---|---|---|---|
| Stable Diffusion | 0,729 | 0,962 | 0,712 |
| Midjourney | 0,801 | 0,997 | 0,614 |
| ADM | 0,886 | 0,980 | 0,479 |

Cas S-UNIWARD. Référence naturel : AUC 0,784.

| Source | AUC cross-domaine | AUC appariée | Faux positifs |
|---|---|---|---|
| Stable Diffusion | 0,561 | 0,603 | 0,736 |
| Midjourney | 0,620 | 0,900 | 0,878 |
| ADM | 0,687 | 0,806 | 0,670 |

Cas HILL. Référence naturel : AUC 0,711.

| Source | AUC cross-domaine | AUC appariée | Faux positifs |
|---|---|---|---|
| Stable Diffusion | 0,532 | 0,557 | 0,775 |
| Midjourney | 0,566 | 0,846 | 0,901 |
| ADM | 0,601 | 0,683 | 0,762 |

Figures : `expA_srm_roc_<algo>_p04.png`, `expA_srm_aucbars_<algo>_p04.png`, `expA_srm_fprcdf_<algo>_p04.png`.

## Interprétation

La détection des algorithmes adaptatifs progresse avec les données. La référence sur le naturel atteint
0,784 pour S-UNIWARD et 0,711 pour HILL, contre environ 0,70 et 0,60 à 5000 images. Le plafond observé aux
échelles précédentes venait donc bien du volume de données, pas de la méthode. On reste sous le régime de la
littérature, mais la progression est réelle et mesurée.

Le décalage de domaine est confirmé et sévère, plus encore sur l'adaptatif. Appliqué aux sources générées,
le détecteur naturel tombe vers 0,53 à 0,69 d'AUC, proche du hasard, et le taux de faux positifs explose,
de 47 % à 90 % selon la source et l'algorithme, contre une cible de 5 %. En conditions réelles, ce détecteur
signalerait comme porteuses la quasi-totalité d'images générées vierges.

Le point le plus important est la colonne appariée, car elle sépare les deux problèmes. Sur Midjourney et
ADM, le réentraînement par source récupère largement la performance, y compris sur l'adaptatif : Midjourney
remonte à 0,900 et 0,846, au-dessus même de la référence naturelle, ADM à 0,806 et 0,683. Sur Stable
Diffusion au contraire, le détecteur apparié reste proche du hasard sur l'adaptatif, 0,603 et 0,557.
Autrement dit, le réentraînement répare le simple décalage de domaine, mais bute sur Stable Diffusion, où le
signal est physiquement masqué. Ce constat converge avec l'Expérience B, dans laquelle Stable Diffusion est
la seule source à masquer l'insertion : on en voit ici la conséquence directe sur la détectabilité.

Enfin, un détail cohérent avec la question de la sélection de couverture : sur Midjourney, une fois le
détecteur apparié, l'adaptatif est plus détectable que sur le naturel, car ses images plus lisses laissent
la trace plus visible. Une source commerciale où dissimuler un message est en réalité plus risqué.

## Synthèse

À 10000 images, la détection des algorithmes adaptatifs progresse, le décalage de domaine se répare par
réentraînement sur toutes les sources sauf Stable Diffusion, où l'interférence l'en empêche.

## Limites

Stable Diffusion provient de DiffusionDB, au contenu artistique, tandis que Midjourney et ADM sont sur
contenu ImageNet. L'effet du générateur et celui du contenu restent partiellement confondus. Les AUC sont
rapportées en validation simple à cinq plis ; l'écart type sur la référence est de l'ordre de 0,005, donc
négligeable à cette échelle.
