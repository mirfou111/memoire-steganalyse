# Expérience A : décalage de domaine

## Objectif

Tester l'hypothèse H1 : un détecteur de stéganalyse entraîné sur des images naturelles perd sa fiabilité
sur des images générées. On mesure trois choses : une AUC de référence sur le naturel, l'AUC en
cross-domaine du détecteur naturel appliqué aux sources générées, et l'AUC appariée d'un détecteur
réentraîné sur chaque source. On y ajoute le taux de faux positifs, la proportion d'images vierges classées
à tort comme porteuses.

## Protocole

Caractéristiques SRM (environ 34000 dimensions), détecteur linéaire précédé d'une réduction (normalisation,
PCA, régression logistique), validation croisée répétée. Insertion LSB à 0,4 bpp. Trois sources générées
comparées au naturel : Stable Diffusion, SDXL, ADM. Le seuil de décision est calibré à 5 % de fausses
alarmes sur le naturel.

Une première campagne sur caractéristiques SPAM (686 dimensions) avait déjà révélé le phénomène sur LSB,
avec la même hiérarchie entre sources. Le passage à SRM permet de le confirmer avec un descripteur riche et
d'ouvrir la voie aux algorithmes adaptatifs, que SPAM ne détecte pas.

## Résultats (SRM, LSB, 0,4 bpp)

Référence naturel : AUC environ 0,99.

| Source | AUC cross-domaine | AUC appariée | Faux positifs |
|---|---|---|---|
| naturel (référence) | 0,99 | - | 0,05 |
| Stable Diffusion | 0,77 | 0,93 | 0,83 |
| SDXL | 0,95 | 0,99 | 0,20 |
| ADM | 0,96 | 0,98 | 0,36 |

Figures : `expA_srm_roc_lsb_p04.png`, `expA_srm_aucbars_lsb_p04.png`, `expA_srm_fprcdf_lsb_p04.png`.

La figure des faux positifs mérite une mention particulière. Elle trace la distribution cumulée des scores
du détecteur naturel appliqué aux images vierges de chaque source, avec le seuil calibré à 5 % sur le
naturel. Au seuil, naturel, SDXL et ADM restent bas, peu d'images au-dessus. Stable Diffusion décroche
seul : 83 % de ses images vierges passent au-dessus du seuil et sont déclarées porteuses. La figure isole
ainsi visuellement Stable Diffusion comme la seule source qui trompe massivement le détecteur.

## Interprétation

Le décalage de domaine est confirmé, et il est hétérogène. Le signal le plus fort est le taux de faux
positifs sur Stable Diffusion : un détecteur calibré pour 5 % de fausses alarmes sur le naturel en produit
83 % sur des images générées vierges. En conditions réelles, il signalerait massivement des images
innocentes.

Les détecteurs appariés, réentraînés sur chaque source générée, restent performants, de 0,93 à 0,99. Cela
prouve que l'information de détection est présente et que la perte vient du changement de domaine, non d'une
impossibilité. C'est le point qui motive la partie solution (Expérience C).

La hiérarchie entre sources est stable : Stable Diffusion montre le décalage le plus marqué, ADM un
décalage modéré, SDXL le plus faible. Elle est identique à celle observée sur SPAM, ce qui renforce la
robustesse du constat.

## Limites et points à vérifier

La hiérarchie ne suit pas la distance architecturale attendue. On aurait pu croire le décalage maximal sur
ADM, architecturalement le plus éloigné, or c'est Stable Diffusion qui montre l'effet le plus fort. Une
explication possible : les images Stable Diffusion utilisées, issues de DiffusionDB, portent des
statistiques de bas niveau particulières qui trompent le détecteur, plus que l'architecture. Il faudra le
vérifier avec une autre source Stable Diffusion, pour distinguer l'effet du générateur de celui de la base.

Le cas LSB ne couvre que l'insertion naïve. La détection des algorithmes adaptatifs avec SRM plafonne
faute de données (autour de 0,60 à 0,70 d'AUC de référence, contre le régime de la littérature vers 10000
images), ce qui empêche d'y mesurer proprement un décalage puis une récupération. C'est une limite de
données, pas de principe.
