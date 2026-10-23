# Expérience C : adaptation du détecteur (H3)

## Hypothèse

Adapter le détecteur restaure une part de la performance perdue à cause du décalage de domaine. On met en
scène cette idée comme solution et on en teste deux formes réalistes, sur les trois algorithmes.

## Démarche

Une partition train et test fixe par source, identique pour toutes les stratégies, rend les AUC comparables.
Détecteur linéaire précédé d'une réduction (normalisation, PCA à 300 composantes, régression logistique).
Corpus des quatre sources, sous-échantillonné à 5000 images par source pour cette expérience, la plus lourde
en mémoire. Quatre stratégies évaluées sur les sources générées :

- naturel seul : détecteur entraîné sur le naturel, appliqué au généré, rappelle le problème ;
- mixte : un seul détecteur entraîné sur naturel et généré mélangés ;
- conscient de la source : un classifieur identifie d'abord la source, puis route vers le détecteur apparié ;
- apparié : détecteur entraîné et testé sur la même source, borne haute.

Un volet supplémentaire teste la généralisation à un générateur non vu à l'entraînement.

## Résultats (SRM, 0,4 bpp)

AUC de test sur la source générée. Dernière colonne : exactitude d'identification de la source.

### LSB

| Source | naturel seul | mixte | conscient | apparié | id source |
|---|---|---|---|---|---|
| Stable Diffusion | 0,733 | 0,948 | 0,952 | 0,953 | 0,992 |
| Midjourney | 0,845 | 0,995 | 0,994 | 0,994 | 0,999 |
| ADM | 0,868 | 0,966 | 0,963 | 0,963 | 0,999 |

### S-UNIWARD

| Source | naturel seul | mixte | conscient | apparié | id source |
|---|---|---|---|---|---|
| Stable Diffusion | 0,563 | 0,593 | 0,555 | 0,557 | 0,996 |
| Midjourney | 0,609 | 0,861 | 0,878 | 0,878 | 0,999 |
| ADM | 0,645 | 0,746 | 0,742 | 0,742 | 0,999 |

### HILL

| Source | naturel seul | mixte | conscient | apparié | id source |
|---|---|---|---|---|---|
| Stable Diffusion | 0,536 | 0,547 | 0,522 | 0,523 | 0,996 |
| Midjourney | 0,555 | 0,783 | 0,820 | 0,820 | 0,999 |
| ADM | 0,576 | 0,649 | 0,639 | 0,639 | 0,998 |

Généralisation à un générateur non vu (naturel seul vers mixte sans cette source) :

| Source non vue | LSB | S-UNIWARD | HILL |
|---|---|---|---|
| Stable Diffusion | 0,733 → 0,924 | 0,563 → 0,595 | 0,536 → 0,547 |
| Midjourney | 0,845 → 0,980 | 0,609 → 0,772 | 0,555 → 0,684 |
| ADM | 0,868 → 0,952 | 0,645 → 0,716 | 0,576 → 0,600 |

Figures : expC_srm_strategies_<algo>_p04.png, expC_srm_loso_<algo>_p04.png.

## Lecture

Pour LSB, la solution fonctionne pleinement. Le détecteur naturel seul, plombé par le décalage de domaine,
remonte au niveau de la borne apparié sur les trois sources, de 0,733 à 0,95 pour Stable Diffusion, jusqu'à
0,99 pour Midjourney. Le réentraînement mixte, un détecteur unique, égale la détection consciente de la
source, dont le classifieur identifie l'origine à plus de 99 %.

Pour les algorithmes adaptatifs, la solution sépare nettement les deux problèmes. Sur Midjourney et ADM, qui
ne masquent pas l'insertion, l'adaptation récupère la détection : S-UNIWARD sur Midjourney passe de 0,609 à
0,878, HILL de 0,555 à 0,820, ADM de 0,645 à 0,742 et de 0,576 à 0,639. Le mixte et le conscient atteignent
la borne apparié, donc on récupère tout le récupérable.

Sur Stable Diffusion, au contraire, la solution bute. Pour S-UNIWARD, on passe seulement de 0,563 à 0,593,
et l'apparié lui-même plafonne à 0,557, quasi le hasard ; pour HILL, de 0,536 à 0,547, apparié 0,523. Même
le meilleur détecteur possible, entraîné sur Stable Diffusion, reste au niveau du hasard sur l'adaptatif. Le
réentraînement ne récupère pas un signal physiquement masqué.

Point subtil qui boucle la démonstration : l'identification de source reste excellente partout, donc la
détection consciente route bien les images Stable Diffusion vers leur détecteur dédié, mais cela ne sert à
rien puisque ce détecteur dédié est lui-même impuissant. Router correctement vers un détecteur au niveau du
hasard ne sauve pas.

Le volet du générateur non vu confirme : l'exposition à d'autres générés aide face à un générateur inconnu,
fortement pour LSB et pour l'adaptatif sur Midjourney et ADM, mais sans effet sur Stable Diffusion en
adaptatif.

## Portée et limites

La solution répare le décalage de domaine, partout pour LSB et pour l'adaptatif sur les sources sans
interférence, mais elle ne récupère pas ce que l'interférence masque, sur Stable Diffusion en adaptatif, ni
ce qui manque faute de données. C'est la séparation nette entre les deux problèmes, H1 réparable, H2 non.
Cette expérience est menée sur 5000 images par source, suffisant pour des AUC stables ; les autres
expériences utilisent les 10000.
