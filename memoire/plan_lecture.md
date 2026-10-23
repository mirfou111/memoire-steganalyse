# Plan de lecture et de rédaction de l'état de l'art

Fichier de travail. Pour chaque point du plan, les ressources à lire avant de rédiger : d'abord une
lecture d'introduction accessible quand elle existe, puis les articles scientifiques, référencés par leur
numéro dans `bibliographie.md`. On lit, on rédige à sa main, on recense au passage toute source nouvelle
dans la bibliographie. Le tableau de suivi en fin de fichier permet de cocher lecture et rédaction.

Convention des numéros : ils renvoient à `bibliographie.md`. Les liens directs des ressources sont donnés
une fois ici pour gagner du temps.

---

## 1. Introduction

Objectif : poser le contexte, l'essor des images générées par IA, et le problème que cela crée pour la
stéganalyse classique. Formuler la problématique et annoncer le plan.

Lectures :
- [31] Revue systématique du cover-source mismatch en stéganalyse, EURASIP 2024. Le cadre théorique
  central du mémoire.
- [41] GenImage, NeurIPS 2023. Montre l'ampleur du contenu généré et la difficulté de détection.
- [2] Fridrich, Steganography in Digital Media, 2009. Pour cadrer stéganographie et stéganalyse.

Rien à rédiger avant d'avoir en tête le fil : image générée comme nouvelle source de couverture.

## 2. Fondements de la stéganographie et de la stéganalyse

