# Méthode : le détecteur de stéganalyse

Description du détecteur utilisé dans les expériences, pour la rédaction et la soutenance.

## Vue d'ensemble

Le détecteur reproduit la chaîne classique de la stéganalyse. Il se compose de deux briques
distinctes, et aucune n'est un réseau de neurones.

## Brique 1 : extraction de caractéristiques

- Descripteur principal : SRM (Spatial Rich Models), environ 34000 caractéristiques.
- Principe : de nombreux sous-modèles de résidus entre pixels voisins, quantifiés et seuillés, qui captent
  des dépendances fines et variées. Descripteur de stéganalyse classique, calculé à la main, pas appris.
- Rôle : transformer chaque image en un vecteur de nombres.

Étape antérieure : SPAM (Subtractive Pixel Adjacency Matrix, 686 dimensions, chaîne de Markov d'ordre 1).
SPAM détecte bien le LSB mais reste aveugle aux algorithmes adaptatifs, S-UNIWARD et HILL, dont la
référence tombe au niveau du hasard, car ils préservent justement les statistiques d'ordre faible que SPAM
modélise. On a donc mené SPAM en validation légère de la chaîne, puis basculé sur SRM pour traiter les
trois algorithmes sur un pied d'égalité. Le prix est un coût de calcul lourd, d'où l'extraction sur
serveur. Le grand nombre de dimensions de SRM est ramené à un sous-ensemble par réduction, PCA ou la
méthode PFA de l'encadrant.

## Brique 2 : classifieur

- Modèle : régression logistique, précédée d'une normalisation puis d'une réduction (PCA, ou PFA).
- Nature : modèle linéaire d'apprentissage automatique, simple et interprétable.
- Apprentissage : séparer les images vierges (étiquette 0) des images porteuses (étiquette 1).

La réduction n'est pas un détail : sans elle, les 34000 dimensions de SRM font sur-apprendre le modèle.
Dans la littérature, les caractéristiques riches sont souvent associées à un ensemble de FLD ; on a retenu
la régression logistique, plus simple et tout aussi défendable pour une démonstration.

## Évaluation

- Métrique principale : AUC (aire sous la courbe ROC).
- Protocole : validation croisée répétée (RepeatedStratifiedKFold), moyenne et écart type rapportés,
  pour montrer que le résultat ne dépend pas d'un découpage chanceux.
- Mesures dérivées : taux de faux positifs à seuil calibré, et comparaison entre détecteur naturel et
  détecteur apparié pour distinguer un problème de domaine d'un problème de détectabilité.

## Résumé pour la soutenance

Le détecteur est la chaîne classique de stéganalyse : caractéristiques riches SRM, réduction, puis
classifieur linéaire, sans deep learning. Ce choix privilégie la transparence, chaque étape étant
explicable. La réduction s'appuie sur la méthode PFA de l'encadrant, ce qui rend les caractéristiques
riches abordables.

## Pourquoi pas de deep learning pour la détection

Argumentaire, du plus fort au plus nuancé.

1. Fidélité à la problématique. Le travail vise à démontrer que la stéganalyse classique, calibrée sur
   des images naturelles, est perturbée par le contenu IA. Pour prouver que la stéganalyse classique
   échoue, il faut l'utiliser telle quelle. Un réseau profond changerait la nature de l'objet étudié.

2. Transparence. Le détecteur est entièrement explicable : on sait ce que mesure SPAM et ce que fait la
   régression logistique. Un réseau profond est une boîte noire. Pour un mémoire qui doit expliquer un
   phénomène, la transparence prime sur la performance brute.

3. Coût. Un stéganalyseur profond comme SRNet demande un GPU et de longs entraînements, ainsi que
   beaucoup plus de données, alors que le projet est déjà limité en données. La méthode PFA de l'encadrant
   va dans le sens inverse, réduire les ressources.

4. Argument scientifique. Le décalage de domaine touche aussi les réseaux profonds, peut-être davantage,
   car ils sur-apprennent les statistiques de leur domaine d'entraînement. Un détecteur simple et
   interprétable pose le problème plus clairement.

Limite assumée. Le deep learning, en particulier SRNet, reste l'état de l'art de la performance en
stéganalyse. On ne prétend pas le contraire. On le pose en perspective : une extension naturelle serait
de tester si un détecteur profond résiste mieux au décalage de domaine.

Formule courte. Le deep learning est l'état de l'art de la performance, mais mon objectif est de
démontrer et d'expliquer un phénomène sur la stéganalyse classique, avec transparence et sans ressources
lourdes, ce qui est plus fidèle à ma problématique et plus honnête sur les moyens. Le point est soumis à
l'encadrant, pour décider s'il faut ajouter un volet neuronal ou le poser en perspective.
