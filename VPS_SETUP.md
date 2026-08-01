# Guide : extraction SRM sur un VPS

But : lancer l'extraction des caractéristiques sur un serveur à plusieurs cœurs, sans interface,
en tâche de fond, puis récupérer les résultats.

## 1. Choisir le VPS

Prendre une machine CPU, pas GPU. SRM n'utilise pas le GPU.

- 8 à 16 vCPUs, 16 Go de RAM, une trentaine de Go de disque suffisent.
- Fournisseurs abordables : Hetzner, Contabo, Scaleway. Quelques euros pour quelques jours.
- Système : Ubuntu récent.

## 2. Préparer la machine

Se connecter en SSH, puis :

```
sudo apt update && sudo apt install -y python3-pip python3-venv tmux unzip
python3 -m venv venv && source venv/bin/activate
pip install sealwatch imageio scipy numpy gdown jupyter
```

## 3. Récupérer le corpus

Le corpus est archivé sur Google Drive (lien dans CORPUS.md). Le télécharger avec gdown, en
utilisant l'identifiant du fichier partagé :

```
mkdir -p memoire_data
gdown --id IDENTIFIANT_DU_FICHIER -O memoire_data/corpus.zip
```

L'identifiant est la longue chaîne dans le lien de partage, entre `/d/` et `/view`.
Le notebook décompresse l'archive automatiquement au premier lancement.

## 4. Récupérer le code

```
git clone https://github.com/mirfou111/memoire-steganalyse.git
cd memoire-steganalyse
```

Régler la cellule de configuration du notebook 01 selon le besoin, par exemple FEATURE = 'srmq1',
ALGOS = ['uniward', 'hill'], PAYLOADS = [0.4].

## 5. Lancer en tâche de fond

Utiliser tmux pour que le calcul survive à la déconnexion SSH :

```
tmux new -s extraction
jupyter nbconvert --to notebook --execute --inplace notebooks/01_extraction_features.ipynb
```

Détacher la session avec Ctrl-b puis d. Se reconnecter plus tard avec `tmux attach -t extraction`.
Le cache reprend tout seul si le calcul est interrompu.

## 6. Récupérer les caractéristiques

Depuis votre machine, copier le dossier des caractéristiques par scp :

```
scp -r utilisateur@IP_DU_VPS:~/memoire_data/features_srmq1 .
```

Puis les déposer sur votre Drive, dans memoire_data, pour que le notebook 02 les charge comme d'habitude.

## 7. Éteindre le VPS

Une fois les caractéristiques récupérées, détruire l'instance pour ne plus payer.

## Estimation

Le notebook affiche le temps par image et la durée par ensemble. Multipliez par le nombre d'ensembles
pour estimer le total, et ajustez le nombre de cœurs ou passez à SRMQ1 si c'est trop long.
