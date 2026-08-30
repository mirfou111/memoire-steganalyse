# Expérience C : adaptation du détecteur (H3)

## Hypothèse

Adapter le détecteur restaure une part de la performance perdue à cause du décalage de domaine. La brique
« réentraînement » est déjà visible dans l'Expérience A, colonne AUC apparié ; cette expérience la met en
scène comme solution et en teste deux formes plus réalistes.

## Démarche

Une partition train et test fixe par source, identique pour toutes les stratégies, rend les AUC
comparables. Détecteur identique à l'Expérience A : mise à l'échelle, PCA à 300 composantes, régression
logistique. Quatre stratégies évaluées sur les sources générées, cas LSB à 0,4 bpp :

- naturel seul : détecteur entraîné sur le naturel, appliqué au généré, rappelle le problème ;
- mixte : un seul détecteur entraîné sur naturel et généré mélangés ;
- conscient de la source : un classifieur identifie d'abord la source, puis route vers le détecteur
  apparié correspondant ;
- apparié : détecteur entraîné et testé sur la même source, borne haute.

Un volet supplémentaire teste la généralisation à un générateur non vu : entraînement sur le naturel et
deux générateurs, évaluation sur le troisième.

## Résultats

Cas LSB à 0,4 bpp. AUC de test sur la source générée.

| Source | naturel seul | mixte | conscient | apparié | identification source |
|---|---|---|---|---|---|
| SD | 0,725 | 0,931 | 0,924 | 0,926 | 0,996 |
| SDXL | 0,936 | 0,996 | 0,993 | 0,994 | 0,999 |
| ADM | 0,933 | 0,990 | 0,983 | 0,985 | 0,996 |

Généralisation à un générateur non vu à l'entraînement :

| Source non vue | naturel seul | mixte sans cette source |
|---|---|---|
| SD | 0,725 | 0,864 |
| SDXL | 0,936 | 0,975 |
| ADM | 0,933 | 0,979 |

Figures : expC_srm_strategies_lsb_p04.png, expC_srm_loso_lsb_p04.png.

## Lecture

Le décalage de domaine est concentré sur Stable Diffusion, où le détecteur naturel seul tombe à 0,725.
Les deux formes d'adaptation le remontent à 0,93, soit pratiquement la borne apparié de 0,926 : la solution
récupère la quasi-totalité de ce que le décalage avait fait perdre. SDXL et ADM, moins affectés au départ,
montent à environ 0,99, également au niveau de leur borne apparié.

Le réentraînement mixte égale le détecteur apparié sur les trois sources. Un seul détecteur entraîné sur
naturel plus généré fait donc aussi bien que quatre détecteurs spécialisés, ce qui est la solution la plus
simple à déployer. La détection consciente de la source fait jeu égal ; son classifieur identifie l'origine
à plus de 99,6 %, ce qui confirme au passage l'ampleur du décalage, puisque la source est presque triviale
à reconnaître.

Le volet du générateur non vu montre que l'exposition au contenu généré, même d'autres modèles, aide face à
un générateur inconnu : SDXL et ADM atteignent presque leur borne apparié sans avoir été vus (0,975 et
0,979). Stable Diffusion gagne beaucoup en absolu, de 0,725 à 0,864, mais ne referme pas tout l'écart, ce
qui confirme qu'il reste le domaine le plus atypique.

## Portée et limites

La solution restaure ce que le décalage de domaine avait fait perdre (H1). Elle ne récupère pas ce que la
génération masque (interférence, H2) ni ce qui manque faute de données pour les algorithmes adaptatifs.
Elle répare le problème du domaine, pas la physique du signal. Le résultat porte ici sur LSB, le cas
détectable, qui est celui où le décalage de domaine est lisible.
