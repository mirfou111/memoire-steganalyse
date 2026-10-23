# Suivi des figures du mémoire

Les figures prévues sont décrites ici, hors du docx, pour ne pas l'encombrer. Pour chacune : emplacement
exact, contenu, production, appel dans le texte et légende proposée. Règle : on ne copie jamais une figure
d'un article. Soit on la dessine, soit on la génère à partir de nos données ; si une figure s'inspire d'une
source, la légende indique « adapté de [n] ».

## Vue d'ensemble

Mise à jour du 18 octobre : figures produites par `src/figures_partie1.py`, fichiers dans
`memoire/figures/`. Images sources libres (Wikimedia Commons), à citer dans chaque légende :

- `Cheikh_Anta_Diop,_late_1940s.jpg` : auteur inconnu, domaine public (figure 1.2) ;
- `Thiéboudiène_Boukhonk_with_tamarind.jpg` : T. K. Naliaka, CC BY-SA 4.0 (figure 1.3) ;
- `Baobab_du_Sénégal_Palmarin_04.jpg` : 4MAPS, CC BY-SA 4.0 (figures 1.4 et 1.5).

La carte HILL est une simulation recodée d'après la fonction de coût de l'article [38], sans conseal ;
la refaire avec conseal si possible. Les figures ne sont pas dans le fichier de travail, seulement dans la
version de relecture `Memoire_Ndieguene_Intro_PartieI_relecture.docx`.

| N° | Section | Titre | Fichier | Image source |
|---|---|---|---|---|
| 1.1 | 1.1.1 | Chaîne stéganographique (Awa, Moussa, le gardien) | `fig1_1_chaine.png` | schéma de l'auteur |
| 1.2 | 1.1.3 | L'image vue comme une matrice | `fig1_2_matrice.png` | portrait de Cheikh Anta Diop |
| 1.3 | 1.1.3 | Insertion LSB, lettre « T » | `fig1_3_lsb.png` | thiéboudiène |
| 1.4 | 1.1.4 | Pixels modifiés, LSB matching contre HILL | `fig1_4_modifications.png` | baobab de Palmarin |
| 1.5 | 1.2.1 | Histogramme avant et après substitution LSB | `fig1_5_histogramme.png` | baobab de Palmarin |
| 2.1, 5.1 | 2.5, 5.1 | Tableaux de synthèse | dans le texte | |

Les descriptions détaillées ci-dessous datent de la première planification ; la numérotation ci-dessus fait foi.

## Figure 1.1 : Chaîne stéganographique

- Emplacement : fin de 1.1.1, après le paragraphe sur le lexique (cover, payload, stego).
- Contenu : de gauche à droite, le message (payload) et l'image de couverture (cover) entrent dans un bloc
  d'insertion, avec une clé secrète facultative. En sortie, le stégo-objet (stego) part sur un canal de
  transmission surveillé par un observateur, le stéganalyste. À l'arrivée, un bloc d'extraction utilise la
  même clé pour retrouver le message.
- Production : schéma dessiné par l'auteur (draw.io ou PowerPoint), avec exactement le vocabulaire du texte.
- Appel dans le texte : « (figure 1.1) » après la phrase qui définit le stégo-objet.
- Légende proposée : « Figure 1.1 : Chaîne stéganographique. Le message est inséré dans le support de
  couverture pour produire le stégo-objet, qui circule sous l'œil d'un observateur avant d'être extrait par
  le destinataire. »

## Figure 1.2 (facultative) : Le compromis entre quantité et discrétion

- Emplacement : fin de 1.1.2, après le paragraphe sur le compromis.
- Contenu : courbe qualitative, sans valeurs chiffrées. En abscisse la charge en bpp, en ordonnée le risque
  de détection ; la courbe monte avec la charge. Une seconde courbe, plus basse, représente l'insertion
  adaptative, pour annoncer la sous-partie 1.1.4.
- Production : schéma de principe dessiné par l'auteur, présenté clairement comme illustratif. À remplacer
  par une courbe réelle si plusieurs charges sont mesurées dans la partie pratique.
- Appel dans le texte : « (figure 1.2) » à la fin de la phrase sur le compromis permanent.
- Légende proposée : « Figure 1.2 : Schéma de principe du compromis entre charge insérée et risque de
  détection. »

## Figure 1.3 : Le LSB, du pixel à l'image

- Emplacement : fin de 1.1.3, après le paragraphe sur le LSB et le LSB matching.
- Contenu : deux panneaux. (a) Un petit tableau de trois ou quatre pixels, avec leur valeur en décimal et en
  binaire, avant et après insertion ; seul le dernier bit change, mis en couleur (par exemple 154, soit
  10011010, qui devient 155, soit 10011011). (b) Une image naturelle du corpus et, à côté, son plan des bits
  de poids faible : il ressemble à du bruit, ce qui montre pourquoi le modifier ne se voit pas à l'œil.
