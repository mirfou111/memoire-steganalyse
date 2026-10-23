% Plan du mémoire : proposition pour validation
% Ousmane Ndiéguène
% Septembre 2026

Sujet : stéganographie et stéganalyse face aux contenus générés par intelligence artificielle.

Le mémoire s'ouvre sur une introduction générale, suivie de deux parties, et se ferme sur une conclusion
générale. La première partie, l'état de l'art, a été validée dans ses grandes lignes. La seconde présente la
contribution pratique, alignée sur les expériences réellement menées.

# Introduction générale

- Contexte et enjeux : stéganographie, stéganalyse, et l'essor des images générées par IA.
- Problématique : dans quelle mesure la stéganalyse classique reste-t-elle applicable au contenu généré ?
- Contributions du mémoire :
    1. Un corpus contrôlé pour la stéganalyse à l'ère générative : quatre sources traitées à l'identique,
       dont une commerciale, à 10000 images chacune, avec pour chaque image sa version vierge et ses
       versions porteuses. Un artefact réutilisable.
    2. Une démonstration quantifiée des deux difficultés que le contenu généré pose à la stéganalyse
       classique, le décalage de domaine et l'interférence, et de leur traitement par adaptation du
       détecteur, avec la distinction nette entre ce qui se répare et ce qui ne se répare pas.
  La nouveauté tient à la curation et à la mise en évidence, non à la création d'images ni d'une nouvelle
  méthode de détection.
- Annonce du plan.

# Partie I : État de l'art

## 1. Fondements de la stéganographie et de la stéganalyse

- 1.1 Principes de la stéganographie.
- 1.2 Stéganalyse classique : SRM et approches statistiques.
- 1.3 Métriques d'évaluation (AUC, payload, bpp).

## 2. Contenu généré par IA : techniques et artefacts

- 2.1 GANs et leur signature fréquentielle.
- 2.2 VAEs et leurs propriétés statistiques.
- 2.3 Modèles de diffusion et résidus de débruitage.
- 2.4 Modèles de langue et perplexité.

## 3. Stéganographie dans le contenu généré par IA

- 3.1 Stéganographie classique appliquée aux images générées.
- 3.2 Stéganographie apprise (HiDDeN, SteganoGAN).
- 3.3 Watermarking natif (Tree-Ring, SynthID, Stable Signature).

## 4. Stéganalyse face au contenu généré par IA

- 4.1 Limites des détecteurs classiques (décalage de domaine).
- 4.2 Forensique IA (CNNDetection, Corvi).
- 4.3 Vérification de watermark et ses limites.
- 4.4 Pistes émergentes : disentanglement, adaptation de domaine.

## 5. Synthèse critique et positionnement

- Lacunes identifiées, questions ouvertes, positionnement du mémoire dans le cover-source mismatch génératif.

# Partie II : Cas pratique

## 6. Méthodologie expérimentale

- 6.1 Objectifs et hypothèses : décalage de domaine (H1), interférence (H2), solution (H3), et la question
  de l'attribution d'algorithme.
- 6.2 Constitution du corpus : quatre sources (naturel, Stable Diffusion, Midjourney, ADM), 10000 images,
  prétraitement uniforme. Le corpus contrôlé comme apport.
- 6.3 Insertion stéganographique : LSB, S-UNIWARD, HILL, simulées avec conseal.
- 6.4 Détecteur de stéganalyse : caractéristiques SRM, réduction, classifieur linéaire, et choix assumé de
  ne pas recourir au deep learning.
- 6.5 Réduction de caractéristiques : PFA et S-SELECT, avec une variante supervisée.
- 6.6 Métriques, protocole de rigueur et infrastructure.

## 7. Les deux problèmes

- 7.1 Décalage de domaine (Expérience A) : effondrement du détecteur transféré du naturel au généré, faux
  positifs massifs.
- 7.2 Interférence des artefacts (Expérience B) : mesure sans détecteur, Stable Diffusion masque l'insertion.
- 7.3 Convergence : parmi les générateurs, Stable Diffusion est le seul à cumuler les deux difficultés,
  Midjourney et ADM se comportent autrement.

## 8. La solution

- 8.1 Adaptation du détecteur (Expérience C) : réentraînement mixte, détection consciente de la source,
  borne apparié.
- 8.2 Résultats et généralisation à un générateur non vu.
- 8.3 Portée et limite : l'adaptation répare le décalage de domaine, mais pas l'interférence de Stable
  Diffusion en insertion adaptative.

## 9. Ouverture : attribution multi-classe

- 9.1 Principe : identifier l'algorithme employé, et non plus seulement la présence d'un message.
- 9.2 Résultats exploratoires (Expérience D) : LSB s'isole nettement, les schémas adaptatifs se confondent ;
  discussion honnête du caractère préliminaire de cette piste.

## 10. Discussion générale et perspectives

- 10.1 Fil rouge et positionnement dans le cover-source mismatch génératif.
- 10.2 Limites : confond entre générateur et contenu, plafond des adaptatifs, coût de la réduction.
- 10.3 Perspectives : stéganalyse profonde, seconde source Stable Diffusion, intégration plus centrale de la
  réduction PFA.

# Conclusion générale

- Rappel des apports, réponse à la problématique, prolongements.

# Bibliographie

# Annexes

- Notebooks et scripts, tableaux de résultats, détails d'implémentation.
