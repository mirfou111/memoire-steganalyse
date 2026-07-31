# Historique des détecteurs et des extracteurs en stéganalyse

Fiche de référence pour la rédaction et la soutenance. Elle retrace l'évolution des méthodes de
détection, côté classifieur et côté caractéristiques, avec les articles fondateurs.

Note : vérifiez le format exact des citations (pages, DOI) avant l'insertion finale dans le mémoire.

## Partie 1 : les classifieurs, comment on décide

### 1. Tests statistiques directs, sans apprentissage (fin 1990 à début 2000)

On calcule une statistique sur l'image et on la compare à un seuil. Pas de modèle entraîné.

- Westfeld, Pfitzmann, "Attacks on Steganographic Systems", Information Hiding, 1999. Attaque du chi-deux
  contre le LSB.
- Fridrich, Goljan, Du, "Reliable Detection of LSB Steganography in Color and Grayscale Images",
  ACM Multimedia, 2001. Analyse RS.
- Dumitrescu, Wu, Wang, "Detection of LSB Steganography via Sample Pair Analysis", IEEE Trans. Signal
  Processing, 2003.

### 2. Caractéristiques plus SVM (milieu des années 2000)

On extrait des caractéristiques, puis on entraîne une machine à vecteurs de support. Ce fut le standard
pendant des années.

- Lyu, Farid, "Detecting Hidden Messages Using Higher-Order Statistics and Support Vector Machines",
  Information Hiding, 2002.
- Pevny, Bas, Fridrich, "Steganalysis by Subtractive Pixel Adjacency Matrix" (SPAM), IEEE Trans.
  Information Forensics and Security, 2010.

### 3. Caractéristiques riches plus ensemble de FLD (à partir de 2012)

La dimension des caractéristiques explose, la SVM devient trop coûteuse. On passe à un ensemble de
discriminants linéaires de Fisher entraînés sur des sous-espaces aléatoires, rapide et scalable.

- Kodovsky, Fridrich, Holub, "Ensemble Classifiers for Steganalysis of Digital Media", IEEE Trans.
  Information Forensics and Security, 2012.

C'est le couple classique caractéristiques riches plus ensemble de FLD. La régression logistique utilisée
dans ce mémoire appartient à la même famille des classifieurs linéaires, en plus simple à expliquer.

### 4. Réseaux profonds, bout en bout (à partir de 2015)

Le réseau apprend lui-même les caractéristiques et la décision. État de l'art actuel de la performance.

- Qian, Dong, Wang, Tan, "Deep Learning for Steganalysis via Convolutional Neural Networks", SPIE, 2015.
- Xu, Wu, Shi, "Structural Design of Convolutional Neural Networks for Steganalysis" (Xu-Net), IEEE Signal
  Processing Letters, 2016.
- Ye, Ni, Yi, "Deep Learning Hierarchical Representations for Image Steganalysis" (Ye-Net), IEEE Trans.
  Information Forensics and Security, 2017.
- Boroumand, Chen, Fridrich, "Deep Residual Network for Steganalysis of Digital Images" (SRNet), IEEE
  Trans. Information Forensics and Security, 2019.

## Partie 2 : les extracteurs, comment on décrit l'image

### Statistiques d'ordre supérieur et ondelettes

- Lyu, Farid, "Detecting Hidden Messages Using Higher-Order Statistics and Support Vector Machines",
  Information Hiding, 2002.

### Modèles de Markov et SPAM

- Shi et al., "A Markov Process Based Approach to Effective Attacking JPEG Steganography", Information
  Hiding, 2007.
- Pevny, Bas, Fridrich, SPAM, IEEE TIFS, 2010. 686 dimensions, celui utilisé ici.

### Modèles riches spatiaux, SRM

- Fridrich, Kodovsky, "Rich Models for Steganalysis of Digital Images", IEEE Trans. Information Forensics
  and Security, 2012. Environ 34000 dimensions, la référence lourde, prévue pour la suite.

### Modèles riches pour le domaine JPEG

- Holub, Fridrich, "Low-Complexity Features for JPEG Steganalysis Using Undecimated DCT" (DCTR), IEEE TIFS,
  2015.
- Song et al., "Steganalysis of Adaptive JPEG Steganography Using 2D Gabor Filters" (GFR), IH&MMSec, 2015.

## Partie 3 : réduction de caractéristiques et stéganalyse universelle

Le grand nombre de caractéristiques riches motive des méthodes de réduction, pour rendre l'apprentissage
abordable. C'est le fil qui relie ce mémoire au travail de l'encadrant.

- Lu, Plataniotis, Venetsanopoulos, "Feature Selection Using Principal Feature Analysis" (PFA), ACM
  Multimedia, 2007. La méthode PFA d'origine.
- Article de l'encadrant, "Feature Reduction Algorithm for Universal Steganalysis". Applique une sélection
  de caractéristiques par PFA à la stéganalyse universelle.

## Situer notre choix

Notre détecteur, SPAM plus régression logistique, se situe dans la lignée caractéristiques faites main
plus classifieur linéaire, entre l'ère SVM et l'ère ensemble de FLD. Le passage prévu vers SRM avec
réduction PFA nous fait rejoindre la logique moderne de réduction de caractéristiques, sans recourir au
deep learning.
