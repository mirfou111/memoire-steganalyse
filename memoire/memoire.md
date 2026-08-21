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

Le cas pratique confronte un détecteur de stéganalyse classique à des images de sources différentes, afin
de mesurer concrètement les difficultés que le contenu généré pose à la détection. La démarche compare le
comportement du détecteur sur des images naturelles, sur lesquelles il a été conçu, et sur des images
générées par plusieurs modèles de diffusion. Trois hypothèses guident l'expérimentation.

La première, notée H1, est celle du décalage de domaine : un détecteur entraîné sur des images naturelles
perd sa fiabilité sur des images générées, ce qui se traduit par une chute de sa capacité de séparation et
par une hausse de son taux de fausses alarmes. La deuxième, notée H2, est celle de l'interférence : sur
les images générées, la trace de l'insertion est masquée par les artefacts de génération, ce qui réduit
l'écart mesurable entre une image vierge et une image porteuse. La troisième, notée H3, porte sur une
esquisse de solution : réintroduire dans le détecteur la connaissance de la source, et réduire la
dimension des caractéristiques, permet de restaurer une part de la performance.

### 6.2 Constitution du corpus

Le corpus réunit quatre sources d'images. Les images naturelles proviennent de BOSSbase 1.01, jeu de
référence de la stéganalyse. Les images générées proviennent de trois modèles de diffusion, choisis pour
former un spectre de distance architecturale : Stable Diffusion, via le jeu public DiffusionDB, et son
évolution SDXL, tous deux fondés sur la diffusion latente ; et ADM, fondé sur la diffusion en espace
pixel, architecturalement plus éloigné, extrait du jeu GenImage. ADM est retenu comme générateur lointain
parce qu'il maximise le contraste avec Stable Diffusion tout en restant un modèle de diffusion, avec un
contenu proche des images naturelles et une résolution native adaptée.

Le principe directeur de la constitution du corpus est l'isolement d'une seule variable. Toutes les
images, quelle que soit leur source, subissent exactement le même prétraitement : conversion en niveaux de
gris, recadrage centré à 256 pixels de côté, et enregistrement au format PGM sans perte. Ainsi, toute
différence observée dans les expériences ne peut provenir que de la source ou de l'insertion, jamais du
traitement. Le format sans perte est indispensable, car toute compression introduirait des artefacts
susceptibles de masquer ou d'imiter les traces d'insertion.

### 6.3 Insertion stéganographique

Trois algorithmes d'insertion sont appliqués aux images de couverture, choisis pour couvrir un éventail de
conceptions. Le LSB matching, qui modifie légèrement les bits de poids faible, représente l'insertion
naïve. S-UNIWARD et HILL sont deux algorithmes adaptatifs, qui concentrent l'insertion dans les zones
texturées de l'image et sont conçus pour échapper aux modèles statistiques ; ils forment le duo de
référence des travaux récents. Deux charges utiles sont testées, 0,2 et 0,4 bit par pixel, afin de tracer
une courbe de sensibilité entre une insertion discrète et une insertion plus marquée.

L'insertion est réalisée par simulation, à l'aide de la bibliothèque conseal, développée par le
laboratoire à l'origine de ces algorithmes. La simulation reproduit fidèlement les modifications
statistiques qu'entraînerait l'insertion d'un message réel, sans encoder de message extractible. C'est la
pratique standard en recherche de stéganalyse, puisque l'objet d'étude est la détectabilité et non la
communication secrète.

### 6.4 Détecteur de stéganalyse

Le détecteur reproduit la chaîne classique de la stéganalyse, et se compose de deux briques. La première
est l'extraction de caractéristiques. Deux descripteurs sont employés : SPAM, léger, à 686 dimensions,
suffisant pour l'insertion naïve ; et SRM, riche, à plusieurs dizaines de milliers de dimensions, requis
pour les algorithmes adaptatifs que SPAM ne capte pas. La seconde brique est le classifieur, une
régression logistique, modèle linéaire simple et interprétable, qui apprend à séparer les images vierges
des images porteuses.

La grande dimension de SRM impose une étape de réduction, sans laquelle le classifieur surapprend. Deux
approches sont considérées. La première est l'analyse en composantes principales, qui construit des
variables synthétiques. La seconde est la méthode de réduction par analyse en caractéristiques principales
proposée par l'encadrant, qui sélectionne un sous-ensemble des caractéristiques d'origine, plus
interprétables. Une variante supervisée de cette méthode, développée dans ce travail, choisit les
caractéristiques par leur pouvoir de séparation entre cover et stégo.

Le choix d'une chaîne classique plutôt que d'un réseau de neurones profond est délibéré. Il est d'abord
fidèle à la problématique, qui vise à éprouver la stéganalyse classique elle-même. Il privilégie ensuite
la transparence, chaque étape étant explicable, contrairement à une architecture profonde. Il répond enfin
à une contrainte de ressources, la chaîne classique ne demandant pas de matériel spécialisé. La
stéganalyse profonde, qui représente l'état de l'art de la performance, est posée en perspective.

### 6.5 Métriques et protocole de rigueur

La performance de détection est mesurée par l'aire sous la courbe ROC, qui évalue la capacité du détecteur
à séparer les deux classes indépendamment du seuil. Le taux de fausses alarmes, à un seuil calibré pour
cinq pour cent de faux positifs sur les images naturelles, sert à quantifier la confusion introduite par
les images générées. L'interférence, elle, est mesurée sans détecteur entraîné, par une distance
multivariée entre les distributions cover et stégo, une distance plus faible sur une source générée
signalant que l'insertion y est plus masquée.

Plusieurs précautions assurent la robustesse des résultats. Les mesures d'aire sous la courbe reposent sur
une validation croisée répétée, dont on rapporte la moyenne et l'écart type, afin de montrer que le
résultat ne dépend pas d'un découpage particulier. La graine aléatoire est fixée, les découpages sont
documentés, et les caractéristiques extraites sont mises en cache, ce qui rend l'ensemble des
expériences rejouable à l'identique.

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
