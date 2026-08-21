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
Courbes ROC pour LSB. Ce qu'elle montre : [reference vs cross-domaine, ampleur de la chute par source].

### expA_srm_aucbars_lsb_p04.png
Barres d'AUC pour LSB, référence, cross-domaine et apparié par source. Ce qu'elle montre : [effondrement
cross-domaine et récupération par le détecteur apparié].

### expA_srm_fprcdf_lsb_p04.png
Distribution cumulée des scores sur images vierges, LSB. Ce qu'elle montre : [quelle source décroche au
seuil, taux de faux positifs lu à la ligne du seuil].

### expA_srm_roc_uniward_p04.png
Courbes ROC pour S-UNIWARD. Ce qu'elle montre : [detectabilite de l'adaptatif avec SRM, niveau atteint].

### expA_srm_aucbars_uniward_p04.png
Barres d'AUC pour S-UNIWARD. Ce qu'elle montre : [référence, cross, apparié].

### expA_srm_fprcdf_uniward_p04.png
Scores sur images vierges, S-UNIWARD. Ce qu'elle montre : [faux positifs par source].

### expA_srm_roc_hill_p04.png
Courbes ROC pour HILL. Ce qu'elle montre : [detectabilite, niveau].

### expA_srm_aucbars_hill_p04.png
Barres d'AUC pour HILL. Ce qu'elle montre : [référence, cross, apparié].

### expA_srm_fprcdf_hill_p04.png
Scores sur images vierges, HILL. Ce qu'elle montre : [faux positifs par source].

## Expérience B, interférence (SRM)

### expB_srm_maha_lsb_p04.png
Distances cover vers stégo par source, LSB. Ce qu'elle montre : [quelle source masque le plus l'insertion,
comparaison au niveau naturel].

### expB_srm_proj2d_lsb_p04.png
Projection 2D des classes, LSB. Ce qu'elle montre : [séparation cover et stégo par source, chevauchement].

### expB_srm_maha_uniward_p04.png
Distances cover vers stégo par source, S-UNIWARD. Ce qu'elle montre : [interférence sur l'adaptatif, enfin
mesurable avec SRM].

### expB_srm_proj2d_uniward_p04.png
Projection 2D des classes, S-UNIWARD. Ce qu'elle montre : [chevauchement des paires par source].

### expB_srm_maha_hill_p04.png
Distances cover vers stégo par source, HILL. Ce qu'elle montre : [interférence sur l'adaptatif].

### expB_srm_proj2d_hill_p04.png
Projection 2D des classes, HILL. Ce qu'elle montre : [chevauchement des paires par source].

## Synthèse transversale

À compléter une fois toutes les figures obtenues : la conclusion d'ensemble, notamment si Stable Diffusion
reste la source la plus affectée à travers tous les algorithmes et sur les deux axes, décalage de domaine
et interférence.
