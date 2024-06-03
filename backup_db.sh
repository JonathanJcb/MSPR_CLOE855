#!/bin/bash

# Variables du backup
DB_PATH="/home/jonathanjcb129/www/flask1/database.db"
BACKUP_PATH=" /home/jonathanjcb129/www/flask1/backup"
DATE=$(date +"%Y%m%d%H%M")
BACKUP_FILE="database_backup_$DATE.db"
REMOTE_USER="JONATHAN"
REMOTE_HOST="176.175.172.29"
REMOTE_PATH="/backup/"

# Copier la base de données
cp $DB_PATH $BACKUP_PATH/$BACKUP_FILE

# Envoyer le fichier de sauvegarde à la machine personnelle
scp -i ~/.ssh/id_rsa_backup $BACKUP_PATH/$BACKUP_FILE $REMOTE_USER@$REMOTE_HOST:$REMOTE_PATH
