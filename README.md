# Smart News Journal

Système automatisé de veille technologique qui scrape des articles d'actualité IA, les résume et génère un journal quotidien en PDF envoyé par mail.

**Ce projet a été conçu dans un cadre personnel.**

---

## À propos

Smart News Journal est un outil qui vous permet de :
- Récupérer automatiquement des articles d'actualité sur l'IA
- Générer des résumés intelligents
- Créer un journal PDF quotidien
- Recevoir le journal par email chaque matin

---

## Fonctionnalités

- **Scraping multi-sources** : Récupère des articles depuis plusieurs sites
- **Résumé automatique** : Résume les articles avec des algorithmes NLP
- **Export PDF** : Génère un journal au format PDF
- **Envoi par email** : Envoie le PDF automatiquement par mail
- **Planification** : Automatise l'exécution quotidienne avec cron
- **Configuration flexible** : Personnalise sources, nombre d'articles et résumés

### Deux modes de résumé

- **LOCAL (Sumy)** - Recommandé : Fonctionne offline, résumés de qualité
- **API (Hugging Face)** - Expérimental : Nécessite un token, qualité variable

---

## Installation

```bash
# 1. Cloner le projet
git clone https://github.com/votre-utilisateur/smart-news-journal.git
cd smart-news-journal

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Créer et configurer le fichier .env
cp .env.example .env
nano .env  # ou vim, code, etc.
```

---

## Utilisation

### 1. Configuration minimale

Éditez le fichier `.env` :

```env
MODE=local
SOURCES=https://www.actuia.com/actualite/
MAX_ARTICLES=4
SENTENCES_COUNT=5
SEND_EMAIL=false
```

### 2. Lancer le programme

```bash
python3 journal.py
```

Le PDF sera généré dans le dossier `data/mon_journal_YYYY-MM-DD.pdf`

### 3. Configuration avancée

**Ajouter plusieurs sources** :
```env
SOURCES=https://www.actuia.com/actualite/,https://autre-site.com/ia/
```

**Modifier le nombre d'articles** :
```env
MAX_ARTICLES=10
```

**Changer la longueur des résumés** :
```env
SENTENCES_COUNT=8
```

---

## Automatisation (optionnel)

### Envoi par email

1. Configurez l'email dans `.env` :
```env
SEND_EMAIL=true
EMAIL_FROM=votre.email@gmail.com
EMAIL_PASSWORD=mot_de_passe_application
EMAIL_TO=destinataire@example.com
```

2. Exécutez le programme, le PDF sera envoyé par mail

### Planification quotidienne (cron)

Pour recevoir le journal automatiquement chaque matin :

```bash
# Éditer le crontab
crontab -e

# Ajouter cette ligne (exécution à 8h chaque jour)
0 8 * * * /chemin/absolu/vers/smart-news-journal/schedule_daily.sh
```

**Guide complet** : Consultez [GUIDE_AUTOMATISATION.md](GUIDE_AUTOMATISATION.md)

---

## Structure du projet

```
smart-news-journal/
├── core/
│   ├── scrap.py              # Scraping web
│   ├── summarizer_local.py   # Résumé local (Sumy)
│   ├── summarizer_api_hf.py  # Résumé via API
│   ├── pdf_generator.py      # Génération PDF
│   └── email_sender.py       # Envoi email
├── data/                     # PDFs générés
├── logs/                     # Logs d'exécution
├── journal.py                # Script principal
├── schedule_daily.sh         # Script cron
├── requirements.txt          # Dépendances
├── .env.example              # Configuration exemple
└── README.md                 # Documentation
```

---

## Technologies

- **Python 3.8+**
- **BeautifulSoup4** - Parsing HTML
- **Sumy** - Résumé automatique (LSA, Luhn, LexRank)
- **ReportLab** - Génération PDF
- **Requests** - Requêtes HTTP
- **python-dotenv** - Configuration

---

## Exemple de résultat

Fichier généré : `data/mon_journal_2025-10-19.pdf`

Contenu :
- Date et sources
- 4 articles (configurable)
- Pour chaque article : Titre, URL, Résumé (5 phrases)

---

## Dépannage

### Pas d'articles trouvés
- Vérifiez que l'URL dans `SOURCES` est accessible
- Testez avec l'URL par défaut : `https://www.actuia.com/actualite/`

### Email non envoyé
- Utilisez un mot de passe d'application pour Gmail
- Vérifiez les logs : `cat logs/cron.log`

### Erreur d'import
```bash
pip install -r requirements.txt
```

---

## Auteur

Projet personnel réalisé par **raniaXdaoudi**
