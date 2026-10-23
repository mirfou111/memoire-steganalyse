# Expérience D : stéganalyse multi-classe (attribution d'algorithme)

## Idée

Passer de la question binaire, vierge ou porteuse, à une question plus fine : quel algorithme d'insertion a
été utilisé. C'est la stéganalyse multi-classe, ou attribution d'algorithme. L'exploration teste aussi une
intuition sur la méthode de l'encadrant : régler le k du k-means de S-SELECT sur le nombre de classes
réelles pour étendre la sélection au cas multi-classe.

## Démarche

Source naturelle, quatre classes sur les mêmes images : cover, LSB, S-UNIWARD, HILL, à 0,4 bpp,
caractéristiques SRM, 10000 images par classe. Classifieur multinomial (mise à l'échelle, PCA, régression
logistique), évalué en validation croisée. La matrice de confusion est construite sur des prédictions hors
échantillon. Deux k-means à ne pas confondre : celui de PFA regroupe les caractéristiques, celui du critère
S-SELECT regroupe les images, et c'est lui que l'on règle sur le nombre de classes, ici quatre.

## Résultats (SRM, natural, 0,4 bpp, 10000 images par classe)

Exactitude globale 0,581, F1 macro 0,572, pour un hasard à 0,25.

| Classe | Précision | Rappel | F1 |
|---|---|---|---|
| cover | 0,522 | 0,596 | 0,557 |
| lsb | 0,883 | 0,947 | 0,914 |
| uniward | 0,459 | 0,455 | 0,457 |
| hill | 0,409 | 0,324 | 0,361 |

La confusion se concentre entre cover, S-UNIWARD et HILL ; LSB est isolé. Matrice de confusion normalisée en
figure.

Critère non supervisé, k = 4 : silhouette 0,252, accord avec les vraies classes (ARI) -0,000.

Sélection supervisée, exactitude par nombre de caractéristiques (sous-échantillon, validation croisée) :

| Configuration | Nb caractéristiques | Exactitude |
|---|---|---|
| Toutes (PCA 300) | ~34000 | 0,544 |
| PFA + supervisé | 24 | 0,428 |
| PFA + supervisé | 50 | 0,379 |
| PFA + supervisé | 100 | 0,437 |

Figure : expD_srm_confusion_natural_p04.png.

## Lecture

L'attribution multi-classe fonctionne nettement au-dessus du hasard, et progresse avec les données : 0,581
d'exactitude à 10000, contre 0,52 à 5000. LSB est identifié presque parfaitement (F1 0,914), sa signature
grossière le trahit. Cover, S-UNIWARD et HILL se confondent, F1 de 0,56 à 0,36, HILL étant le plus difficile,
car les schémas adaptatifs sont conçus pour être minimaux, donc proches du cover et l'un de l'autre.

Le point central concerne l'extension de S-SELECT au multi-classe par le k. Le critère non supervisé à k = 4
échoue complètement, ARI de -0,000 : aucun accord avec les vraies classes. La raison est nette, les versions
stégo d'une image restent collées à leur cover, donc un regroupement géométrique retrouve les images, pas les
algorithmes. Régler le k ne suffit donc pas ; c'est la variante supervisée qui rend le multi-classe
abordable.

La sélection supervisée tient : de 34000 à quelques dizaines de caractéristiques, on garde de l'ordre de
0,43 contre 0,544 avec la totalité. La courbe n'est pas parfaitement monotone entre 24, 50 et 100, un léger
bruit de la sélection à ces tailles, mais l'ordre de grandeur montre une forte réduction pour une perte
modérée.

## Portée

Exploration honnête, à présenter comme telle. Elle montre que le cadre se généralise à l'attribution
d'algorithme, que LSB s'y détache franchement, et que distinguer finement les schémas adaptatifs demande
davantage de données ou des caractéristiques dédiées. Elle éclaire aussi une limite de la méthode de
l'encadrant en non supervisé, que la variante supervisée corrige.