### 2.1 Principes de la stéganographie
Objectif : cover, stégo, indétectabilité, charge utile en bpp, insertion naïve puis adaptative.
Lectures : [2] (chapitres d'introduction), [40] Simmons (problème des prisonniers), [39] LSB matching,
[1] HUGO, [3] WOW, [20] S-UNIWARD, [38] HILL.

### 2.2 Stéganalyse classique : SRM et approches statistiques
Objectif : des tests statistiques aux modèles riches, et le classifieur.
Lectures : [28] attaque du chi-deux, [29] SPAM, [4] SRM (descripteur central du mémoire), [30] ensemble
classifier, [5] SRNet (pour situer le deep learning en perspective).

### 2.3 Métriques d'évaluation (AUC, payload capacity, bpp)
Objectif : définir AUC-ROC, taux de fausses alarmes, charge en bpp, et le protocole d'évaluation.
Lectures : [2] pour les définitions, [30] pour le protocole d'évaluation par validation, [48] BOSSbase
pour le jeu de référence et la notion de cover-source mismatch.

## 3. Contenu généré par IA : techniques et artefacts

### 3.1 GANs et leur signature fréquentielle
Objectif : principe des GANs, et les artefacts fréquentiels qu'ils laissent.
Introduction accessible : cours GAN de Google, https://developers.google.com/machine-learning/gan
Lectures : [6] GAN, [7] StyleGAN, [8] ProGAN, [47] Frank, analyse fréquentielle des deepfakes,
[10] Dzanic, écarts de spectre, [9] Zhang, [12] Marra, empreintes de GANs.

### 3.2 VAEs et leurs propriétés statistiques
Objectif : principe des auto-encodeurs variationnels et ce qui les distingue statistiquement.
Introduction accessible : Lil'Log, From Autoencoder to Beta-VAE,
https://lilianweng.github.io/posts/2018-08-12-vae/
Lectures : [11] Kingma et Welling. La littérature de détection propre aux VAE est mince, à mentionner
comme telle.

### 3.3 Modèles de diffusion et résidus de débruitage
Objectif : principe de la diffusion, latente contre espace pixel, et les résidus exploitables.
Introduction accessible : Lilian Weng, What are Diffusion Models,
https://lilianweng.github.io/posts/2021-07-11-diffusion-models/
Lectures : [13] DDPM, [44] Dhariwal et Nichol (ADM, ta source pixel), [43] Rombach (diffusion latente,
Stable Diffusion), [14] Corvi (décalage de distribution en diffusion latente), [46] DIRE.
Sources de données à citer : [41] GenImage, [42] DiffusionDB.

### 3.4 LLMs et perplexité
Objectif : mention du texte généré et de sa détection par perplexité, hors périmètre pratique.
Lectures : [16] GPT-3, [17] DetectGPT, [18] Binoculars.

## 4. Stéganographie dans le contenu généré par IA

### 4.1 Stéganographie classique appliquée aux images IA
Objectif : que devient l'insertion classique sur une image générée, et l'interférence des artefacts.
Lectures : [2] pour l'insertion classique, [31] pour le décalage de source. C'est un point peu traité
dans la littérature, ce qui justifie la contribution du mémoire ; le dire explicitement.

### 4.2 Stéganographie apprise (HiDDeN, SteganoGAN)
Objectif : l'insertion apprise de bout en bout.
Lectures : [21] HiDDeN, [22] SteganoGAN.

### 4.3 Watermarking natif (Tree-Ring, SynthID, Stable Signature)
Objectif : marquage à la génération, distinct de la stéganographie, et ses limites.
Lectures : [23] Tree-Ring, [24] Stable Signature, [26] SynthID, [25] filigrane pour LLM, [27] retrait de
filigrane par méthodes spectrales.

## 5. Stéganalyse face au contenu généré par IA

### 5.1 Limites des détecteurs classiques (domain shift)
Objectif : pourquoi un détecteur entraîné sur le naturel échoue sur le généré.
Lectures : [31] revue du cover-source mismatch, [19] transfer learning, [48] BOSSbase (le mismatch y est
déjà identifié).

### 5.2 Forensique IA : CNNDetection, Corvi 2023
Objectif : les détecteurs dédiés au contenu généré, et leur généralisation.
Lectures : [45] CNNDetection, [14] Corvi, [46] DIRE, [15] DE-FAKE.

### 5.3 Vérification de watermark et ses limites
Objectif : détecter via un filigrane, et pourquoi cela ne suffit pas.
Lectures : [23], [24], [26] pour les méthodes, [27] pour les attaques de retrait.

### 5.4 Pistes émergentes : disentanglement, domain adaptation
Objectif : séparer artefact de génération et artefact d'insertion, adapter le détecteur à la source.
Lectures : [32] adaptation adversariale, [33] multi-sources, [34] alignement de variétés, [35] méthode
tenant compte du domaine fréquentiel.

## 6. Synthèse critique et positionnement

Objectif : dégager les lacunes, les questions ouvertes, et situer le mémoire, notamment autour du
cover-source mismatch génératif et de l'interférence, peu traités.
Lectures : reprise transversale, en particulier [31], et l'ensemble des points précédents. Pas de nouvelle
lecture, c'est une mise en perspective.

---

## Tableau de suivi

Statuts possibles : a lire, en cours, lu pour la lecture ; a faire, en cours, redige pour la rédaction.

| Point | Lecture | Rédaction | Notes |
|---|---|---|---|
| 1. Introduction | a lire | a faire | |
| 2.1 Principes stéganographie | a lire | a faire | échantillon de style déjà écrit, à reprendre |
| 2.2 Stéganalyse SRM et statistique | a lire | a faire | |
| 2.3 Métriques | a lire | a faire | |
| 3.1 GANs et signature fréquentielle | a lire | a faire | |
| 3.2 VAEs | a lire | a faire | littérature de détection mince |
| 3.3 Diffusion et résidus | a lire | a faire | cœur du sujet |
| 3.4 LLMs et perplexité | a lire | a faire | hors périmètre pratique |
| 4.1 Stéganographie classique sur images IA | a lire | a faire | point de contribution |
| 4.2 Stéganographie apprise | a lire | a faire | |
| 4.3 Watermarking natif | a lire | a faire | |
| 5.1 Limites des détecteurs classiques | a lire | a faire | |
| 5.2 Forensique IA | a lire | a faire | |
| 5.3 Vérification de watermark | a lire | a faire | |
| 5.4 Pistes émergentes | a lire | a faire | |
| 6. Synthèse et positionnement | a lire | a faire | à écrire en dernier |