- Production : (a) tableau fait par l'auteur ; (b) généré par un court script sur une image BOSSbase.
- Appel dans le texte : « (figure 1.3) » après la phrase qui décrit le remplacement du dernier bit.
- Légende proposée : « Figure 1.3 : Insertion LSB. (a) Seul le bit de poids faible de chaque pixel est
  modifié. (b) Une image naturelle et son plan de bits de poids faible, proche d'un bruit. »

## Figure 1.4 : Où l'insertion modifie l'image

- Emplacement : 1.1.4, après le paragraphe qui présente HUGO, WOW, S-UNIWARD et HILL.
- Contenu : trois panneaux sur la même image du corpus. (a) L'image de couverture. (b) La carte des pixels
  modifiés par le LSB matching à 0,4 bpp : des points dispersés partout, y compris dans les zones lisses.
  (c) La carte des pixels modifiés par HILL à 0,4 bpp : les changements se concentrent sur les textures et
  les contours.
- Production : générée à partir du corpus avec la bibliothèque conseal utilisée dans les expériences, en
  faisant la différence entre le cover et le stego.
- Appel dans le texte : « (figure 1.4) » après la phrase sur HILL.
- Légende proposée : « Figure 1.4 : Pixels modifiés à charge égale (0,4 bpp). Le LSB matching disperse ses
  modifications, HILL les concentre dans les zones texturées. »

## Figure 1.5 : L'histogramme avant et après insertion LSB

- Emplacement : 1.2.1, après le paragraphe sur l'effet de la substitution LSB et l'attaque du chi-deux.
- Contenu : deux histogrammes superposés ou côte à côte, sur une même plage de valeurs (par exemple de 140 à
  170) d'une image naturelle. (a) Avant insertion : les barres de deux valeurs voisines ont des hauteurs
  différentes. (b) Après substitution LSB à forte charge : chaque paire (154 et 155, 156 et 157...) prend la
  même hauteur, ce qui donne un profil en marches d'escalier.
- Production : court script sur une image BOSSbase, en appliquant une substitution LSB (pas le LSB matching,
  qui ne produit pas cet effet).
- Appel dans le texte : « (figure 1.5) » après la phrase sur le rapprochement des effectifs de chaque paire.
- Légende proposée : « Figure 1.5 : Histogramme d'une image naturelle avant et après substitution LSB. Les
  paires de valeurs voisines s'égalisent, ce que détecte l'attaque du chi-deux. »

## Figures déjà disponibles pour la partie pratique

Issues des expériences (dossier `results/`) : courbes ROC, barres d'AUC, distributions de scores
(Expérience A), distances de Mahalanobis (Expérience B), stratégies d'adaptation et généralisation
(Expérience C), matrice de confusion (Expérience D).

## Chapitre 7 : figures issues des expériences

Fichiers déjà produits dans `results/resultats_A` et `results/resultats_B`. Les chiffres affichés sur les
figures doivent correspondre aux tableaux 7.1 et 7.2 (version à dix mille images).

| N° | Section | Fichier | Emplacement et appel | Légende proposée |
|---|---|---|---|---|
| 7.1 | 7.1 | `expA_srm_roc_lsb_p04.png` | Après le paragraphe « Appliqué tel quel… », appel « (figure 7.1) » | Courbes ROC du détecteur naturel sur sa source et sur les sources générées, LSB à 0,4 bpp. |
| 7.2 | 7.1 | `expA_srm_fprcdf_lsb_p04.png` | Après le paragraphe sur les faux positifs | Distribution des scores sur les images vierges ; au seuil calibré sur le naturel, la majorité des images générées dépasse le seuil. |
| 7.3 | 7.1 | `expA_srm_aucbars_uniward_p04.png` (ou hill) | Après le paragraphe sur la colonne appariée | AUC de référence, croisée et appariée par source, S-UNIWARD : la récupération échoue sur Stable Diffusion. |
| 7.4 | 7.2 | les trois `expB_srm_maha_<algo>_p04.png`, à assembler en une figure à trois panneaux | Après le tableau 7.2 | Distance de Mahalanobis entre vierges et porteuses, par source ; la ligne pointillée marque le niveau naturel. |

À vérifier avant insertion : les anciennes interprétations de `figures_interpretations.md` pour l'expérience
A citent encore SDXL et des valeurs à cinq mille images ; seules les figures régénérées à dix mille images
doivent être utilisées.
