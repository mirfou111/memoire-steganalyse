% Cas pratique : stéganalyse face aux images générées — état des résultats
% Ousmane Ndiéguène
% Août 2026

## Objet

Ce document rend compte du cas pratique conçu pour démontrer, sur des mesures reproductibles, les deux
difficultés que pose l'image générée par intelligence artificielle à la stéganalyse classique : le
décalage de domaine et l'interférence des artefacts de génération. Il présente le dispositif, la démarche
et les résultats des deux expériences, ainsi que le travail de réduction de caractéristiques.

## 1. Dispositif expérimental

Le corpus réunit quatre sources d'images, traitées exactement de la même façon pour que seules leurs
différences d'origine entrent en jeu :

- naturel : BOSSbase, référence historique de la stéganalyse ;
- Stable Diffusion : issu de DiffusionDB ;
- SDXL : modèle de diffusion latente plus récent ;
- ADM : modèle de diffusion dans l'espace des pixels, issu de GenImage.

Chaque image est convertie en niveaux de gris, recadrée au centre en 256x256 et enregistrée sans perte.
Sur chaque image vierge (cover), trois algorithmes d'insertion sont simulés avec la bibliothèque conseal :
LSB, insertion naïve, et deux algorithmes adaptatifs, S-UNIWARD et HILL, qui dissimulent le message dans
les zones difficiles à modéliser. Deux charges utiles sont testées, 0,2 et 0,4 bpp. On dispose ainsi, pour
chaque source, des images vierges et de leurs versions porteuses (stego) pour chaque algorithme.

La détection repose sur les caractéristiques SRM, un descripteur riche d'environ 34000 dimensions qui
capte les corrélations fines entre pixels voisins, seul capable de réagir aux algorithmes adaptatifs. Le
classifieur est une régression logistique précédée d'une réduction de dimension, la performance étant
mesurée en aire sous la courbe ROC (AUC) par validation croisée. L'extraction SRM, coûteuse, a été menée
sur un serveur 16 cœurs ; le reste tient sur Colab.

Volume retenu : 1500 images par source, et une extension du naturel à 5000 pour pousser la détection des
algorithmes adaptatifs.

## 2. Expérience A : décalage de domaine

Question. Un détecteur entraîné sur des images naturelles reste-t-il fiable face à des images générées ?

Démarche. Le détecteur est entraîné uniquement sur le naturel, puis appliqué tel quel aux trois sources
générées (cross-domaine). On le compare à un détecteur réentraîné sur chaque source (apparié). On mesure
en plus le taux de faux positifs, c'est-à-dire la proportion d'images vierges classées à tort comme
porteuses, au seuil calibré pour 5 % de faux positifs sur le naturel.

Résultats, cas LSB à 0,4 bpp.

| Source | AUC cross-domaine | AUC apparié | Faux positifs |
|---|---|---|---|
| naturel (référence) | 0,99 | - | 0,05 |
| Stable Diffusion | 0,77 | 0,93 | 0,83 |
| SDXL | 0,95 | 0,99 | 0,20 |
| ADM | 0,96 | 0,98 | 0,36 |

Lecture. Le détecteur naturel s'effondre sur Stable Diffusion : il y déclare porteuses 83 % des images
pourtant vierges. Réentraîné sur cette même source, il remonte à 0,93 d'AUC. La panne ne vient donc pas de
la méthode mais du changement de domaine statistique entre le naturel et le généré. SDXL et ADM subissent
un décalage plus modéré. Le phénomène se retrouve, plus marqué encore, à 0,2 bpp.

## 3. Expérience B : interférence des artefacts

Question. Sur une image générée, la trace de l'insertion est-elle masquée par le bruit propre à la
génération ?

Démarche. On mesure directement, sans détecteur entraîné, l'ampleur du déplacement entre les images
vierges et leurs versions porteuses, par une distance multivariée (Mahalanobis) sur les caractéristiques
réduites. La même réduction est appliquée à toutes les sources pour que la comparaison reste valable. Une
distance plus faible que sur le naturel signale une insertion plus difficile à voir, donc une
interférence.

Résultats à 0,4 bpp.

| Algorithme | naturel | Stable Diffusion | SDXL | ADM |
|---|---|---|---|---|
| LSB | 1,56 | 1,31 | 1,76 | 1,65 |
| S-UNIWARD | 0,74 | 0,55 | 1,05 | 1,10 |
| HILL | 0,58 | 0,50 | 0,84 | 0,90 |

Lecture. Sur Stable Diffusion, la distance passe sous le niveau naturel pour les trois algorithmes :
l'insertion y est effectivement masquée. Sur SDXL et ADM, elle reste au-dessus du naturel, l'insertion y
ressort même davantage. Le résultat est stable que la réduction garde 100 ou 200 composantes. On note que
la distance des algorithmes adaptatifs est faible partout, ce qui reflète leur discrétion intrinsèque.

## 4. Réduction de caractéristiques

