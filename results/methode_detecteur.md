# Méthode : le détecteur de stéganalyse

Description du détecteur utilisé dans les expériences, pour la rédaction et la soutenance.

## Vue d'ensemble

Le détecteur reproduit la chaîne classique de la stéganalyse. Il se compose de deux briques
distinctes, et aucune n'est un réseau de neurones.

## Brique 1 : extraction de caractéristiques

- Descripteur : SPAM (Subtractive Pixel Adjacency Matrix).
- Dimension : 686 caractéristiques.
- Principe : modélise les différences entre pixels voisins par une chaîne de Markov d'ordre 1,
  seuillée. C'est un descripteur de stéganalyse classique, calculé à la main, pas appris.
- Rôle : transformer chaque image en un vecteur de nombres.

Variante prévue pour la suite : SRM (Spatial Rich Models, environ 34000 dimensions), plus riche mais
beaucoup plus lourd. SRM sera nécessaire pour les algorithmes adaptatifs (S-UNIWARD, HILL), que SPAM ne
détecte pas. La réduction du grand nombre de caractéristiques SRM se fera par la méthode PFA de
l'encadrant.

## Brique 2 : classifieur

- Modèle : régression logistique, précédée d'une normalisation (StandardScaler).
- Nature : modèle linéaire d'apprentissage automatique, simple et interprétable.
- Apprentissage : séparer les images vierges (étiquette 0) des images porteuses (étiquette 1).

Dans la littérature, les caractéristiques riches sont souvent associées à un ensemble de FLD. Ici on a
retenu la régression logistique, plus simple et tout aussi défendable pour une démonstration.

## Évaluation

- Métrique principale : AUC (aire sous la courbe ROC).
- Protocole : validation croisée répétée (RepeatedStratifiedKFold), moyenne et écart type rapportés,
  pour montrer que le résultat ne dépend pas d'un découpage chanceux.
- Mesures dérivées : taux de faux positifs à seuil calibré, et comparaison entre détecteur naturel et
  détecteur apparié pour distinguer un problème de domaine d'un problème de détectabilité.

## Résumé pour la soutenance

Le détecteur est la chaîne classique de stéganalyse : caractéristiques SPAM plus classifieur linéaire,
sans deep learning et sans GPU. Ce choix privilégie la transparence, chaque étape étant explicable. Il
évoluera vers SRM et la réduction PFA pour traiter les algorithmes adaptatifs.

## Pourquoi pas de deep learning pour la détection

Argumentaire, du plus fort au plus nuancé.

1. Fidélité à la problématique. Le travail vise à démontrer que la stéganalyse classique, calibrée sur
   des images naturelles, est perturbée par le contenu IA. Pour prouver que la stéganalyse classique
   échoue, il faut l'utiliser telle quelle. Un réseau profond changerait la nature de l'objet étudié.

2. Transparence. Le détecteur est entièrement explicable : on sait ce que mesure SPAM et ce que fait la
   régression logistique. Un réseau profond est une boîte noire. Pour un mémoire qui doit expliquer un
   phénomène, la transparence prime sur la performance brute.

3. Coût. Un stéganalyseur profond comme SRNet demande un GPU et de longs entraînements. Le projet a
   justement une contrainte de calcul, celle qui a fait passer à SPAM. Le deep learning irait à contre
   courant, et la méthode PFA de l'encadrant va dans le sens inverse, réduire les ressources.

4. Argument scientifique. Le décalage de domaine touche aussi les réseaux profonds, peut-être davantage,
   car ils sur-apprennent les statistiques de leur domaine d'entraînement. Un détecteur simple et
   interprétable pose le problème plus clairement.

Limite assumée. Le deep learning, en particulier SRNet, reste l'état de l'art de la performance en
stéganalyse. On ne prétend pas le contraire. On le pose en perspective : une extension naturelle serait
de tester si un détecteur profond résiste mieux au décalage de domaine.

Formule courte. Le deep learning est l'état de l'art de la performance, mais mon objectif est de
démontrer et d'expliquer un phénomène sur la stéganalyse classique, avec transparence et sans ressources
lourdes, ce qui est plus fidèle à ma problématique et plus honnête sur les moyens.
