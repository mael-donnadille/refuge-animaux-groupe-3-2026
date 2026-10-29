# Projet Refuge
## Installation
1 - Installer les dépendances 
    
    poetry install

2 - Créer un une configuration PyCharm avec Python pointant sur le module refuge_esn81.main

## Base de donnée

1 - Créer une base de donnée nommée "animals"

2 - Modifier l'utilisateur et le mot de passe dans le fichier database/database.py

3 - Modifier l'utilisateur et le mot de passe dans le fichier alembic.ini

4 - Jouer les migrations en lançant la commande

    poetry run alembic upgrade head

## Lancement
1 - Appuyer sur la flèche !

2 - La doc de l'API est présente ici : http://localhost:9000/docs#