Les 34000 dimensions de SRM rendent les modèles lourds et sujets au surapprentissage. La méthode de
réduction de l'encadrant, PFA et son enveloppe de sélection S-SELECT, a été implémentée et évaluée. Sur
SRM en cas LSB, elle ramène les caractéristiques à quelques dizaines en conservant l'essentiel de la
performance (AUC 0,91 avec 24 caractéristiques, contre 0,93 avec la totalité).

Le critère de sélection non supervisé de S-SELECT, fondé sur la séparation des groupes, a montré une
limite dans notre montage : le contenu des images domine la trace de l'insertion, ce qui brouille ce
critère. Une variante supervisée, guidée par la performance de détection, corrige ce point et constitue
une contribution propre.

## 5. Expérience C : adaptation du détecteur

Question. Peut-on restaurer la performance perdue à cause du décalage de domaine ?

Démarche. Sur une même partition de test, on compare le détecteur naturel seul à trois formes d'adaptation :
un détecteur réentraîné sur naturel et généré mélangés (mixte), un détecteur qui identifie d'abord la
source puis route vers le modèle adapté (conscient de la source), et le détecteur apparié qui donne la
borne haute. Cas LSB à 0,4 bpp.

| Source | naturel seul | mixte | conscient | apparié |
|---|---|---|---|---|
| Stable Diffusion | 0,73 | 0,93 | 0,92 | 0,93 |
| SDXL | 0,94 | 1,00 | 0,99 | 0,99 |
| ADM | 0,93 | 0,99 | 0,98 | 0,99 |

Lecture. L'adaptation récupère la quasi-totalité de la performance perdue : Stable Diffusion remonte de
0,73 à 0,93, au niveau de la borne apparié. Le réentraînement mixte, un seul détecteur pour toutes les
sources, égale les détecteurs spécialisés. Un test complémentaire montre qu'un détecteur exposé à d'autres
générateurs se défend déjà mieux face à un générateur jamais vu. La solution répare le décalage de domaine ;
elle ne récupère ni ce que l'interférence masque, ni ce qui manque faute de données pour l'adaptatif.

## 6. Cas difficile : les algorithmes adaptatifs

S-UNIWARD et HILL restent le point dur. Avec 1500 images la détection est faible (AUC autour de 0,60), et
elle progresse lentement en élargissant le naturel à 5000 (autour de 0,67 à 0,70). Les tests sur le
classifieur montrent que ce n'est pas lui le frein mais le volume de données : la littérature situe le bon
régime autour de 10000 images, hors de portée pour SDXL et ADM dont les jeux sources sont plafonnés. Ce
point est donc rapporté honnêtement comme une limite de données.

## 7. Ce que l'ensemble établit

Les deux axes convergent vers un même constat. Parmi les trois générateurs, Stable Diffusion est le seul
qui perturbe la stéganalyse classique sur les deux plans à la fois : il trompe le détecteur (faux positifs
massifs) et masque l'insertion. SDXL et ADM ne présentent qu'un décalage de domaine modéré, sans masquage.
L'adaptation du détecteur (Expérience C) répare ce que le décalage de domaine avait fait perdre, en
ramenant Stable Diffusion au niveau de la borne haute. La réduction de caractéristiques rend par ailleurs
les descripteurs riches abordables.

## 8. Portée et limites

Les trois résultats n'ont pas la même portée, et il faut éviter de les résumer par un simple « LSB et SD ».
Chaque axe a sa propre restriction, et elles ne tombent pas sur les mêmes expériences.

| Résultat | Selon l'algorithme d'insertion | Selon le générateur |
|---|---|---|
| A, décalage de domaine | net sur LSB, adaptatif limité par les données | les trois, Stable Diffusion extrême |
| B, interférence | les trois algorithmes | Stable Diffusion spécifiquement |
| C, solution | LSB, adaptatif non traité | les trois générateurs |

Sur l'axe de l'algorithme, le décalage de domaine et la solution se lisent nettement sur LSB. Ce n'est pas
que le phénomène serait propre à LSB : pour les algorithmes adaptatifs, la détection de base est déjà trop
faible, faute de données, pour qu'on mesure proprement une chute puis une récupération. C'est une limite de
données, pas de principe. L'interférence, elle, a été mesurée sur les trois algorithmes, y compris les
adaptatifs, car sa mesure ne dépend pas d'un détecteur entraîné.

Sur l'axe du générateur, c'est l'inverse. Le décalage de domaine et la solution valent pour les trois
générateurs : Stable Diffusion est le cas extrême, mais SDXL et ADM montrent aussi le décalage et sont tout
aussi bien réparés par l'adaptation. Seule l'interférence est spécifique à Stable Diffusion, seul générateur
à masquer l'insertion.

Deux réserves à garder honnêtement : la faiblesse sur l'adaptatif est un plafond de données, que la
littérature situe autour de 10000 images ; et la spécificité de Stable Diffusion pourrait tenir en partie
aux propriétés de DiffusionDB plutôt qu'au seul générateur, ce qu'une seconde source SD permettrait de
trancher.
