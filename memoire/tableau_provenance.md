# Tableau de provenance

Trace, pour chaque unité rédigée, l'information avancée et sa source dans la bibliographie. Sert à garantir
la traçabilité et à éviter le plagiat : chaque source est reformulée, jamais recopiée. Les numéros renvoient
à `bibliographie.md`.

| Unité | Information avancée | Source |
|---|---|---|
| Ouverture | Cas ZeusVM (février 2014), photo de coucher de soleil trahie par sa taille, liste chiffrée des banques ciblées ajoutée en fin de fichier | [49] |
| Ouverture | Principe de la stéganographie, distinction avec le chiffrement | [2] |
| Ouverture | Cas non isolé, malware utilisant l'information cachée comme défi reconnu, Duqu | [50] |
| Ouverture | Stegoloader, charge dissimulée dans une image PNG légitime | [51] |
| Ouverture | Analogie stéganalyse et cryptanalyse, déplacement introduit par les images générées | cadrage de l'auteur, sans source directe |
| Problématique | Question centrale et deux pistes, changement de source et interférence | cadrage de l'auteur, sans source directe |
| Problématique | Le décalage entre sources est documenté (cover-source mismatch) | [31] |
| Contributions | Deux apports, corpus contrôlé et démonstration quantifiée des deux problèmes | cadrage de l'auteur, sans source directe |
| 1.1 | Définition et principe (dissimuler l'existence), supports multimédias variés | [52] |
| 1.1 | Lexique cover, payload, stego ; indétectabilité ; capacité de charge utile | [2] |
| 1.1 | Unité bits par pixel (bpp) et compromis entre quantité et discrétion | [2] |
| 1.1 | Histoire de la stéganographie (Antiquité, micropoint) et étymologie | [52] |
| 1.1 | Représentation d'une image en pixels, canaux, niveaux de gris comme dans BOSSbase | [48] |
| 1.1 | Zones lisses, textures, contours et bruit du capteur dans une image naturelle | [2] |
| 1.1 | Insertion LSB et LSB matching | [39] |
| 1.1 | Insertion adaptative, coût de distorsion, zones difficiles ; HUGO, WOW, S-UNIWARD, HILL | [1], [3], [20], [38] |
| 1.2 | But de la stéganalyse, stéganalyse ciblée et universelle | [2] |
| 1.2.1 | Histogramme des valeurs de pixels dans une image naturelle | [2] |
| 1.2.1 | Attaque du chi-deux, égalisation des paires de valeurs par la substitution LSB, stéganalyse ciblée | [28] |
| 1.2.2 | Passage aux caractéristiques et à l'apprentissage ; descripteur SPAM (686 valeurs) et SVM | [29] |
| 1.2.2 | SPAM vise les insertions ajoutant un faible signal semblable à du bruit, dont le LSB matching | [29] |
| 1.2.3 | Limite de SPAM : écrêtage des différences, aveugle dans les zones texturées | [29] |
| 1.2.3 | HUGO conçu pour préserver des statistiques de voisinage proches de SPAM | [1] |
| 1.2.3 | Modèles riches, résidus par filtres, co-occurrences, SRM à 34 671 caractéristiques | [4] |
| Organisation | Annonce détaillée des chapitres | cadrage de l'auteur, sans source directe |
| Chapeau Partie I | Parcours de l'état de l'art | cadrage de l'auteur, sans source directe |
| 1.2.4 | Ensemble de FLD sur sous-espaces aléatoires, vote, rapidité en grande dimension ; P_E | [30] |
| 1.2.4 | PFA, sélection de caractéristiques représentatives | [36] |
| 1.2.4 | PFA appliquée à la stéganalyse universelle | [37] |
| 1.2.5 | SRNet, apprentissage bout en bout sans filtres fixés, performances supérieures aux modèles riches | [5] |
| 1.3 | Fausse alarme, détection manquée, ROC, AUC | notions générales de classification |
| 1.3 | Probabilité d'erreur minimale P_E | [30] |
| 1.3 | BOSSbase comme base de référence | [48] |
| 2.1 | Principe des GAN, générateur et discriminateur | [6] |
| 2.1 | ProGAN, croissance progressive ; StyleGAN | [8], [7] |
| 2.1 | Artefacts de suréchantillonnage dans le spectre | [9], [47] |
| 2.1 | Écarts en hautes fréquences | [10] |
| 2.1 | Empreinte propre à chaque GAN, analogie avec le bruit du capteur | [12] |
| 2.2 | Principe des VAE, encodeur, espace latent, décodeur | [11] |
| 2.2 | Flou des VAE | connaissance générale, sans source directe |
| 2.2 | Auto-encodeur au cœur de la diffusion latente | [43] |
| 2.2, 2.3 | Artefacts de Fourier pour diffusion et VQ-GAN, écarts en moyennes et hautes fréquences | [14] |
| 2.3 | Principe de la diffusion, bruitage et débruitage | [13] |
| 2.3 | ADM, diffusion dans l'espace des pixels, supérieure aux GAN | [44] |
| 2.3 | Diffusion latente, coût réduit, Stable Diffusion | [43] |
| 2.3 | Lien entre zone des traces et zone de l'insertion | cadrage de l'auteur, sans source directe |
| 2.4 | Modèles de langue, prédiction du mot suivant | [16] |
| 2.4 | DetectGPT, variation de probabilité sous perturbation | [17] |
| 2.4 | Binoculars, comparaison de deux modèles | [18] |
| 3.1 | Cover-source mismatch étudié depuis une vingtaine d'années | [31] |
| 3.1 | Notion d'interférence, rareté des travaux combinant les deux effets | cadrage de l'auteur, sans source directe |
| 3.2 | HiDDeN, encodeur, décodeur, couches de bruit | [21] |
| 3.2 | SteganoGAN, critique, capacité 4,4 bpp | [22] |
| 3.3 | Tree-Ring, motif dans le spectre du bruit initial, inversion | [23] |
| 3.3 | Stable Signature, décodeur modifié, extracteur | [24] |
| 3.3 | SynthID, plus de dix milliards d'images et de trames, vérification réservée | [26] |
| 3.3 | Tatouage du texte | [25] |
| 4.1 | Revue du cover-source mismatch, causes, phénomène négligé | [31] |
| 4.2 | Détecteur entraîné sur ProGAN avec augmentations, généralisation | [45] |
| 4.2 | Détection par analyse fréquentielle | [47] |
| 4.2 | Difficulté des détecteurs GAN face à la diffusion ; DIRE | [46] |
| 4.2 | DE-FAKE, appui sur le texte | [15] |
| 4.2 | GenImage, généralisation entre générateurs | [41] |
| 4.3 | Effacement des tatouages au niveau pixel par régénération | [27] |
| 4.4 | Adaptation de domaine, apprentissage par transfert | [19] |
| 4.4 | Exemples construits à partir des images analysées ; quelques images de la source visée à l'entraînement ; alignement de variétés ; émulation de la source visée (TADA) | [32], [33], [34], [35] |
| 4.4 | Séparation des traces de source et de message | cadrage de l'auteur, sans source directe |
| 5 | Synthèse et positionnement | cadrage de l'auteur, appuyé sur les chapitres 1 à 4 |
| 1.2.4 (corrigé) | La pratique combine PCA et exploration de la PFA | `results/methode_detecteur.md`, `results/experience_A.md` |
| 6.1 | Hypothèses H1, H2, H3 et question de l'attribution | `results/experience_A-D.md`, cadrage de l'auteur |
| 6.2 | BOSSbase 1.01, photographies en niveaux de gris | [48] |
| 6.2 | DiffusionDB, images Stable Diffusion produites par des utilisateurs | [42] |
| 6.2 | GenImage, Midjourney et ADM, contenu ImageNet | [41], `CORPUS.md` |
| 6.2 | Remplacement de SDXL par Midjourney, prétraitement, limite du contenu | `CORPUS.md`, `results/synthese_resultats.md` |
| 6.3 | LSB matching, S-UNIWARD, HILL, 0,4 bpp, seize ensembles | [39], [20], [38], `CORPUS.md` |
| 6.3 | Insertion simulée par conseal | [53] |
| 6.4 | SRM 34 671 caractéristiques, extraction sealwatch | [4], [54] |
| 6.4 | Essai SPAM, chaîne normalisation, PCA 300, régression logistique ; choix sans apprentissage profond | `results/methode_detecteur.md`, `src/run_experiment_A_vps.py`, [30], [5] |
| 6.5 | PFA, S-SELECT, silhouette | [36], [37] |
| 6.5 | Variante supervisée et résultats préliminaires (24 caractéristiques, 0,912 contre 0,933 ; silhouette 0,738) | `results/evaluation_pfa.md` |
| 6.6 | AUC, seuil à 5 % de faux positifs sur le naturel, cas croisé et apparié, validation croisée à cinq plis, écart type 0,005, partition fixe pour C | `results/experience_A.md`, `results/experience_C.md`, scripts `src/` |
| 7.1 | Références, AUC croisées et appariées, faux positifs (tableau 7.1) ; progression depuis 5 000 images | `results/experience_A.md`, `results/resultats_A/resultats_A.txt` |
| 7.2 | Tentative par moments globaux écartée ; distance de Mahalanobis après PCA 200, covariance Ledoit-Wolf (tableau 7.2) | `results/experience_B.md`, `results/resultats_B/resultats_B.txt`, `src/run_experiment_B_vps.py` |
| 7.2 | Hypothèse du contenu plus lisse pour Midjourney | interprétation de l'auteur, à confirmer |
| 7.3 | Convergence A et B ; confusion générateur et contenu | `results/synthese_resultats.md`, cadrage de l'auteur |
| 1.1.1 (révisé) | L'image, support le plus courant de la stéganographie | [52] |
| 1.1.4 (révisé) | Fonctionnement de HUGO (distorsion sur statistiques de voisinage), WOW (filtres directionnels, coût faible seulement si toutes les directions sont imprévisibles), S-UNIWARD (formule universelle, domaine spatial), HILL (passe-haut puis deux passe-bas, regroupement des modifications) | [1], [3], [20], [38] |
| 1.2.2 (révisé) | SPAM : différences dans huit directions, chaîne de Markov d'ordre deux, 686 valeurs ; SVM à marge maximale et noyau | [29] |
| 1.3 (révisé) | BOSS, Break Our Steganographic System | [48] |
| 2.4 (révisé) | WaveNet, génération audio échantillon par échantillon | [55] |
| 2.4 (révisé) | Détection des voix de synthèse, compétition ASVspoof | [57] |
| 2.4 (révisé) | Modèles de diffusion vidéo, génération conjointe de plusieurs images | [56] |
| 2.3.2 | Autocorrélation anormale, transfert des biais des données d'entraînement | [14] |
| 2.5 | Tableau 2.1 de synthèse des familles de générateurs | [9], [12], [14], [43], [47], cadrage de l'auteur |
| 3.4 | Stéganographie générative du texte par codage arithmétique sur un modèle de langue | [60] |
| 3.4 | Pulsar, message encodé dans le hasard de la diffusion, plusieurs centaines d'octets par image | [61] |
| 4.1.2 | La chaîne de traitement est le facteur principal du mismatch ; deux remèdes (diversité, identification de la source) | [58] |
| 4.2.2 | Détecteurs réel/faux biaisés vers les défauts vus ; caractéristiques CLIP pour généraliser | [59] |
| 4.4.2 | Empreinte stable du générateur, analogie avec le bruit de capteur | [12] |
| 5.1 | Tableau 5.1 de comparaison des approches | chapitres 1 à 4, cadrage de l'auteur |
| 5.2, 5.3 | Trois lacunes, réponse par H1, H2, H3 et le corpus | cadrage de l'auteur |
| 1.1.2 (formule) | Charge alpha = m/N en bpp | [2] |
| 1.1.3 (formules) | Substitution LSB y = 2 floor(x/2) + b ; LSB matching y = x ± 1 | [39] |
| 1.1.4 (formule) | Distorsion additive D = somme des coûts des pixels modifiés | [1], [20], [38] |
| 1.2.1 (formule) | Statistique du chi-deux sur les paires de valeurs | [28] |
| 1.2.3 (formule) | Résidu r = x - prédiction ; différence entre voisins | [4], [29] |
| 1.3 (formules) | AUC comme probabilité de bon ordonnancement ; P_E = min ½ (P_FA + P_MD) | [30] |
| 7.2 (formule) | Distance de Mahalanobis | `src/run_experiment_B_vps.py` |
