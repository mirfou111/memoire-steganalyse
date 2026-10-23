% Stéganographie et stéganalyse face aux contenus générés par intelligence artificielle
% Ousmane Ndiéguène
% Mémoire de Master

# Introduction générale

## Contexte et enjeux

En 2014, une variante du cheval de Troie bancaire Zeus, dénommée ZeusVM, a caché la liste des banques qu'elle
visait dans une image ordinaire. Les antivirus n'y ont vu qu'une photo, alors que les instructions, elles,
étaient bien présentes [49]. Cette technique relève de la stéganographie, la discipline qui consiste à cacher
un message, ou plus largement des données, dans un support anodin comme un fichier image [2]. Elle peut être
confondue avec le chiffrement, mais là où ce dernier rend le message illisible, la stéganographie, elle, cache
l'existence même du message.

Le cas de Zeus n'est pas isolé. D'autres familles de logiciels malveillants ont eu recours à cette technique,
notamment Duqu, qui exfiltre des données en les cachant dans des images [50], ou encore Stegoloader, qui
utilise la stéganographie numérique pour dissimuler le code de son module principal dans une image PNG
téléchargée depuis un site web légitime [51]. Ces méthodes sont aussi dangereuses que sophistiquées, d'où la
nécessité de disposer de techniques pour les détecter. C'est le rôle de la stéganalyse, la discipline qui
cherche à repérer ce qui a été caché.

Plus la stéganographie évolue, plus la stéganalyse doit se réinventer, exactement comme la cryptanalyse pousse
la cryptographie à se renforcer. Si la stéganalyse prend du retard, des systèmes d'information critiques
risquent de subir des attaques, comme dans le cas de Zeus. Les conséquences vont alors de la fraude bancaire à
la fuite massive de données sensibles.

Seulement, un changement récent vient rebattre les cartes. Les images produites par l'intelligence
artificielle sont partout et offrent un nouvel endroit où cacher un message. Mais leur nature, différente de
celle des images naturelles, complique encore la détection, car les outils de stéganalyse ont été entraînés à
repérer des données cachées dans de vraies photos.

## Problématique

D'où la question qui guide ce travail. La stéganalyse classique, pensée et calibrée pour des images
naturelles, sait-elle encore repérer un message caché lorsque le support est une image générée ? Et
lorsqu'elle échoue, quelle en serait la cause ?

Deux raisons rendent ces questions légitimes. La première tient au changement de source : un détecteur
entraîné sur un type d'images peut se tromper sur un autre. Cela est prouvé et documenté sur différentes
sources naturelles [31]. La seconde tient à l'image elle-même : les traces laissées par la génération
pourraient se mêler à celles de l'insertion, au point de les masquer. Or ce sont justement ces traces
d'insertion qu'exploitent les algorithmes de détection en stéganalyse. Caractériser ces deux effets, les
mesurer, et voir si l'on peut les corriger, voilà le fil de ce mémoire.

## Contributions

Pour répondre à ces questions, il a d'abord fallu préparer des données pour l'étude. C'est le premier apport
de ce travail : un corpus contrôlé, pensé pour l'image générée. Quatre sources d'images, une naturelle et
trois produites par des IA, dont une commerciale, dix mille images chacune, toutes passées par le même
processus. Même prétraitement, même format, mêmes algorithmes d'insertion, et pour chaque image sa version
vierge comme ses versions porteuses d'un message caché. De quoi comparer et isoler ce qui vient vraiment du
générateur. Ce jeu de données pourrait servir au-delà de ce mémoire.

Le second apport est ce que ce terrain a permis de montrer. Les deux difficultés, le changement de source et
l'interférence, ne sont pas seulement décrites : elles sont mesurées, chiffres à l'appui. Nous montrons où le
détecteur se trompe, pourquoi, et jusqu'où il est possible de le remettre d'aplomb. Rien là-dedans n'invente
d'images ni de nouvelle méthode de détection. L'apport est ailleurs, dans le cadre comparable et dans la mise
en évidence, encore rare, de ces phénomènes sur des images d'IA.

## Organisation du mémoire

Nous avons organisé le travail en deux parties.

La première fait l'état des lieux de ce que l'on sait déjà. Elle part des bases, avec un premier chapitre
consacré à la façon de cacher un message dans une image et à celle de le repérer, des premiers tests
statistiques jusqu'aux modèles riches comme SRM, sans oublier les mesures qui permettent de juger un
détecteur. Ces bases posées, le chapitre 2 se tourne vers les images générées. Il décrit les grandes familles
de générateurs et les traces que chacune laisse dans ce qu'elle produit. Le chapitre 3 rapproche les deux
mondes en examinant les différentes manières de cacher de l'information dans ce nouveau contenu, des méthodes
classiques au tatouage que certains générateurs intègrent eux-mêmes. Reste alors à savoir où en est la
détection. Le chapitre 4 fait le bilan du travail déjà abattu sur ce chantier, de ce qui fonctionne aux points
où les détecteurs cèdent. Le chapitre 5 en tire les leçons, relève ce qui manque encore et situe notre travail
dans ce paysage.

La seconde partie passe à la pratique. Le chapitre 6 décrit la méthode, de la constitution du corpus jusqu'au
protocole d'évaluation. Les chapitres 7 et 8 forment le cœur du travail. Le premier met en évidence les deux
difficultés, le changement de source puis l'interférence. Le second teste une manière de les atténuer, et
montre ce qu'elle répare comme ce qu'elle laisse de côté. Le chapitre 9 s'aventure ensuite sur une piste plus
exploratoire, qui consiste à reconnaître l'algorithme employé et non plus seulement la présence d'un message.
Enfin, le chapitre 10 prend du recul sur l'ensemble des résultats, leurs limites et les suites possibles.

Une conclusion générale referme le mémoire en rappelant les apports et en répondant à la question posée en
introduction.

# Partie I : État de l'art

Avant de mesurer quoi que ce soit, il faut savoir d'où l'on part. Cette première partie rassemble ce que la
littérature établit sur les deux domaines qui se croisent dans ce mémoire, la stéganographie et la stéganalyse
d'un côté, la génération d'images par intelligence artificielle de l'autre. Le chemin va du plus ancien au
plus récent. Il commence par les principes et les outils classiques, passe par les générateurs et leurs
traces, puis arrive aux travaux qui confrontent les deux. Il se termine par un bilan qui fait apparaître ce
qui manque encore, et c'est dans ce manque que s'inscrit la partie pratique.

## 1. Fondements de la stéganographie et de la stéganalyse

### 1.1 Principes de la stéganographie

#### 1.1.1 Définition et vocabulaire

Comme nous l'avons évoqué dans l'introduction, la stéganographie est la science qui consiste à transmettre des
données secrètes au sein d'un support multimédia approprié. Elle repose sur le principe selon lequel, si
l'élément est visible, le point d'attaque est évident ; l'objectif est donc toujours de dissimuler l'existence
même des données intégrées. Dans notre cas, les supports étudiés sont les fichiers image, mais les données
secrètes peuvent aussi être embarquées dans des fichiers audio, vidéo ou texte [52].

Jusque-là, nous avons utilisé des appellations communes comme image, message caché ou support. Mais comme dans
toute discipline, la stéganographie a son propre lexique. On parle de médium de couverture, ou « cover », pour
désigner le fichier, image, vidéo, audio ou texte, destiné à contenir le message à cacher, lui-même appelé
payload, ou charge utile. Une fois le message inséré, ce même fichier devient le stégo-objet, ou stego. Tout
l'enjeu de la stéganographie réside dans la quasi-impossibilité de distinguer le cover du stego [2].

