# Évaluation de PFA et S-SELECT sur nos données

Premiers tests de la réduction de caractéristiques sur le cas naturel, insertion LSB à 0,4 bpp,
caractéristiques SPAM. Le détecteur est une régression logistique, l'AUC est mesurée par validation
croisée répétée.

## Résultats

| Configuration | Nb caractéristiques | AUC |
|---|---|---|
| Toutes les caractéristiques | 686 | 0,933 |
| S-SELECT (critère silhouette) | 10 | 0,738 |
| PFA seul | 15 | 0,910 |
| PFA seul | 50 | 0,873 |
| PFA seul | 100 | 0,897 |
| PFA seul | 200 | 0,907 |
| PFA seul | 300 | 0,903 |

## Lecture

Deux constats nets se dégagent.

PFA fonctionne bien comme réducteur. Même à 15 caractéristiques, l'AUC reste à 0,910, tout près des 0,933
obtenus avec les 686 caractéristiques. La brique centrale de la méthode de l'encadrant se généralise donc
à notre montage : on garde l'essentiel du pouvoir de détection avec très peu de caractéristiques.

Le critère de sélection de S-SELECT, en revanche, échoue ici. En choisissant les caractéristiques qui
séparent le plus proprement les images en deux groupes, sans étiquettes, il sélectionne des
caractéristiques liées au contenu des images, pas à l'insertion. L'AUC tombe alors à 0,738. La cause est
que la trace de l'insertion est minuscule face à la variabilité de contenu entre images.

## Portée et limite

Ce résultat délimite les conditions d'application de la méthode. L'hypothèse de S-SELECT, selon laquelle
le meilleur découpage non supervisé en deux groupes correspond à cover contre stégo, tient dans le cadre
de l'article d'origine mais pas dans le nôtre, où le contenu domine. Cela reste vrai même à l'intérieur
d'une seule source : le problème ne vient pas du mélange de sources, mais du fait que le contenu écrase le
signal d'insertion.

Ce n'est pas un échec de la méthode, mais une observation critique utile : elle valide PFA comme réducteur
et identifie précisément la limite du critère non supervisé.

## Piste : une variante supervisée

Puisque les étiquettes cover et stégo sont disponibles, on peut garder PFA pour enlever les redondances,
mais remplacer le critère silhouette par un critère supervisé, l'AUC en validation croisée. On choisit
alors la taille et les caractéristiques qui séparent réellement cover et stégo. Cette variante, à évaluer
ci-après, serait une extension personnelle du travail de l'encadrant.
