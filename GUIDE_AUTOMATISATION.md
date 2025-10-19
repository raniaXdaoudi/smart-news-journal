# Guide d'automatisation

Guide pour configurer l'envoi par email et l'automatisation avec cron.

---

## Envoi par email (Gmail)

### 1. Créer un mot de passe d'application

1. Aller sur https://myaccount.google.com/
2. **Sécurité** → **Validation en deux étapes** (activez-la)
3. **Sécurité** → **Mots de passe d'application**
4. Créer un mot de passe pour "Mail"
5. Copier le mot de passe généré (16 caractères)

### 2. Configurer `.env`

```env
SEND_EMAIL=true
EMAIL_FROM=votre.email@gmail.com
EMAIL_PASSWORD=xxxx_xxxx_xxxx_xxxx
EMAIL_TO=destinataire@example.com
```

### 3. Tester

```bash
python3 journal.py
```

**Autres fournisseurs** :
- **Outlook** : `SMTP_SERVER=smtp-mail.outlook.com`
- **Yahoo** : `SMTP_SERVER=smtp.mail.yahoo.com`

---

## Automatisation avec cron

### 1. Rendre le script exécutable

```bash
chmod +x schedule_daily.sh
```

### 2. Tester le script

```bash
./schedule_daily.sh
cat logs/cron.log  # Vérifier les logs
```

### 3. Configurer cron

```bash
crontab -e
```

Ajouter une de ces lignes :

```bash
# Tous les jours à 8h
0 8 * * * /chemin/vers/smart-news-journal/schedule_daily.sh

# Du lundi au vendredi à 9h
0 9 * * 1-5 /chemin/vers/smart-news-journal/schedule_daily.sh
```

**Syntaxe** : `minute heure jour mois jour_semaine commande`


### 4. Vérifier

```bash
crontab -l              # Voir le crontab
cat logs/cron.log       # Voir les logs
```


## Résultat

Vous recevrez un email quotidien avec :
- **Objet** : Journal IA - 19/10/2025
- **Pièce jointe** : `mon_journal_2025-10-19.pdf`

**Conseil** : Testez toujours manuellement avant d'automatiser !
