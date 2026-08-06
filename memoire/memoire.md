% Stéganographie et stéganalyse face aux contenus générés par intelligence artificielle
% Ousmane Ndiéguène
% Mémoire de Master, année 2026

# Plan du mémoire

Ce document est le squelette du mémoire. Chaque partie sera rédigée de façon incrémentale. Les mentions
entre crochets indiquent ce que la section contiendra et seront remplacées par le texte définitif.

Registre : nous ou tournures impersonnelles. Encadrant : M. Gomis. Établissement : à compléter.

---

# Introduction générale

## Contexte et enjeux

La stéganographie et la stéganalyse forment un couple de disciplines anciennes, à la croisée de la
sécurité de l'information, du traitement du signal et de l'apprentissage automatique. La première cherche
à dissimuler l'existence même d'un message au sein d'un contenu anodin, la seconde à détecter cette
dissimulation. Leur histoire est celle d'une course aux armements, où chaque progrès de l'insertion
appelle un progrès de la détection, et réciproquement. Les méthodes de stéganalyse les plus abouties ont
été conçues et validées sur des images naturelles, dont les propriétés statistiques sont bien
caractérisées et servent de socle aux détecteurs.

L'essor récent des modèles génératifs d'intelligence artificielle, réseaux antagonistes génératifs,
auto-encodeurs variationnels et surtout modèles de diffusion, bouleverse ce socle. Ces modèles ne
capturent pas le monde, ils fabriquent des images à partir de bruit, en y laissant des traces
statistiques involontaires, propres à leur architecture. Le contenu généré présente ainsi une
distribution fondamentalement différente de celle des images naturelles. Deux conséquences en découlent.
D'une part, les détecteurs existants, calibrés sur le naturel, voient leurs hypothèses mises en défaut,
ce qui crée de nouvelles vulnérabilités. D'autre part, ces mêmes modèles deviennent des vecteurs de
dissimulation inédits, sur lesquels la stéganalyse n'a pas encore de recul.

## Problématique

Ce travail s'inscrit dans cette rupture. Il pose la question suivante : dans quelle mesure les techniques
de stéganalyse existantes sont-elles applicables au contenu généré par des modèles de diffusion, et
comment caractériser l'interférence entre les artefacts de génération, propres au modèle, et les artefacts
de dissimulation, propres à l'insertion d'un message ? Cette interférence est au cœur du problème : dans
une image générée puis porteuse d'un message, deux sources de traces statistiques se superposent dans les
mêmes composantes, et rien ne garantit qu'un détecteur classique sache encore les distinguer.

## Objectifs et contributions

L'objectif de ce mémoire est de ne pas se limiter à la littérature, mais de démontrer concrètement, sur un
protocole reproductible, les difficultés que le contenu généré pose à la stéganalyse. Il se décline en
trois volets. D'abord, cartographier l'état de l'art, tant du côté des techniques de génération, pour
comprendre ce que l'on cherche à analyser, que du côté des techniques de détection. Ensuite, démontrer
expérimentalement deux problèmes : le décalage de domaine, qui dégrade un détecteur transféré du naturel
au généré, et l'interférence des artefacts. Enfin, esquisser une solution, en réintroduisant dans le
détecteur la connaissance de la source, et en s'appuyant sur les méthodes de réduction de caractéristiques
adaptées à la stéganalyse universelle.

Les contributions attendues sont la constitution d'un corpus contrôlé mêlant images réelles et générées
par plusieurs modèles, une démonstration quantifiée du décalage de domaine, une caractérisation de
l'interférence des artefacts sur les modèles de diffusion, encore peu traitée, et le positionnement de ce
travail dans le cadre du cover-source mismatch et de la réduction de caractéristiques.

## Organisation du mémoire

Le mémoire est organisé en deux parties. La première dresse l'état de l'art de la stéganographie, de la
stéganalyse et des modèles génératifs, et dégage les lacunes que ce travail entend combler. La seconde
présente la contribution pratique : la méthodologie expérimentale, les résultats obtenus sur le décalage
de domaine et l'interférence, une esquisse de solution, puis une discussion des limites et des
perspectives. Une conclusion générale récapitule les apports et ouvre sur les prolongements possibles.

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