#### 1.1.2 Charge utile et compromis

Dans un média donné, il existe une quantité maximale de données secrètes, en bits ou en octets, qu'il est
possible de dissimuler sans éveiller les soupçons. On appelle cette quantité la payload capacity, ou capacité
de charge utile.

Dans le cas des images, cette capacité se mesure le plus souvent en bits par pixel, le bpp. Un bpp de 0,4,
par exemple, veut dire qu'on cache en moyenne quatre dixièmes de bit dans chaque pixel. Plus ce chiffre monte,
plus on transporte de données.

Mais tout se paie. Chaque bit inséré modifie légèrement l'image, et ces petites retouches s'accumulent. À
faible charge, elles restent noyées dans le bruit naturel du support. À forte charge, elles finissent par
laisser une trace repérable. Il y a donc un compromis permanent entre la quantité que l'on veut cacher et la
discrétion que l'on cherche à garder [2].

#### 1.1.3 L'insertion naïve : le LSB

Historiquement, cacher un message n'a rien de nouveau. Dans l'Antiquité, Hérodote rapporte déjà le cas d'un
maître qui rase la tête d'un esclave, y tatoue un message, puis attend que les cheveux repoussent avant de
l'envoyer. D'autres gravaient un texte sous la cire d'une tablette, ou écrivaient à l'encre invisible. Plus
tard, pendant les guerres mondiales, on réduisait des pages entières à la taille d'un point, le micropoint. Le
mot lui-même vient du grec steganos, couvert, et graphein, écrire [52].

Avec le numérique, on assiste à un changement de support, mais l'idée reste la même. L'image remplace la
tablette de cire, et l'insertion se joue désormais sur les bits qui composent chaque pixel. La plus simple est
la méthode LSB, pour least significant bit, c'est-à-dire le bit de poids faible.

Pour comprendre son fonctionnement, il faut voir comment une image est stockée. Dans la machine, elle prend la
forme d'une matrice de pixels, et chaque pixel porte une valeur qui fixe son intensité, du noir au blanc. Une
image en couleur en compte trois par pixel, une pour chacun des canaux rouge, vert et bleu, dont le mélange
donne la teinte affichée.

Ces valeurs ne se répartissent pas au hasard. Dans une zone lisse, comme un ciel dégagé, les pixels voisins
ont des valeurs presque identiques. Dans une zone texturée, comme un feuillage ou une chevelure, et le long
des contours, elles varient fortement d'un pixel à l'autre. À cela s'ajoute le bruit : de petites fluctuations
aléatoires, dues notamment au capteur de l'appareil, qui touchent toute l'image [2]. Ces notions comptent pour
la suite. Une modification invisible à l'œil reste une perturbation de ce bruit, et c'est justement là que la
stéganographie cherche à se cacher, et que la stéganalyse cherche à la débusquer.

Dans ce travail, nous nous intéressons aux images en niveaux de gris, qui ne gardent qu'une seule valeur par
pixel, comme celles de la base BOSSbase [48]. Cette valeur est un nombre entier, souvent compris entre 0 et
255, codé sur huit bits. Le dernier de ces bits, le moins significatif, ne change presque rien à l'intensité
du pixel quand on le modifie. L'idée du LSB est donc de remplacer ce bit par un bit du message à cacher. Dans
une version plus prudente, le LSB matching, on n'écrase pas le bit : on ajoute ou on retire une unité au
hasard pour tomber sur la bonne valeur, ce qui évite certaines traces faciles à repérer [39]. Simple et
efficace, le LSB a pourtant un défaut. Il répartit les modifications sans tenir compte du contenu de l'image,
ce qui le rend vulnérable à la détection.

#### 1.1.4 L'insertion adaptative

Pour corriger ce défaut, il a fallu inventer des méthodes plus sournoises : les algorithmes d'insertion
adaptative. Leur principe est le suivant : plutôt que de modifier les pixels au hasard, on choisit où insérer.
L'idée est de toucher en priorité les endroits où une modification se remarque le moins, comme les zones
texturées, les contours ou les régions bruitées, et d'épargner les zones lisses, où le moindre changement
saute aux yeux d'un détecteur.

En pratique, chaque pixel reçoit un coût qui traduit le risque de laisser une trace si on le modifie. Plus ce
coût est faible, plus le pixel se prête à recevoir une partie du message sans éveiller de soupçon.
L'algorithme répartit alors le message de façon à payer le moins de coût possible. Plusieurs méthodes ont
affiné cette idée. HUGO a été l'un des premiers à minimiser la distorsion dans un espace de caractéristiques
de grande dimension [1]. WOW s'appuie sur des filtres directionnels pour viser les textures complexes [3].
S-UNIWARD a proposé une fonction de coût applicable à plusieurs domaines, devenue une référence [20]. HILL
combine plusieurs filtres pour concentrer encore davantage les changements dans les zones difficiles [38].

Ces algorithmes forment le standard actuel de l'insertion. Bien plus discrets que le LSB, ils sont pensés pour
résister aux détecteurs, et c'est justement ce qui rend leur détection si ardue. Comment, alors, repérer une
insertion aussi bien dissimulée ? C'est tout l'objet de la stéganalyse.

### 1.2 Stéganalyse classique : SRM et approches statistiques

Cette image, ou plus généralement ce média, contient-il un message caché ? Voilà la question qui guide la
stéganalyse. Pour rappel, une technique de stéganographie ne tient que tant qu'on ignore que le média porte un
message. Dès que le média devient suspect, elle a déjà échoué. La stéganalyse ne cherche donc pas forcément à
lire le payload, seulement à le repérer. Pour cela, deux approches se distinguent. La première, la stéganalyse
ciblée, vise un algorithme de stéganographie précis, dont elle connaît déjà les faiblesses. La seconde, la
stéganalyse universelle, dite aveugle, cherche au contraire à détecter une insertion sans savoir comment elle
a été faite [2].

#### 1.2.1 Les premières méthodes : les tests statistiques

Les premières méthodes reposaient sur des tests statistiques directs, sans apprentissage. Elles regardent
l'image non comme un dessin, mais comme une collection de nombres dont on étudie la répartition. L'outil le
plus simple est l'histogramme, qui compte combien de pixels prennent chaque valeur, de 0 à 255. Dans une image
naturelle, deux valeurs voisines comme 154 et 155 apparaissent avec des fréquences proches mais différentes,
sans lien particulier entre elles [2].

La substitution LSB vient troubler cet équilibre. En remplaçant le dernier bit, elle fait passer des pixels de
154 à 155, et inversement, en fonction du message à insérer. Plus la charge augmente, plus les effectifs de
chaque paire de valeurs se rapprochent. L'attaque du chi-deux, proposée par Westfeld et Pfitzmann, exploite
exactement cet effet : elle mesure à quel point ces paires s'égalisent, ce qu'une image naturelle ne fait pas
[28]. C'est un exemple typique de stéganalyse ciblée : redoutable contre le LSB naïf, elle perd en efficacité
face au LSB matching et aux méthodes adaptatives, qui ne laissent pas de trace de cette nature.

#### 1.2.2 Le passage à l'apprentissage : SPAM

