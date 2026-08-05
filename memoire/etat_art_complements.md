# Compléments à l'état de l'art

Ces sections complètent le draft existant. Elles ajoutent trois éléments que le cas pratique mobilise
directement : l'évolution des classifieurs de stéganalyse, le problème du cover-source mismatch et
l'adaptation de domaine, et la réduction de caractéristiques pour la stéganalyse universelle.

Registre académique, à insérer aux emplacements indiqués. Les références nouvelles sont numérotées à
partir de [28] et devront être fusionnées avec la bibliographie existante. Le format exact des citations
reste à vérifier avant la version finale.

---

## Complément 1 : des tests statistiques à l'ensemble classifier

À insérer dans la section 2.2, après la présentation des SRM.

L'évolution de la stéganalyse ne concerne pas seulement les caractéristiques extraites, mais aussi la
manière de décider. Les premières méthodes, à la fin des années 1990, reposaient sur des tests
statistiques directs, sans apprentissage : on calculait une statistique sur l'image, comme dans l'attaque
du chi-deux de Westfeld et Pfitzmann [28], et on la comparait à un seuil. Ces approches, efficaces contre
le LSB naïf, se sont révélées insuffisantes face aux techniques adaptatives.

L'introduction de l'apprentissage supervisé a marqué une rupture. On extrait alors un vecteur de
caractéristiques, puis on entraîne un classifieur à séparer les images vierges des stégo-objets. La
machine à vecteurs de support (SVM) s'est imposée comme le classifieur de référence durant les années
2000, notamment associée aux caractéristiques SPAM de Pevný, Bas et Fridrich [29], un descripteur fondé
sur une modélisation markovienne des différences entre pixels voisins.

L'explosion de la dimension des caractéristiques, avec les modèles riches et leurs dizaines de milliers de
dimensions, a rendu la SVM trop coûteuse. Kodovský, Fridrich et Holub [30] ont proposé en réponse
l'ensemble classifier, aujourd'hui standard pour les modèles riches. Il entraîne un grand nombre de
discriminants linéaires de Fisher, chacun sur un sous-espace aléatoire de caractéristiques et un
échantillon aléatoire des données, et agrège leurs votes. Cette construction gère nativement le cas où le
nombre de caractéristiques dépasse largement le nombre d'exemples, tout en restant rapide et peu gourmande
en mémoire.

Enfin, à partir du milieu des années 2010, les réseaux de neurones convolutifs, déjà évoqués avec SRNet,
ont proposé d'apprendre conjointement les caractéristiques et la décision, atteignant l'état de l'art de
la performance au prix d'un coût de calcul et d'une opacité accrus.

## Complément 2 : le cover-source mismatch et l'adaptation de domaine

À insérer dans la section 5, comme nouvelle sous-section 5.x, avant les pistes émergentes.

Un obstacle central à l'application de la stéganalyse en conditions réelles est le cover-source mismatch,
c'est-à-dire l'écart entre la distribution des images d'entraînement et celle des images de test. Un
détecteur entraîné sur une source d'images voit ses performances chuter sur une source différente, car
les hypothèses statistiques apprises ne sont plus valides. Une revue systématique récente [31] dresse le
panorama de ce problème et des stratégies pour l'atténuer.

Les réponses proposées relèvent principalement de l'adaptation de domaine. Certaines approches reposent
sur un entraînement adversarial qui aligne les représentations des deux domaines [32], d'autres sur
l'adaptation multi-sources [33], sur l'alignement de variétés dans un espace latent commun [34], ou encore
sur des méthodes récentes tenant compte du domaine fréquentiel [35]. Le principe commun est de réintroduire
dans le détecteur une connaissance de la source cible, plutôt que de supposer une source unique.

Cette problématique, historiquement étudiée pour des sources naturelles différentes, appareils photo ou
qualités de compression, se pose de manière aiguë pour les images générées par intelligence artificielle,
dont la distribution s'éloigne fortement de celle des images naturelles. C'est précisément le cadre
théorique dans lequel s'inscrit la contribution pratique de ce mémoire : traiter les images de diffusion
comme une nouvelle source, et caractériser puis atténuer le décalage qu'elles induisent.

## Complément 3 : réduction de caractéristiques pour la stéganalyse universelle

À insérer à la suite du complément 2.

La stéganalyse universelle, ou aveugle, cherche à détecter la présence d'un message sans connaître
l'algorithme d'insertion. Elle repose sur l'extraction d'un très grand nombre de caractéristiques, ce qui
rend l'apprentissage coûteux et empêche l'usage de certains algorithmes. Réduire ce nombre, sans perdre le
pouvoir discriminant, est donc un enjeu majeur.

Deux familles de méthodes existent. La réduction par extraction, comme l'analyse en composantes
principales, construit de nouvelles variables combinant les caractéristiques d'origine, au prix de leur
interprétabilité. La sélection de caractéristiques, au contraire, conserve un sous-ensemble des variables
originales. L'analyse en caractéristiques principales, ou PFA, proposée par Lu, Plataniotis et
Venetsanopoulos [36], relève de cette seconde famille : elle regroupe les caractéristiques selon leur
structure de covariance et retient, dans chaque groupe, la plus représentative.

Cette approche a été appliquée à la stéganalyse universelle par [37], qui propose de sélectionner par PFA
le sous-ensemble de caractéristiques offrant la meilleure séparation, puis d'entraîner un classifieur
binaire cover contre stégo sur ce sous-ensemble réduit. L'intérêt est double : rendre l'apprentissage
abordable sans ressources de calcul importantes, et conserver des caractéristiques interprétables. Ce
mémoire mobilise cette approche pour rendre exploitables les caractéristiques riches, dont le coût est
autrement prohibitif, et l'intègre à sa démarche de détection face au contenu généré.

---

## Références ajoutées

[28] A. Westfeld, A. Pfitzmann, "Attacks on Steganographic Systems", Information Hiding, 1999.

[29] T. Pevný, P. Bas, J. Fridrich, "Steganalysis by Subtractive Pixel Adjacency Matrix", IEEE Trans.
Information Forensics and Security, 2010.

[30] J. Kodovský, J. Fridrich, V. Holub, "Ensemble Classifiers for Steganalysis of Digital Media", IEEE
Trans. Information Forensics and Security, 2012.

[31] Cover-source mismatch in steganalysis : systematic review, EURASIP Journal on Information Security,
2024.

[32] Tackling the Cover-Source Mismatch Problem in Audio Steganalysis With Unsupervised Domain Adaptation,
IEEE, 2020.

[33] Multi-source Domain Adaptation Image Steganalysis for Cover Source Mismatch.

[34] Manifold Alignment Approach to Cover Source Mismatch in Steganalysis.

[35] FADG : Frequency-Aware Adaptive Domain Generation for Cover Source Mismatch in Steganalysis.

[36] Y. Lu, I. Cohen, X. S. Zhou, Q. Tian, "Feature Selection Using Principal Feature Analysis", ACM
Multimedia, 2007.

[37] Article de l'encadrant, "Feature Reduction Algorithm for Universal Steganalysis".
