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

## Expérience B, interférence (SRM, 10000 images par source)

Note : la projection 2D a été écartée, non pertinente. Seules les figures de distance sont retenues.

### expB_srm_maha_lsb_p04.png
Distances cover vers stégo par source, LSB. Ce qu'elle montre : SD est sous le niveau naturel (1,33 contre
1,63), donc masque l'insertion ; Midjourney est au-dessus (1,75) et ADM proche du naturel (1,54), pas de
masquage.

### expB_srm_maha_uniward_p04.png
Distances cover vers stégo par source, S-UNIWARD. Ce qu'elle montre : SD masque fortement (0,53 contre 0,91
pour le naturel, 41 % de moins) ; Midjourney nettement au-dessus (1,30), ADM au niveau du naturel (0,97).
Interférence marquée sur l'adaptatif.

### expB_srm_maha_hill_p04.png
Distances cover vers stégo par source, HILL. Ce qu'elle montre : SD masque fortement (0,46 contre 0,77,
40 % de moins) ; Midjourney au-dessus (1,17), ADM au niveau du naturel (0,75).

## Expérience C, adaptation du détecteur (SRM)

### expC_srm_strategies_lsb_p04.png
Quatre stratégies comparées par source générée, LSB, 10000 images (5000 par source). Ce qu'elle montre : le
détecteur naturel seul est bas sur SD (0,733), les stratégies adaptées le remontent au niveau de la borne
apparié (mixte 0,948, conscient 0,952, apparié 0,953) ; Midjourney et ADM montent à 0,99 et 0,96. Le mixte
égale l'apparié partout, un détecteur unique suffit.

### expC_srm_strategies_uniward_p04.png
Quatre stratégies, S-UNIWARD. Ce qu'elle montre : l'adaptation récupère l'adaptatif sur Midjourney (0,609
vers 0,878) et ADM (0,645 vers 0,742), jusqu'à la borne apparié ; mais sur Stable Diffusion elle bute, même
l'apparié reste au hasard (0,557). Illustration de la limite de la solution face à l'interférence.

### expC_srm_strategies_hill_p04.png
Quatre stratégies, HILL. Même lecture que S-UNIWARD, en plus marqué : Midjourney 0,555 vers 0,820, ADM 0,576
vers 0,639, mais Stable Diffusion reste au hasard, apparié 0,523.

### expC_srm_loso_lsb_p04.png
Généralisation à un générateur non vu, LSB. Ce qu'elle montre : entraîner sur naturel plus deux générateurs
et tester sur le troisième relève l'AUC par rapport au détecteur naturel seul. SD 0,733 vers 0,924,
Midjourney vers 0,980, ADM vers 0,952. Voir d'autres générés aide face à un générateur inconnu.

### expC_srm_loso_uniward_p04.png
Généralisation à un générateur non vu, S-UNIWARD. Ce qu'elle montre : Midjourney et ADM gagnent (0,609 vers
0,772, 0,645 vers 0,716), Stable Diffusion non (0,563 vers 0,595), cohérent avec l'interférence.

### expC_srm_loso_hill_p04.png
Généralisation à un générateur non vu, HILL. Même profil : Midjourney 0,555 vers 0,684, ADM 0,576 vers 0,600,
Stable Diffusion sans gain (0,536 vers 0,547).

## Expérience D, stéganalyse multi-classe (SRM)

### expD_srm_confusion_natural_p04.png
Matrice de confusion des quatre classes cover, LSB, S-UNIWARD, HILL sur la source naturelle, 10000 images par
classe, normalisée par vraie classe. Ce qu'elle montre : LSB est identifié presque parfaitement (rappel
0,95), sa ligne est très diagonale ; cover, S-UNIWARD et HILL se confondent entre eux, leurs lignes étalées,
HILL le plus dispersé (rappel 0,32). L'attribution est facile pour l'insertion grossière, difficile entre
schémas adaptatifs.

## Synthèse transversale

Les figures convergent, à l'échelle 10000 et sur les quatre sources naturel, Stable Diffusion, Midjourney,
ADM. Sur les deux axes, décalage de domaine (A) et interférence (B), Stable Diffusion est la source la plus
affectée, seule à masquer l'insertion ; Midjourney et ADM ne masquent pas, Midjourney rendant même la trace
plus visible. Pour LSB, l'adaptation du détecteur (C) répare le décalage de domaine partout. Pour les
adaptatifs, la détection progresse avec les données (A) et l'adaptation la récupère sur Midjourney et ADM,
mais bute sur Stable Diffusion, où l'interférence plafonne même le détecteur apparié au niveau du hasard.
L'attribution multi-classe (D) isole bien LSB mais confond les schémas adaptatifs entre eux.
