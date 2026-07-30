# Expérience A : décalage de domaine

## Objectif

Tester l'hypothèse H1 : un détecteur de stéganalyse entraîné sur des images naturelles perd sa
fiabilité sur des images générées. On mesure trois choses : une AUC de référence sur le naturel,
le taux de faux positifs quand ce détecteur est appliqué à des images générées vierges, et l'AUC
en cross domaine comparée à un détecteur réentraîné sur du généré.

## Protocole

Caractéristiques SPAM (686 dimensions), détecteur linéaire (normalisation puis régression logistique),
validation croisée répétée. Insertion LSB matching aux charges 0,2 et 0,4 bit par pixel. Trois sources
générées comparées au naturel : Stable Diffusion, SDXL, ADM.

Note importante : SPAM ne détecte pas les algorithmes adaptatifs S-UNIWARD et HILL, dont la référence
reste au niveau du hasard. Ces algorithmes seront traités avec les caractéristiques riches SRM. La présente
section porte donc sur le cas LSB, qui suffit à démontrer le phénomène.

## Résultats

### Charge 0,4 bpp

Référence naturel : AUC = 0,981 +/- 0,004

| Source | AUC cross | AUC appariée | FPR covers |
|---|---|---|---|
| sd | 0,855 | 0,914 +/- 0,009 | 0,400 |
| sdxl | 0,958 | 0,988 +/- 0,002 | 0,079 |
| adm | 0,964 | 0,989 +/- 0,002 | 0,127 |

### Charge 0,2 bpp

Référence naturel : AUC = 0,868 +/- 0,012

| Source | AUC cross | AUC appariée | FPR covers |
|---|---|---|---|
| sd | 0,623 | 0,756 +/- 0,018 | 0,499 |
| sdxl | 0,809 | 0,932 +/- 0,007 | 0,149 |
| adm | 0,827 | 0,956 +/- 0,004 | 0,162 |

Rappel : le taux de faux positifs visé sur le naturel est de 0,05.

Figures : `expA_lsb_p0.4.png`, `expA_lsb_p0.2.png`.

## Interprétation

Le décalage de domaine est confirmé, mais il est hétérogène. Le signal le plus fort est le taux de
faux positifs sur Stable Diffusion : un détecteur calibré pour 5 pour cent de fausses alarmes sur le
naturel en produit 40 pour cent à 0,4 bpp, et 50 pour cent à 0,2 bpp, sur des images générées vierges.
En conditions réelles, ce détecteur signalerait donc massivement des images innocentes.

Le décalage s'accentue à faible charge. Quand l'insertion est plus discrète, l'écart entre la référence
et le cross domaine se creuse et les faux positifs augmentent. Le problème est donc pire dans le régime
difficile, qui est aussi le plus réaliste.

La hiérarchie entre sources est stable sur les deux charges : Stable Diffusion montre le décalage le plus
marqué, ADM un décalage modéré, SDXL le plus faible.

Enfin, les détecteurs appariés, réentraînés sur chaque source générée, restent performants, de 0,76 à
0,99. Cela prouve que l'information de détection est présente et que la perte vient du changement de
domaine, non d'une impossibilité. C'est le point qui motive la partie solution.

## Limites et points à vérifier

La hiérarchie observée ne suit pas la distance architecturale attendue. On aurait pu penser que le
décalage serait maximal sur ADM, architecturalement le plus éloigné, or c'est Stable Diffusion qui montre
l'effet le plus fort. Une explication possible est que les images Stable Diffusion utilisées, issues de
DiffusionDB, portent des statistiques de bas niveau particulières qui trompent le détecteur, plus que
l'architecture elle-même. Il faudra vérifier si cet effet tient avec une autre source d'images Stable
Diffusion, pour distinguer l'effet du générateur de celui du pipeline de la base.

Le cas LSB ne couvre que l'insertion naïve. La généralisation aux algorithmes adaptatifs demande les
caractéristiques SRM, prévue dans la suite.
