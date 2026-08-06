# Méthode : PFA et S-SELECT (réduction de caractéristiques)

Fiche de compréhension de l'algorithme de l'encadrant, pour la mise en oeuvre et la soutenance.
Source : F. K. Gomis, M. S. Camara, I. Diop, "Feature Reduction Algorithm for Universal Steganalysis",
EMENA-ISTL, 2019.

## But

En stéganalyse universelle, on extrait beaucoup de caractéristiques par image, ce qui est lourd et
empêche certains classifieurs de fonctionner. L'objectif est de réduire à un petit sous-ensemble de
caractéristiques d'origine, sans perdre le pouvoir de séparer cover et stégo.

## Idée centrale

La sélection est non supervisée, elle n'utilise pas les étiquettes. Le pari : les bonnes caractéristiques
sont celles qui, à elles seules, découpent les images en deux groupes bien nets. Comme les deux vrais
groupes sont cover et stégo, un découpage propre en deux revient à trouver les caractéristiques
discriminantes.

## Brique 1 : PFA (Principal Feature Analysis, Lu 2007)

PFA choisit, parmi toutes les caractéristiques, un nombre n de caractéristiques d'origine représentatives.
Principe :

1. Calculer la matrice de corrélation des caractéristiques.
2. En faire une analyse en composantes principales, garder les q premières composantes qui portent
   l'essentiel de la variance.
3. Représenter chaque caractéristique par son vecteur de coordonnées sur ces q composantes.
4. Regrouper ces vecteurs de caractéristiques en n groupes par k-means.
5. Dans chaque groupe, garder la caractéristique la plus proche du centre du groupe, son représentant.
6. Renvoyer ces n caractéristiques.

Effet : on enlève les redondances, on garde n caractéristiques variées et informatives.

## Brique 2 : le score de silhouette

Mesure la propreté d'un découpage en groupes. Valeur dans [-1, 1]. Proche de 1, groupes bien séparés,
proche de 0, groupes qui se chevauchent. Sert à évaluer un k-means à deux groupes.

## Algorithme S-SELECT

Entrée : le jeu de données sans les étiquettes, un nombre minimum m et un nombre maximum p de
caractéristiques.

```
Initialiser n = m
Initialiser L = plus basse valeur possible
Initialiser S = ensemble vide
Tant que n <= p :
    idx = PFA(donnees, n)                 # n caracteristiques
    labels = kmeans(donnees[:, idx], k=2) # deux groupes
    mesure = silhouette(donnees[:, idx], labels)
    si mesure > L :
        L = mesure
        S = idx
    n = n + 1
Renvoyer S
```

En clair : on essaie chaque taille de m à p, on garde celle qui donne la séparation en deux la plus
nette, et on renvoie le sous-ensemble correspondant. Ensuite on entraîne un classifieur supervisé sur S.

## Résultats de l'article

Base BOSSbase 1.01, images en JPEG, insertion LSB, 486 caractéristiques intra et inter blocs.
Réglages m = 10, p = 30. S-SELECT retient 15 caractéristiques. Un perceptron multicouche sur ces 15
atteint 0,99 de précision, autant qu'avec les 486, et autant que la sélection stepwise qui en gardait 51.
Conclusion : même performance, bien moins de caractéristiques, calcul allégé.

## Deux k-means, à ne pas confondre

- Dans PFA, le k-means regroupe les caractéristiques entre elles (n groupes de caractéristiques).
- Dans S-SELECT, le k-means regroupe les images en deux groupes, pour mesurer la silhouette.

## Point d'attention pour notre cas

Dans l'article, toutes les images viennent d'une seule base, donc le seul découpage en deux possible est
cover contre stégo. Nous mélangeons quatre sources. Le découpage dominant risque d'être naturel contre
généré plutôt que cover contre stégo. Il faudra donc appliquer S-SELECT à l'intérieur d'une seule source,
ou sur un couple cover et stégo d'une même source, pour qu'il sélectionne bien les caractéristiques qui
séparent l'insertion.

## Différences avec notre montage actuel

- Eux : caractéristiques JPEG intra et inter blocs, insertion LSB, classifieur perceptron multicouche.
- Nous : caractéristiques spatiales SPAM ou SRM, insertions LSB, S-UNIWARD, HILL, classifieur linéaire.
- La méthode de réduction est générale, elle s'applique quel que soit le jeu de caractéristiques.

## Ce qu'il faudra implémenter

1. Une fonction PFA(X, n) qui renvoie les indices de n caractéristiques.
2. Une fonction S-SELECT(X, m, p) qui balaie n de m à p et renvoie le meilleur sous-ensemble.
3. Le branchement de S-SELECT dans le détecteur, à la place de la PCA.
4. Une comparaison PFA contre PCA, pour la discussion du mémoire.
