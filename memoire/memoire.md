% Stéganographie et stéganalyse face aux contenus générés par intelligence artificielle
% Ousmane Ndiéguène
% Mémoire de Master, année 2026

# Plan du mémoire

Ce document est le squelette du mémoire. Chaque partie sera rédigée de façon incrémentale. Les mentions
entre crochets indiquent ce que la section contiendra et seront remplacées par le texte définitif.

Registre : nous ou tournures impersonnelles. Encadrant : M. Gomis. Établissement : à compléter.

---

# Introduction générale

[Contexte et enjeux : montée des contenus générés par IA, sécurité de l'information à la croisée du
traitement du signal et de l'apprentissage automatique, rupture introduite par les modèles génératifs.]

[Problématique : dans quelle mesure la stéganalyse existante s'applique-t-elle au contenu généré par
diffusion, et comment caractériser l'interférence entre artefacts de génération et de dissimulation.]

[Objectifs : cartographier l'état de l'art, démontrer les deux problèmes, esquisser une solution.]

[Contributions et annonce du plan.]

# Partie I. État de l'art

## 1. Fondements de la stéganographie et de la stéganalyse

### 1.1 Principes de la stéganographie
[Couverture, stégo-objet, LSB, insertion adaptative, capacité en bpp.]

### 1.2 Stéganalyse classique : des modèles statistiques aux réseaux
[Tests statistiques, SPAM, SRM, SVM, ensemble classifier, SRNet.]

### 1.3 Métriques d'évaluation
[AUC, probabilité d'erreur, capacité.]

## 2. Contenu généré par IA : techniques et artefacts

### 2.1 Réseaux antagonistes génératifs
[Principe, signature fréquentielle.]

### 2.2 Auto-encodeurs variationnels
[Principe, propriétés statistiques.]

### 2.3 Modèles de diffusion
[Principe, résidus de débruitage, absence de signature GAN.]

### 2.4 Modèles de langue
[Mention, perplexité, hors périmètre pratique.]

### 2.5 Implications pour la stéganalyse
[Le décalage de domaine.]

## 3. Stéganographie dans le contenu généré par IA

### 3.1 Stéganographie classique appliquée aux images générées
[Interférence des artefacts.]

### 3.2 Stéganographie apprise
[HiDDeN, SteganoGAN.]

### 3.3 Watermarking natif et ses limites
[Tree-Ring, Stable Signature, SynthID, attaques.]

## 4. Stéganalyse face au contenu généré par IA

### 4.1 Limites des détecteurs classiques
[Décalage de domaine.]

### 4.2 Forensique IA
[CNNDetection, Corvi.]

### 4.3 Cover-source mismatch et adaptation de domaine
[Problème, approches, lien avec les images générées.]

### 4.4 Réduction de caractéristiques pour la stéganalyse universelle
[PFA, article de l'encadrant.]

## 5. Synthèse critique et positionnement
[Lacunes, questions ouvertes, positionnement du mémoire.]

# Partie II. Cas pratique

## 6. Méthodologie expérimentale

### 6.1 Objectifs et hypothèses
[H1 décalage de domaine, H2 interférence, H3 solution.]

### 6.2 Constitution du corpus
[BOSSBase, DiffusionDB, SDXL, ADM, prétraitement uniforme, format sans perte.]

### 6.3 Insertion stéganographique
[LSB, S-UNIWARD, HILL, simulation, charges utiles.]

### 6.4 Détecteur de stéganalyse
[SPAM et SRM, réduction, classifieur, choix et justification.]

### 6.5 Métriques et protocole de rigueur
[AUC, faux positifs, validation croisée, reproductibilité.]

## 7. Résultats : décalage de domaine
[AUC de référence, faux positifs, effondrement cross-domaine, détecteur apparié, cas LSB.]

## 8. Résultats : interférence des artefacts
[Tailles d'effet, spectres, projection, interprétation.]

## 9. Vers une solution
[Adaptation de domaine, détecteur conscient de la source, positionnement CSM, limites.]

## 10. Discussion générale
[Confrontation à la littérature, limites, généralisation.]

# Conclusion générale
[Rappel, contributions, perspectives.]

# Bibliographie
[Références numérotées.]

# Annexes
[Notebooks, tableaux de résultats, détails d'implémentation.]