Pour contrer le LSB matching, et plus largement les insertions qui ajoutent à l'image un faible signal
semblable à du bruit, la stéganalyse a changé d'approche. Plutôt que de chercher une trace précise, on résume
maintenant chaque image par un ensemble de mesures, appelées caractéristiques, puis on confie à un algorithme
d'apprentissage la tâche de séparer les images vierges des images porteuses. Il suffit de lui montrer des
exemples des deux types : il trouve seul la frontière. C'est l'entrée dans la stéganalyse universelle : le
même principe est utilisé quel que soit l'algorithme d'insertion, pourvu qu'on dispose d'exemples.

Ces caractéristiques ne portent pas sur le contenu de l'image, mais sur son bruit. L'insertion modifie des
détails infimes, invisibles à l'œil nu, et c'est dans les relations entre pixels voisins qu'elle se trahit. Le
descripteur SPAM, proposé par Pevný, Bas et Fridrich, en est un bon exemple : il observe comment la différence
entre deux pixels voisins évolue d'un pixel au suivant, et résume ce comportement en 686 valeurs [29]. Associé
à une machine à vecteurs de support, ou SVM, il a longtemps servi de référence en stéganalyse. Mais face aux
algorithmes adaptatifs, des caractéristiques aussi simples ne suffisent plus.

#### 1.2.3 Les modèles riches : SRM

Pourquoi SPAM ne suffit-il plus ? Ses 686 caractéristiques ne regardent qu'une seule chose : la manière dont
les différences entre pixels voisins s'enchaînent. Et pour rester de taille raisonnable, il écrête ces
différences : au-delà d'un petit seuil, toutes les grandes valeurs tombent dans la même case [29]. Or c'est
justement dans les zones texturées, là où les différences sont grandes, que les algorithmes adaptatifs placent
leurs modifications. SPAM ne permet donc pas de détecter de façon fiable une insertion faite avec ces
algorithmes.

Il y a plus gênant encore. Les algorithmes adaptatifs ont été conçus en connaissant ce type de mesure. HUGO,
par exemple, choisit ses modifications de façon à perturber le moins possible des statistiques de voisinage
proches de celles de SPAM [1]. Le détecteur se retrouve face à une insertion conçue exprès pour lui échapper.

Ainsi fallait-il trouver un moyen de resserrer les mailles du filet. C'est ce qui a donné naissance aux
modèles riches, proposés par Fridrich et Kodovský en 2012. Au lieu de ne regarder qu'un seul type de mesure,
on en combine plusieurs, chacune d'entre elles étant sensible à une forme différente de dépendance entre
pixels voisins [4].

Le principe exploite toujours le bruit. On commence par prédire chaque pixel à partir de ses voisins, à l'aide
de nombreux filtres, puis on garde l'écart entre la valeur réelle et la prédiction. Cet écart, appelé résidu,
efface en grande partie le contenu de l'image et fait ressortir le bruit, là où l'insertion se cache. On
compte ensuite, sur de petits groupes de résidus voisins, quelles combinaisons de valeurs reviennent le plus
souvent. Le modèle complet, appelé SRM pour Spatial Rich Model, aboutit ainsi à 34 671 caractéristiques par
image [4]. C'est ce descripteur qui sert dans la partie pratique de ce mémoire.

L'intérêt de cette richesse est simple. Un algorithme adaptatif peut éviter de perturber une statistique
donnée, mais il lui est très difficile d'en épargner des milliers à la fois. Le seul bémol, c'est la dimension
: avec plus de trente mille valeurs à extraire par image, SRM est très gourmand en puissance de calcul. De
plus, un classifieur comme la SVM devient lent et risque de mal apprendre. D'où la question de l'outil de
décision à employer.

#### 1.2.4 L'outil de décision : l'ensemble de classifieurs

Avec SRM, le problème a changé de nature. Il ne s'agit plus seulement de trouver les bonnes mesures, mais de
savoir quoi en faire. Face à plus de trente mille caractéristiques, et souvent moins d'images que cela pour
apprendre, la SVM, qui servait de référence jusque-là, devient trop lente à entraîner.

Kodovský, Fridrich et Holub ont proposé en 2012 une réponse simple dans son principe [30]. Plutôt qu'un seul
classifieur puissant, on en entraîne un grand nombre de très simples. Chacun est un discriminant linéaire de
Fisher, ou FLD, qui ne regarde qu'un petit sous-ensemble de caractéristiques tirées au hasard. Pris seul, il
se trompe souvent. Une fois leurs votes réunis, en revanche, la décision collective devient fiable, et
l'apprentissage reste rapide même quand les caractéristiques sont bien plus nombreuses que les exemples [30].
Ce couple, modèles riches et ensemble de FLD, est depuis devenu la référence de la stéganalyse classique.

Une autre manière de dompter la dimension consiste à réduire le nombre de caractéristiques avant d'apprendre.
On peut construire de nouvelles variables qui résument les anciennes, comme le fait l'analyse en composantes
principales, mais on perd alors le sens de chaque mesure. On peut aussi n'en garder qu'une partie. C'est le
principe de l'analyse en caractéristiques principales, ou PFA, qui regroupe les caractéristiques porteuses
d'une information voisine et retient la plus représentative de chaque groupe [36]. Gomis, Camara et Diop ont
appliqué cette idée à la stéganalyse universelle, pour rendre l'apprentissage abordable sans grands moyens de
calcul tout en conservant des caractéristiques lisibles [37]. La partie pratique explore cette voie aux côtés
de l'analyse en composantes principales, avec un classifieur linéaire plus simple encore, la régression
logistique.

#### 1.2.5 Vers l'apprentissage profond

Depuis le milieu des années 2010, une autre voie s'est imposée. Les réseaux de neurones convolutifs apprennent
eux-mêmes, à partir des images, à la fois les caractéristiques et la décision. SRNet, proposé par Boroumand,
Chen et Fridrich, en est un exemple marquant [5]. Il se passe des filtres fixés à la main que l'on plaçait
jusque-là en entrée des réseaux, et laisse l'apprentissage découvrir les résidus utiles. Ses performances
dépassent celles des modèles riches dans les comparaisons publiées [5].

Ce gain a un prix. Un tel réseau demande beaucoup d'images et de puissance de calcul, et il reste difficile de
dire ce qu'il a appris. Pour un travail qui cherche à comprendre pourquoi un détecteur se trompe, cette
opacité pèse lourd. Nous revenons sur ce choix au chapitre 6.

### 1.3 Métriques d'évaluation

Un détecteur peut se tromper de deux façons. Il peut voir un message là où il n'y en a pas, ce qu'on appelle
une fausse alarme ou un faux positif. Il peut aussi laisser passer une image porteuse sans rien signaler, et
l'on parle alors de détection manquée. Les deux erreurs n'ont pas le même poids. En situation réelle, où les
images innocentes sont de loin les plus nombreuses, un taux de faux positifs même modeste noie l'analyste sous
les fausses alertes.

La plupart des détecteurs ne répondent pas par oui ou par non, mais par un score. C'est le seuil choisi qui
transforme ce score en décision, et chaque seuil donne un compromis différent entre les deux erreurs. La
courbe ROC trace ce compromis pour tous les seuils possibles, en mettant en regard le taux de vrais positifs
et le taux de faux positifs. L'aire sous cette courbe, l'AUC, résume la qualité du détecteur en un seul
nombre. Elle vaut 1 pour un détecteur parfait et 0,5 pour un détecteur qui répond au hasard. En stéganalyse,
on rencontre aussi la probabilité d'erreur minimale, notée P_E, qui fait la moyenne des deux erreurs au
meilleur seuil [30].

