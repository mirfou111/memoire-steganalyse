# Interprétations des figures

Ce fichier recense chaque figure produite par les notebooks, référencée par son nom exact. On y note
l'interprétation au fur et à mesure que les figures sont générées. Les valeurs entre crochets sont à
remplir avec les chiffres réels.

## Nomenclature

Les figures suivent le schéma `<exp>_<feat>_<type>_<algo>_p<charge>.png`.

- exp : expA (décalage de domaine) ou expB (interférence)
- feat : srm (ou spam)
- type : roc, aucbars, fprcdf, maha, proj2d
- algo : lsb, uniward, hill
- charge : 04 pour 0,4 bpp, 02 pour 0,2 bpp

Les figures sont produites dans le dossier figures de Drive, puis copiées dans results du dépôt.

## Expérience A, décalage de domaine (SRM)

### expA_srm_roc_lsb_p04.png
Courbes ROC pour LSB. Ce qu'elle montre : la courbe de référence est presque parfaite (AUC 0,99) ; en
cross-domaine, la courbe Stable Diffusion s'effondre nettement (0,77) tandis que SDXL et ADM restent hautes
(0,95 et 0,96).

### expA_srm_aucbars_lsb_p04.png
Barres d'AUC pour LSB, référence, cross-domaine et apparié par source. Ce qu'elle montre : l'écart entre la
barre cross-domaine et la barre apparié mesure la perte due au domaine ; il est fort sur SD (0,77 vers 0,93)
et faible sur SDXL et ADM, qui reviennent près de 0,99.

### expA_srm_fprcdf_lsb_p04.png
Distribution cumulée des scores sur images vierges, LSB. Ce qu'elle montre : au seuil calibré à 5 % sur le
naturel, SD décroche seul, 83 % de ses images vierges passent au-dessus du seuil et sont classées porteuses,
contre 20 % pour SDXL et 36 % pour ADM.

### expA_srm_roc_uniward_p04.png
Courbes ROC pour S-UNIWARD. Ce qu'elle montre : le cas difficile ; même la référence reste modeste (autour
de 0,60 à 0,70), la détection de l'adaptatif étant limitée par le volume de données.

### expA_srm_aucbars_uniward_p04.png
Barres d'AUC pour S-UNIWARD. Ce qu'elle montre : des niveaux bas et proches sur toutes les conditions, signe
que la détection plafonne faute de données plutôt qu'à cause du domaine.

### expA_srm_fprcdf_uniward_p04.png
Scores sur images vierges, S-UNIWARD. Ce qu'elle montre : des distributions peu séparées, cohérentes avec la
faible détectabilité de l'adaptatif à cette échelle.

### expA_srm_roc_hill_p04.png
Courbes ROC pour HILL. Ce qu'elle montre : même profil que S-UNIWARD, détectabilité faible, cas difficile
limité par les données.

### expA_srm_aucbars_hill_p04.png
Barres d'AUC pour HILL. Ce qu'elle montre : niveaux bas et proches, conclusion identique au cas S-UNIWARD.

### expA_srm_fprcdf_hill_p04.png
Scores sur images vierges, HILL. Ce qu'elle montre : distributions peu séparées, faible détectabilité.

## Expérience B, interférence (SRM)

### expB_srm_maha_lsb_p04.png
Distances cover vers stégo par source, LSB. Ce qu'elle montre : SD est sous le niveau naturel (1,31 contre
1,56), donc masque l'insertion ; SDXL et ADM sont au-dessus (1,76 et 1,65), pas de masquage.

### expB_srm_proj2d_lsb_p04.png
Projection 2D des classes, LSB. Illustrative seulement : les deux axes captent le contenu et la source, pas
l'insertion, d'où un fort chevauchement attendu qui n'infirme pas la mesure de distance.

### expB_srm_maha_uniward_p04.png
Distances cover vers stégo par source, S-UNIWARD. Ce qu'elle montre : SD masque l'insertion (0,55 contre
0,74 pour le naturel) ; SDXL et ADM sont nettement au-dessus (1,05 et 1,10). Interférence mesurable sur
l'adaptatif grâce à SRM.

### expB_srm_proj2d_uniward_p04.png
Projection 2D des classes, S-UNIWARD. Illustrative seulement, même réserve que pour LSB : le chevauchement
est attendu, la preuve tient à la distance multivariée.

### expB_srm_maha_hill_p04.png
Distances cover vers stégo par source, HILL. Ce qu'elle montre : SD légèrement sous le naturel (0,50 contre
0,58), masquage marginal ; SDXL et ADM au-dessus (0,84 et 0,90).

### expB_srm_proj2d_hill_p04.png
Projection 2D des classes, HILL. Illustrative seulement, mêmes réserves : classes visuellement enchevêtrées,
cohérent avec un effet subtil.

## Expérience C, adaptation du détecteur (SRM)

### expC_srm_strategies_lsb_p04.png
Quatre stratégies comparées par source générée, LSB. Ce qu'elle montre : le détecteur naturel seul est bas
sur SD (0,725), les stratégies adaptées (mixte 0,931, conscient 0,924) le remontent au niveau de la borne
apparié (0,926) ; sur SDXL et ADM l'adaptation porte les AUC à environ 0,99, également à la borne apparié.
Le réentraînement mixte égale le détecteur apparié partout, donc un détecteur unique suffit.

### expC_srm_loso_lsb_p04.png
Généralisation à un générateur non vu, LSB. Ce qu'elle montre : entraîner sur naturel plus deux générateurs
et tester sur le troisième relève l'AUC par rapport au détecteur naturel seul. SDXL et ADM atteignent
presque leur borne apparié sans avoir été vus (0,975 et 0,979) ; SD gagne fortement (0,725 vers 0,864) sans
refermer tout l'écart, restant le domaine le plus atypique.

## Synthèse transversale

Les figures convergent. Sur les deux axes, décalage de domaine (A) et interférence (B), Stable Diffusion
est la source la plus affectée, seule à cumuler les deux problèmes, tandis que SDXL et ADM se comportent
comme des images naturelles. Les figures de l'Expérience C montrent que l'adaptation du détecteur ramène
Stable Diffusion au niveau de la borne apparié. Les cas adaptatifs (S-UNIWARD, HILL) restent le point
difficile, limité par le volume de données.
