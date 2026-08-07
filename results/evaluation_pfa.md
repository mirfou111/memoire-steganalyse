# Évaluation de PFA et S-SELECT sur nos données

Tests de la réduction de caractéristiques sur le cas naturel, insertion LSB, caractéristiques SPAM.
Détecteur : régression logistique. AUC mesurée par validation croisée répétée.

## Run 1 : PFA seul, échantillon de 200 images

Ce premier essai mesure l'effet de la réduction PFA seule, sans critère de choix.

| Configuration | Nb caractéristiques | AUC |
|---|---|---|
| Toutes les caractéristiques | 686 | 0,933 |
| S-SELECT (silhouette) | 10 | 0,738 |
| PFA seul | 15 | 0,910 |
| PFA seul | 50 | 0,873 |
| PFA seul | 100 | 0,897 |
| PFA seul | 200 | 0,907 |
| PFA seul | 300 | 0,903 |

PFA seul conserve l'essentiel du signal, même avec peu de caractéristiques. C'est le choix opéré par
le critère silhouette qui fait chuter l'AUC, pas la réduction elle-même.

## Run 2 : comparaison des critères, 1500 images

Comparaison des critères de sélection, à 0,4 bpp, sur le corpus complet.

| Méthode | Nb caractéristiques | AUC |
|---|---|---|
| Toutes les caractéristiques | 686 | 0,981 |
| S-SELECT silhouette (non supervisé) | 11 | 0,721 |
| S-SELECT supervisé, jusqu'à 30 | 27 | 0,824 |
| S-SELECT supervisé, jusqu'à 100 | 100 | 0,956 |
| Top 15 par test F (univarié) | 15 | 0,624 |

## Lecture d'ensemble

Trois enseignements se dégagent.

PFA est un réducteur efficace. Combiné à un critère supervisé, il ramène l'AUC à 0,956 avec 100
caractéristiques sur 686, soit 97 pour cent de la performance des caractéristiques complètes. Le point de
fonctionnement se situe autour de 100 caractéristiques, pas une quinzaine. Réduire trop coûte cher, car le
signal de l'insertion est diffus.

Le critère silhouette, non supervisé, échoue dans notre montage. En cherchant le meilleur découpage en
deux groupes, il suit le contenu des images plutôt que l'insertion, dont la trace est minuscule. L'AUC
tombe à 0,721. Cette limite tient même à l'intérieur d'une seule source.

La sélection univariée par test F est la pire, à 0,624. Choisir les caractéristiques individuellement les
plus corrélées à l'étiquette ne marche pas : le signal n'est pas concentré dans quelques caractéristiques
fortes, il est réparti sur beaucoup, qui ne comptent qu'ensemble. C'est la justification même des modèles
riches et des classifieurs d'ensemble.

## Conclusion et portée

PFA se généralise à notre cas, et une variante supervisée, qui garde PFA pour enlever les redondances mais
choisit les caractéristiques par leur pouvoir de séparation cover contre stégo, surmonte la limite du
critère silhouette d'origine. C'est une extension du travail de l'encadrant, à lui présenter.

L'intérêt réel de cette réduction n'apparaît pas sur SPAM, qui ne fait que 686 dimensions et reste
exploitable tel quel, mais sur SRM et ses 34000 dimensions, où passer à quelques centaines de
caractéristiques serait un gain de calcul déterminant. Les résultats sur SPAM donnent confiance que le
procédé y transférera. L'évaluation sur SRM à grande échelle est prévue une fois les caractéristiques
extraites sur serveur.

## Réserve méthodologique

Choisir la taille du sous-ensemble sur la même AUC que l'on rapporte est légèrement optimiste. Pour le
chiffre final du mémoire, le sous-ensemble retenu sera réévalué sur des données mises de côté.