Ces chiffres n'ont de sens qu'à conditions égales. La difficulté de détection dépend fortement de la charge
insérée, d'où l'habitude de la mesurer en bits par pixel et de comparer les méthodes à charge identique,
souvent 0,4 bpp. Elle dépend aussi des images elles-mêmes. C'est pour cette raison que la communauté s'est
dotée de bases de référence comme BOSSbase, issue du concours BOSS [48], qui permettent de comparer les
travaux entre eux. Dans ce mémoire, l'AUC sert de mesure principale. Nous la complétons par le taux de faux
positifs, qui rend mieux compte de ce qui se passe lorsqu'un détecteur change de source.

## 2. Contenu généré par IA : techniques et artefacts

Le chapitre précédent supposait, sans le dire, que les images venaient d'un appareil photo. Ce n'est plus
toujours vrai. Une part croissante des images qui circulent aujourd'hui est produite par des modèles
génératifs, et chacun de ces modèles fabrique ses images à sa manière. Ce chapitre présente les principales
familles et, surtout, les traces qu'elles laissent, car ce sont ces traces qui intéressent la stéganalyse.

### 2.1 GANs et leur signature fréquentielle

Les réseaux antagonistes génératifs, ou GAN, ont été proposés par Goodfellow et ses collègues en 2014 [6].
L'idée repose sur un duel entre deux réseaux. Le premier, le générateur, fabrique des images à partir d'un
bruit aléatoire. Le second, le discriminateur, reçoit tantôt une vraie image, tantôt une image fabriquée, et
doit dire laquelle est laquelle. Chacun progresse au contact de l'autre, jusqu'à ce que le discriminateur ne
parvienne plus à faire la différence [6]. Des versions successives, comme ProGAN, qui fait grandir l'image par
étapes [8], puis StyleGAN [7], ont amené ces images à un réalisme frappant.

Réaliste à l'œil ne veut pourtant pas dire identique à une photo. Pour obtenir une grande image à partir d'une
petite représentation, le générateur l'agrandit couche après couche. Cette opération de suréchantillonnage
laisse des motifs réguliers, invisibles dans l'image mais très nets dans son spectre de fréquences, où ils
apparaissent comme des pics répétés [9], [47]. D'autres travaux observent que les images générées se
distinguent aussi des photos par leur contenu en hautes fréquences [10].

Ces traces sont assez stables pour servir d'empreinte. Marra et ses collègues ont montré que chaque GAN laisse
dans ses images une signature qui lui est propre, un peu comme le capteur d'un appareil photo marque chaque
cliché de son bruit particulier [12]. On peut ainsi, dans une certaine mesure, retrouver quel générateur a
produit une image.

### 2.2 VAEs et leurs propriétés statistiques

Les auto-encodeurs variationnels, ou VAE, suivent une autre logique [11]. Un premier réseau, l'encodeur,
compresse l'image en une représentation réduite, appelée espace latent. Un second, le décodeur, reconstruit
l'image à partir de cette représentation. Comme l'espace latent est contraint à garder une forme régulière, on
peut ensuite y tirer des points au hasard et les décoder pour obtenir des images nouvelles [11].

Utilisés seuls, les VAE ont la réputation de produire des images plus floues que les GAN, la reconstruction
ayant tendance à lisser les détails fins. Leur intérêt pour nous est ailleurs. Leur principe de compression a
été repris au cœur des modèles de diffusion latente, dont Stable Diffusion, où un auto-encodeur fait le
passage entre l'image et l'espace dans lequel le modèle travaille [43]. Toute image produite par ces modèles
passe donc par un décodeur, et en porte la marque. Corvi et ses collègues relèvent d'ailleurs des artefacts
dans le domaine de Fourier aussi bien pour des modèles de diffusion que pour des modèles à espace latent comme
VQ-GAN [14].

### 2.3 Modèles de diffusion et résidus de débruitage

Les modèles de diffusion ont pris le relais des GAN à partir de 2020. Leur principe tient en deux mouvements.
Pendant l'apprentissage, on abîme progressivement des images en leur ajoutant du bruit, étape après étape,
jusqu'à ce qu'il ne reste plus que du bruit. Le modèle apprend à défaire ce chemin, c'est-à-dire à retirer un
peu de bruit à chaque étape [13]. Pour créer une image, il suffit alors de partir d'un bruit pur et de le
débruiter pas à pas.

Deux variantes nous intéressent directement, parce qu'elles figurent dans notre corpus. La première travaille
dans l'espace des pixels. C'est le cas d'ADM, qui a montré en 2021 que la diffusion pouvait dépasser les GAN
en qualité d'image [44]. La seconde, la diffusion latente, travaille dans l'espace compressé d'un
auto-encodeur, ce qui réduit fortement le coût de calcul [43]. C'est le principe de Stable Diffusion.
Midjourney, service commercial dont le fonctionnement interne n'est pas publié, complète ce panorama.

Les traces de la diffusion sont plus discrètes que celles des GAN, mais elles existent. Corvi et ses collègues
observent, pour ces modèles aussi, des motifs dans le domaine de Fourier et des écarts avec les photos dans
les moyennes et hautes fréquences [14]. Or c'est précisément dans cette zone, celle des détails fins et du
bruit, que la stéganographie cache ses messages et que la stéganalyse les cherche.

### 2.4 Modèles de langue et perplexité

Les images ne sont pas seules en cause. Les modèles de langue, comme GPT-3, produisent du texte en prédisant
le mot suivant à partir de ceux qui précèdent [16]. Ce mode de production laisse lui aussi une trace
statistique. Un texte généré a tendance à suivre les choix les plus probables du modèle, ce qui se mesure par
la perplexité, autrement dit la surprise du modèle face au texte. Des détecteurs s'appuient sur cette
propriété, comme DetectGPT, qui examine comment la probabilité d'un texte varie quand on le modifie légèrement
[17], ou Binoculars, qui compare les réactions de deux modèles proches [18].

Nous ne traitons pas le texte dans la partie pratique. Ce détour montre toutefois une chose utile. Quel que
soit le média, la génération automatique laisse une signature statistique, et c'est sur ce type de signature
que repose toute détection.

## 3. Stéganographie dans le contenu généré par IA

Une image générée peut porter de l'information cachée de plusieurs façons. On peut lui appliquer les méthodes
classiques, comme à n'importe quelle photo. On peut aussi confier l'insertion à un réseau de neurones.
Certains générateurs, enfin, marquent eux-mêmes leurs images. Ces trois cas ne posent pas le même problème.

### 3.1 Stéganographie classique appliquée aux images générées

Rien n'empêche d'utiliser une image générée comme support. Pour un algorithme comme S-UNIWARD ou HILL, une
image reste un tableau de pixels, quelle que soit son origine. Et à mesure que ces images se répandent sur les
réseaux, elles deviennent des couvertures tout à fait plausibles, qui n'attirent pas plus l'attention qu'une
photo de vacances.

Reste à savoir ce que devient alors la détection. Deux effets peuvent jouer. Le premier est connu. Un
détecteur entraîné sur une source d'images se trompe davantage sur une autre, et ce phénomène, le cover-source
mismatch, est étudié depuis une vingtaine d'années pour des sources naturelles différentes [31]. Le second est
plus propre aux images générées. Leurs traces vivent dans les mêmes fréquences que celles de l'insertion, si
bien qu'elles pourraient s'y mêler au point de la masquer. C'est ce que nous appelons l'interférence.

À notre connaissance, peu de travaux étudient ces deux effets ensemble, sur des images générées et avec des
algorithmes d'insertion classiques. C'est l'un des points de départ de ce mémoire.

### 3.2 Stéganographie apprise

Une autre voie consiste à confier l'insertion à un réseau de neurones. Dans HiDDeN, un réseau encodeur cache
le message dans l'image, un réseau décodeur le récupère, et des couches de bruit placées entre les deux
simulent les dégradations que l'image peut subir, comme la compression JPEG [21]. Ces réseaux apprennent
ensemble, de sorte que le message résiste à ces dégradations. SteganoGAN reprend une architecture proche, avec
un réseau critique chargé de rendre l'image porteuse indiscernable d'une image normale, et vise une capacité
élevée, jusqu'à 4,4 bits par pixel [22].

Ces méthodes changent la nature du problème. L'insertion n'obéit plus à une règle connue, comme le LSB ou les
coûts de HILL, mais à ce qu'un réseau a appris. Elles sortent du cadre de notre partie pratique, qui s'en
tient aux algorithmes classiques. Elles montrent cependant que la frontière entre image générée et image
porteuse devient de plus en plus floue.

### 3.3 Watermarking natif

Le tatouage numérique, ou watermarking, cache lui aussi de l'information dans une image, mais dans un autre
but. La stéganographie veut que personne ne soupçonne la présence d'un message. Le tatouage, lui, ne cherche
pas à se faire oublier. Il doit surtout résister aux modifications, pour que l'on puisse toujours retrouver
l'origine de l'image. Avec la multiplication des images générées, plusieurs acteurs ont intégré un tel
tatouage directement dans leurs générateurs.

Tree-Ring agit dès le début de la génération. Le bruit de départ, d'où naît l'image dans un modèle de
diffusion, reçoit dans son spectre de Fourier un motif en anneaux. Pour vérifier une image, on remonte le
processus de génération jusqu'à retrouver ce bruit, puis on y cherche le motif [23]. Stable Signature procède
autrement. Il modifie le décodeur d'un modèle de diffusion latente pour que toutes les images qu'il produit
portent une signature, qu'un réseau dédié sait ensuite extraire [24]. SynthID, développé par Google DeepMind,
est quant à lui déployé à grande échelle dans les services de l'entreprise, avec plus de dix milliards
d'images et d'images de vidéos marquées selon ses auteurs [26]. Le principe existe aussi pour le texte, où le
modèle favorise discrètement certains mots selon une règle secrète [25].

Quel que soit leur mécanisme, ces tatouages modifient l'image d'une façon qu'aucune photo ne connaît. Pour la
stéganalyse, ils représentent donc une trace de plus, voulue cette fois, qui s'ajoute à celles de la
génération.

## 4. Stéganalyse face au contenu généré par IA

Face à ces images, que sait-on détecter ? Ce chapitre fait le bilan du travail déjà abattu, en partant des
détecteurs de stéganalyse classiques, puis en passant par la forensique des images générées et la vérification
des tatouages. Il s'achève sur les pistes que la recherche commence à explorer.

### 4.1 Limites des détecteurs classiques

Un détecteur de stéganalyse n'apprend pas seulement à reconnaître la trace d'une insertion. Il apprend aussi,
sans qu'on le lui demande, les habitudes statistiques des images qui ont servi à son entraînement. Tant que
les images à analyser leur ressemblent, tout va bien. Dès qu'elles s'en écartent, il peut confondre ce qui
relève de la source et ce qui relève du message.

La revue de Mallet, Beneš et Cogranne fait le point sur vingt ans de recherche autour de ce problème [31].
Elle en recense les causes connues, liées à la façon dont les images ont été acquises puis traitées, et
souligne que le phénomène reste souvent négligé, alors qu'il pèse lourd dès qu'on sort du laboratoire [31].
Les images générées poussent cette logique plus loin. Elles ne viennent d'aucun capteur, et leur bruit est le
produit d'un réseau. L'écart avec les images d'entraînement risque donc d'être bien plus grand qu'entre deux
appareils photo.

### 4.2 Forensique IA

Une autre communauté s'est emparée des images générées, avec une question différente. La forensique ne cherche
pas un message caché. Elle veut savoir si une image a été produite par une machine.

Wang et ses collègues ont montré qu'un détecteur entraîné sur les images d'un seul GAN, ProGAN, pouvait
reconnaître celles d'autres générateurs à base de réseaux convolutifs, à condition d'avoir été entraîné avec
des images volontairement floutées ou compressées [45]. D'autres travaux exploitent le spectre de fréquences,
où les artefacts de suréchantillonnage ressortent nettement [47]. L'arrivée de la diffusion a remis ces acquis
en question. Les détecteurs pensés pour les GAN peinent face à ces nouveaux modèles, ce qui a conduit à de
nouvelles approches [46]. DIRE, par exemple, mesure l'écart entre une image et sa reconstruction par un modèle
de diffusion [46], tandis que DE-FAKE s'appuie aussi sur le texte qui a servi à générer l'image [15]. Des
bases à grande échelle comme GenImage permettent aujourd'hui de tester la capacité de ces détecteurs à passer
d'un générateur à l'autre [41].

Ces travaux nous sont précieux, car ils décrivent précisément les traces que nous retrouvons en face. Mais ils
répondent à une autre question. Savoir qu'une image est générée ne dit rien de la présence d'un message à
l'intérieur.

### 4.3 Vérification de watermark et ses limites

Le tatouage offre une voie plus directe. Si le générateur a marqué ses images, il suffit d'y chercher la
marque. Cette solution a toutefois des limites claires.

Elle suppose d'abord la coopération du fournisseur. Seuls les générateurs qui tatouent leurs images peuvent
être vérifiés, et la vérification passe par la clé ou le détecteur de celui qui a posé la marque, comme pour
Tree-Ring [23]. Le service de vérification de SynthID, par exemple, n'est ouvert qu'à des testeurs de
confiance [26]. Un modèle libre, que chacun peut faire tourner chez soi, échappe à ce contrôle. La marque peut
ensuite être effacée. Zhao et ses collègues montrent qu'il suffit d'ajouter du bruit à une image puis de la
reconstruire, par exemple avec un modèle de diffusion, pour faire disparaître de façon prouvable les tatouages
qui agissent au niveau des pixels [27].

Surtout, la vérification d'un tatouage dit d'où vient l'image, pas ce qu'elle transporte. Une image tatouée
par son générateur peut très bien porter, en plus, un message caché par un tiers. Le problème de la
stéganalyse reste entier.

### 4.4 Pistes émergentes

Puisque le problème vient d'un écart entre les images d'entraînement et celles que l'on analyse, une piste
naturelle consiste à réduire cet écart. C'est l'objet de l'adaptation de domaine, une branche de
l'apprentissage par transfert, qui cherche à faire profiter un modèle de ce qu'il a appris sur une source pour
l'appliquer à une autre [19].

En stéganalyse, plusieurs travaux suivent cette voie face au cover-source mismatch. Certains se passent de
base d'entraînement préalable et construisent leurs exemples à partir des images mêmes que l'on analyse [32].
D'autres montrent qu'ajouter à l'entraînement un petit nombre d'images issues de la source visée suffit à
réduire nettement l'effet du changement de source [33]. D'autres encore projettent les données dans un espace
commun [34], ou transforment les images d'entraînement pour qu'elles ressemblent à celles de la source visée
[35]. Le principe reste le même. On réintroduit dans le détecteur une connaissance de la source à analyser, au
lieu de faire comme s'il n'en existait qu'une.

Une idée voisine consiste à séparer, dans ce que voit le détecteur, la part qui vient de la source et celle
qui vient du message. Si l'on parvenait à démêler ces deux traces, la signature du générateur cesserait de
gêner la détection. Cette piste reste largement ouverte pour les images générées, d'autant que les travaux
cités portent pour l'essentiel sur des sources naturelles.

## 5. Synthèse critique et positionnement

Ce tour d'horizon fait apparaître un paysage contrasté. La stéganalyse classique est mûre. Des modèles riches
aux réseaux profonds, elle sait détecter des insertions très discrètes, à condition que les images analysées
ressemblent à celles de l'entraînement. De son côté, la génération d'images a progressé à grande vitesse, et
l'on sait désormais que chaque famille de générateurs laisse des traces, en particulier dans les détails fins
et les hautes fréquences.

Les deux mondes se croisent pourtant peu. Le cover-source mismatch a été étudié en détail, mais surtout entre
sources naturelles, d'un appareil photo à l'autre. La forensique s'intéresse bien aux images générées, mais
pour dire si elles sont générées, pas pour y chercher un message. Quant au tatouage, il dépend du bon vouloir
des fournisseurs et peut être effacé. Aucun de ces travaux ne répond donc directement à la question posée en
introduction.

Il manque aussi un terrain d'étude. Pour mesurer l'effet d'une source sur la détection, il faut comparer des
sources traitées exactement de la même façon, avec les mêmes algorithmes d'insertion et à la même charge. Sans
cela, on ne sait plus si un écart vient de la source ou du protocole.

C'est dans cet espace que se place notre travail. Nous traitons les images générées comme une nouvelle source
de couverture, dans le cadre du cover-source mismatch, et nous examinons ce qu'elles font à une stéganalyse
classique fondée sur SRM et un classifieur linéaire. Deux difficultés sont attendues, le changement de source
et l'interférence entre les traces de la génération et celles de l'insertion. La seconde partie les met en
évidence, puis teste une manière d'y répondre.

# Partie II : Cas pratique

## 6. Méthodologie expérimentale

La première partie a laissé une question ouverte. La stéganalyse classique se trompe-t-elle sur les images
générées, et si oui, pourquoi ? Ce chapitre décrit la démarche mise en place pour y répondre. Il précise les
hypothèses testées et la façon dont le corpus a été construit, puis le détecteur et le protocole qui
permettent de lire les résultats des chapitres suivants.

### 6.1 Objectifs et hypothèses

Le travail s'organise autour de trois hypothèses, chacune reliée à une expérience.

La première, notée H1, porte sur le changement de source. Un détecteur entraîné sur des images naturelles
perdrait sa fiabilité lorsqu'on l'applique à des images générées. C'est l'objet de l'expérience A, qui compare
les performances du détecteur sur sa source d'origine et sur chacune des sources générées.

La deuxième, H2, porte sur l'interférence. Sur certaines images générées, les traces de la génération
masqueraient en partie celles de l'insertion, de sorte qu'une image porteuse s'écarterait moins de sa version
vierge que sur une photo. Cette hypothèse est délicate à tester avec un détecteur, puisqu'un mauvais score
pourrait venir du seul changement de source. L'expérience B la mesure donc directement dans l'espace des
caractéristiques, sans aucun apprentissage.

La troisième, H3, porte sur la solution. Adapter le détecteur à la source analysée devrait restaurer une
partie de la performance perdue. L'expérience C teste plusieurs façons de le faire, et cherche à distinguer ce
que l'adaptation répare de ce qu'elle ne répare pas.

Une dernière question, plus exploratoire, prolonge l'ensemble. Au-delà de la présence d'un message, est-il
possible de reconnaître l'algorithme qui l'a inséré ? L'expérience D l'aborde sur les images naturelles.

### 6.2 Constitution du corpus

Pour isoler l'effet de la source, il fallait des images de provenances différentes mais traitées exactement de
la même manière. Aucune base publique ne réunissant ces conditions, un corpus a été constitué pour ce travail.

Il comprend quatre sources de dix mille images chacune. Les images naturelles proviennent de BOSSbase 1.01, la
base de référence de la stéganalyse, composée de photographies en niveaux de gris [48]. Les images de Stable
Diffusion sont tirées de DiffusionDB, qui rassemble des images produites par les utilisateurs de ce modèle à
partir de leurs propres requêtes [42]. Celles de Midjourney et d'ADM viennent de GenImage, une base conçue
pour étudier la détection des images générées [41]. Le panel couvre ainsi trois manières de générer une image,
la diffusion latente avec Stable Diffusion, la diffusion dans l'espace des pixels avec ADM, et un service
commercial au fonctionnement non publié avec Midjourney.

La présence de Midjourney demande une explication. La première version du corpus prévoyait SDXL, une version
plus récente de Stable Diffusion. Il n'a toutefois pas été possible d'en réunir dix mille images issues d'une
même source cohérente, et Midjourney l'a remplacé. Ce changement s'est révélé utile. Midjourney et ADM
partagent la même base d'origine et des contenus de même nature, tirés des catégories d'ImageNet, ce qui les
rend directement comparables.

Toutes les images subissent ensuite le même prétraitement. Elles sont converties en niveaux de gris, recadrées
au centre sur 256 pixels de côté, puis enregistrées au format PGM, sans compression. Aucune image n'est
redimensionnée, car un redimensionnement modifie les relations entre pixels voisins, celles-là mêmes que lit
la stéganalyse. C'est ce traitement identique qui rend les sources comparables, et qui fait du corpus le
premier apport de ce mémoire.

Une limite doit être signalée dès maintenant. Les images de Stable Diffusion, issues de DiffusionDB, ont un
contenu souvent artistique, alors que celles de Midjourney et d'ADM représentent des animaux, des objets ou
des scènes du quotidien. Pour cette source, l'effet du générateur et celui du contenu restent donc en partie
mêlés. Nous y revenons dans la discussion.

### 6.3 Insertion stéganographique

Trois algorithmes d'insertion ont été retenus, de façon à couvrir les deux familles présentées au chapitre 1.
Le LSB matching représente l'insertion naïve, qui modifie les pixels sans tenir compte de leur voisinage [39].
S-UNIWARD [20] et HILL [38] représentent l'insertion adaptative, qui concentre les modifications dans les
zones texturées. Par commodité, le LSB matching est simplement appelé LSB dans la suite.

Chaque image vierge a été déclinée en trois versions porteuses, une par algorithme, toutes à la même charge de
0,4 bit par pixel. Cette valeur, courante dans la littérature, place la détection dans un régime ni trivial ni
hors de portée. Le corpus compte ainsi seize ensembles de dix mille images, soit chacune des quatre sources en
version vierge et en trois versions porteuses.

L'insertion a été réalisée avec la bibliothèque conseal [53]. Comme la plupart des outils de recherche en
stéganalyse, elle ne cache pas un vrai message mais simule les modifications qu'une insertion optimale
produirait à la charge demandée. Pour la détection, le résultat est équivalent, puisque seul compte l'effet de
l'insertion sur les pixels. La graine aléatoire a été fixée, afin que l'ensemble puisse être reproduit à
l'identique.

### 6.4 Détecteur de stéganalyse

Le détecteur reprend la chaîne classique de la stéganalyse décrite au chapitre 1. Il enchaîne trois étapes,
l'extraction des caractéristiques, leur réduction, puis la décision.

Les caractéristiques sont celles du modèle riche SRM, soit 34 671 valeurs par image [4], calculées avec la
bibliothèque sealwatch [54]. Ce choix s'est imposé après un premier essai avec SPAM. Ce descripteur détectait
bien le LSB, mais restait au niveau du hasard face à S-UNIWARD et HILL, ce qui rejoint les limites relevées au
chapitre 1. SRM permet de traiter les trois algorithmes sur un pied d'égalité. Le prix à payer est le temps de
calcul, si bien que l'extraction a dû être menée sur un serveur à plusieurs cœurs.

Avec plus de trente mille caractéristiques, un classifieur apprend mal et la mémoire sature vite. Les
caractéristiques sont donc d'abord normalisées, puis réduites à 300 composantes par une analyse en composantes
principales. La décision revient ensuite à une régression logistique, un classifieur linéaire qui attribue à
chaque image un score compris entre 0 et 1. Ce montage diffère de l'ensemble de FLD habituellement associé aux
modèles riches [30], mais il appartient à la même famille des classifieurs linéaires, et il est plus simple à
expliquer.

Le choix de ne pas recourir à l'apprentissage profond est délibéré. La question posée porte sur la stéganalyse
classique, et pour savoir si elle résiste aux images générées, il faut l'éprouver telle qu'elle est. Un réseau
comme SRNet [5] changerait l'objet même de l'étude. S'y ajoutent deux raisons pratiques. Un détecteur linéaire
reste lisible, ce qui aide à comprendre pourquoi il se trompe, et il ne demande ni carte graphique ni
entraînement de plusieurs jours. Rien n'indique pour autant qu'un réseau profond serait épargné par le
changement de source, et la question reste ouverte pour la suite.

### 6.5 Réduction de caractéristiques : PFA et S-SELECT

L'analyse en composantes principales a un défaut déjà évoqué au chapitre 1. Les composantes qu'elle construit
mélangent toutes les caractéristiques d'origine, si bien qu'on ne sait plus ce que mesure chacune. Une autre
voie a donc été évaluée, la méthode de sélection proposée par Gomis, Camara et Diop [37], qui conserve des
caractéristiques d'origine.

Cette méthode repose sur deux étages. Le premier, PFA, regroupe les caractéristiques qui apportent une
information voisine et garde dans chaque groupe la plus représentative [36]. Le second, S-SELECT, cherche le
bon nombre de caractéristiques à conserver. Pour chaque taille essayée, il partage les images en deux groupes
à l'aide des seules caractéristiques retenues, et mesure la netteté de ce partage par un score de silhouette.
La taille qui donne le partage le plus net l'emporte. L'idée est que, si les caractéristiques sont bien
choisies, les deux groupes qui se dessinent d'eux-mêmes correspondent aux images vierges et aux images
porteuses. Cette sélection n'a donc besoin d'aucune étiquette [37].

Sur notre corpus, cette hypothèse ne tient pas toujours. Les images diffèrent bien davantage par leur contenu
que par la trace, minuscule, de l'insertion, et le partage le plus net suit alors le contenu. Pour cette
raison, une variante a aussi été testée. Elle conserve le regroupement de PFA, mais choisit la taille du
sous-ensemble d'après la qualité de détection mesurée avec les étiquettes, au prix d'une méthode moins
universelle et plus coûteuse.

Les premiers essais montrent que la réduction elle-même est très efficace. Sur SRM, avec l'insertion LSB et
sur un échantillon de 200 images, la variante ramène plus de trente mille caractéristiques à 24 tout en
conservant une AUC de 0,912, contre 0,933 avec la totalité, alors que le critère de silhouette tombe à 0,738.
Ces résultats restent préliminaires et n'ont pas été étendus à l'ensemble du corpus. Les expériences des
chapitres suivants s'appuient donc sur l'analyse en composantes principales, plus simple à mettre en œuvre à
grande échelle, et la réduction par PFA reste une piste dont l'intérêt se confirme mais qu'il faudra
généraliser.

### 6.6 Métriques, protocole et infrastructure

La mesure principale est l'AUC, présentée au chapitre 1. Elle ne dépend d'aucun seuil et se lit simplement, la
valeur 0,5 correspondant à un détecteur qui répond au hasard. Elle ne suffit pourtant pas à décrire ce qui se
passe lorsqu'un détecteur change de source. Un détecteur peut garder une AUC honorable tout en déclenchant des
alertes sur presque toutes les images, si ses scores se sont déplacés d'un bloc. Le taux de faux positifs
complète donc l'AUC. Le seuil est fixé sur les images naturelles de façon à n'y produire que 5 % de fausses
alarmes, puis on compte la proportion d'images générées vierges qui dépassent ce même seuil.

Trois configurations reviennent tout au long des expériences. La référence mesure le détecteur sur sa propre
source, les images naturelles. Le cas croisé applique ce même détecteur, sans le modifier, à une source
générée. Le cas apparié entraîne et teste un détecteur sur la même source générée. La comparaison entre ces
deux derniers cas est décisive. Si le détecteur apparié retrouve une bonne performance, l'échec du cas croisé
tient au changement de source. S'il échoue lui aussi, c'est que la trace de l'insertion est elle-même
difficile à voir sur cette source, ce qui oriente vers l'interférence.

Pour que les chiffres ne dépendent pas d'un découpage favorable, les AUC sont calculées par validation croisée
à cinq plis, en gardant dans chaque pli la même proportion d'images vierges et porteuses. À dix mille images
par source, l'écart type de l'AUC de référence reste de l'ordre de 0,005, ce qui laisse peu de place au hasard
dans les écarts observés par la suite. L'expérience C, la plus gourmande en mémoire, procède autrement. Elle
utilise une partition fixe entre apprentissage et test, identique pour toutes les stratégies comparées, sur
cinq mille images par source.

L'ensemble repose enfin sur des outils libres. Les traitements sont écrits en Python, avec la bibliothèque
scikit-learn pour l'apprentissage. L'insertion et l'extraction de SRM, trop lourdes pour un ordinateur
personnel, ont été menées sur un serveur de calcul loué, et les données sont sauvegardées pour permettre de
reproduire chaque résultat. La même graine aléatoire est utilisée partout.

## 7. Les deux problèmes

Ce chapitre confronte le détecteur aux images générées. Il mesure d'abord ce que coûte le changement de
source, puis cherche à savoir si une partie de l'échec tient à l'image elle-même. Les deux expériences ne
posent pas la même question, mais leurs réponses finissent par se rejoindre.

### 7.1 Le décalage de domaine (expérience A)

Sur sa propre source, le détecteur se comporte comme prévu. Il repère le LSB presque sans erreur, avec une AUC
de 0,994. Les algorithmes adaptatifs résistent davantage, avec 0,784 pour S-UNIWARD et 0,711 pour HILL. Ces
chiffres restent en dessous de ceux que rapporte la littérature avec des détecteurs plus puissants, ce qui n'a
rien d'étonnant pour un classifieur linéaire. Ils progressent d'ailleurs avec le volume de données, puisque
les premiers essais à cinq mille images plafonnaient autour de 0,70 et 0,60. Ils fournissent surtout un point
de comparaison stable, avec un écart type de l'ordre de 0,005.

| Algorithme | Source | AUC croisée | AUC appariée | Faux positifs |
|---|---|---|---|---|
| LSB | Stable Diffusion | 0,729 | 0,962 | 71 % |
| LSB | Midjourney | 0,801 | 0,997 | 61 % |
| LSB | ADM | 0,886 | 0,980 | 48 % |
| S-UNIWARD | Stable Diffusion | 0,561 | 0,603 | 74 % |
| S-UNIWARD | Midjourney | 0,620 | 0,900 | 88 % |
| S-UNIWARD | ADM | 0,687 | 0,806 | 67 % |
| HILL | Stable Diffusion | 0,532 | 0,557 | 78 % |
| HILL | Midjourney | 0,566 | 0,846 | 90 % |
| HILL | ADM | 0,601 | 0,683 | 76 % |

Table: Tableau 7.1 : Expérience A, à 0,4 bpp et dix mille images par source. Références sur les images
naturelles : AUC de 0,994 pour LSB, 0,784 pour S-UNIWARD et 0,711 pour HILL. Les faux positifs sont mesurés au
seuil qui en produit 5 % sur les images naturelles.

Appliqué tel quel aux images générées, le même détecteur perd pied. Pour le LSB, l'AUC tombe à 0,729 sur
Stable Diffusion, 0,801 sur Midjourney et 0,886 sur ADM. Pour les adaptatifs, elle descend entre 0,53 et 0,69,
c'est-à-dire à peine au-dessus du hasard.

L'AUC ne dit pourtant pas tout. Au seuil fixé pour ne produire que 5 % de fausses alarmes sur les images
naturelles, le détecteur signale comme porteuses entre 48 % et 90 % des images générées vierges, selon la
source et l'algorithme. Même pour le LSB, l'algorithme le mieux détecté, près de trois images vierges de
Stable Diffusion sur quatre déclenchent une alerte. En situation réelle, un tel détecteur serait inutilisable,
car il noierait l'analyste sous les fausses alertes, exactement le risque évoqué au chapitre 1.

La colonne appariée permet de comprendre d'où vient cet échec. Réentraîné sur chaque source, le détecteur
retrouve une très bonne performance pour le LSB, entre 0,962 et 0,997. Pour les adaptatifs, il se redresse
nettement sur Midjourney, avec 0,900 pour S-UNIWARD et 0,846 pour HILL, au-delà même de la référence
naturelle, et dans une moindre mesure sur ADM, avec 0,806 et 0,683. Sur ces sources, l'échec du cas croisé
tenait donc bien au changement de source.

Stable Diffusion fait exception. Même entraîné sur ses propres images, le détecteur reste proche du hasard
face aux adaptatifs, avec 0,603 pour S-UNIWARD et 0,557 pour HILL. Le changement de source ne suffit plus à
expliquer cet échec, puisque le détecteur connaît cette fois la source. Tout se passe comme si la trace de
l'insertion était plus difficile à voir dans ces images que dans les autres. L'hypothèse H1 est donc
confirmée, avec une nuance de taille, que l'expérience B permet d'éclairer.

### 7.2 L'interférence des artefacts (expérience B)

Pour tester l'interférence, un détecteur n'est pas le bon instrument. Un mauvais score peut toujours venir
d'un apprentissage insuffisant ou d'un changement de source, si bien qu'il ne dit rien de certain sur la trace
elle-même. L'expérience B mesure donc directement l'écart entre images vierges et images porteuses, dans
l'espace des caractéristiques SRM, sans rien apprendre.

Une première tentative reposait sur des statistiques globales du résidu, comme sa variance ou son entropie.
Elle ne montrait d'effet sur aucune source. Ces mesures sont trop grossières pour saisir une insertion
adaptative, ce qui rejoint l'histoire de la stéganalyse retracée au chapitre 1, où les statistiques simples
ont dû céder la place aux modèles riches.

La mesure retenue est la distance de Mahalanobis. Pour chaque source et chaque algorithme, les
caractéristiques des images vierges et des images porteuses sont réduites à 200 composantes, puis on calcule
la distance entre les deux nuages de points. Cette distance mesure le déplacement moyen provoqué par
l'insertion, rapporté à la variabilité des images de la source. Une distance élevée signifie que l'insertion
ressort nettement de cette variabilité, une distance faible qu'elle s'y perd. Comparer chaque source au niveau
naturel revient alors à se demander si les images générées couvrent davantage l'insertion que les photos.

| Algorithme | Naturel | Stable Diffusion | Midjourney | ADM |
|---|---|---|---|---|
| LSB | 1,633 | 1,331 | 1,754 | 1,540 |
| S-UNIWARD | 0,912 | 0,534 | 1,297 | 0,974 |
| HILL | 0,772 | 0,459 | 1,169 | 0,745 |

Table: Tableau 7.2 : Expérience B, distance de Mahalanobis entre images vierges et images porteuses, à 0,4 bpp
et dix mille images par source. Une valeur inférieure au niveau naturel signale un masquage de l'insertion.

Pour Stable Diffusion, le résultat est net. La distance y est plus faible que sur les images naturelles pour
les trois algorithmes, d'environ 18 % pour le LSB et d'environ 40 % pour les adaptatifs, S-UNIWARD passant de
0,912 à 0,534 et HILL de 0,772 à 0,459. Le masquage est donc le plus fort là où il compte le plus, sur les
algorithmes conçus pour être discrets.

Les deux autres générateurs ne se comportent pas ainsi. Avec Midjourney, la distance dépasse au contraire le
niveau naturel pour tous les algorithmes, et nettement pour les adaptatifs, avec 1,297 et 1,169 contre 0,912
et 0,772. L'insertion y ressort davantage que sur une photo. L'explication la plus plausible tient au contenu,
des images plus lisses offrant moins de textures où se fondre, mais elle reste à confirmer. ADM, enfin, reste
proche du niveau naturel, un peu en dessous pour le LSB et HILL, un peu au-dessus pour S-UNIWARD, sans
masquage marqué.

L'hypothèse H2 est donc vérifiée, mais pour une seule source. L'interférence n'est pas une propriété de toutes
les images générées. Elle apparaît avec Stable Diffusion, qui est aussi la seule source sur laquelle le
détecteur apparié échouait.

### 7.3 Convergence

Prises ensemble, les deux expériences se répondent. L'expérience A montre deux visages de l'échec. Sur
Midjourney et ADM, le détecteur se trompe parce qu'il ne connaît pas la source, et il suffit de la lui faire
connaître pour qu'il se reprenne. Sur Stable Diffusion, il échoue même lorsqu'il la connaît. L'expérience B en
donne la raison sans passer par aucun détecteur. Dans ces images, l'insertion déplace moins les
caractéristiques, sa trace se noyant dans la variabilité propre à la source.

Les deux difficultés annoncées dans l'introduction existent donc bien, mais elles ne se répartissent pas de la
même manière. Le changement de source touche toutes les sources générées. L'interférence, elle, est portée par
Stable Diffusion seul, et surtout face aux algorithmes adaptatifs. Midjourney se place même à l'opposé,
puisque l'insertion y est plus visible que sur une photo. Une source commerciale peut ainsi se révéler un
support plus risqué qu'il n'y paraît pour qui veut cacher un message.

Une réserve s'impose toutefois. Les images de Stable Diffusion se distinguent aussi par leur contenu, souvent
artistique, alors que Midjourney et ADM partagent des contenus tirés d'ImageNet. Il n'est donc pas possible
d'attribuer l'interférence au seul générateur. Seule une seconde source Stable Diffusion, sur un contenu
comparable, permettrait de trancher.

Cette distinction prépare le chapitre suivant. Si le changement de source se corrige en informant le
détecteur, l'interférence touche la trace elle-même, et aucun réentraînement ne devrait suffire à la faire
réapparaître.

## 8. La solution

*[à rédiger]*

## 9. Ouverture : attribution multi-classe

*[à rédiger]*

## 10. Discussion générale et perspectives

*[à rédiger]*

# Conclusion générale

*[à rédiger]*

# Bibliographie

*[voir bibliographie.md]*
