# Botte Peuplade

Bot Botte pour le serveur discord **LaPeuplade**.

## Developpement

Installer les requirements :

```bash
pip3 install -r local.requirements.txt
```

Créer le fichier .env :

```bash
# BOT
BOTTE_ENV=<development|production>
BOTTE_VERSION=<version-du-bot>
BOTTE_TOKEN=<token-du-bot-discord>
BOTTE_PREFIX=/
# GUILD
GUILD_ID=<id-de-votre-serveur-discord>
# MINECRAFT
MINECRAFT_HOST=<a-definir>
MINECRAFT_PORT=<a-definir>
MINECRAFT_USERNAME=<a-definir>
MINECRAFT_PASSWORD=<a-definir>
# BLAGUES
BLAGUE_API_TOKEN=<token-de-l-api-de-blagues>
```

Lancer le bot :

```bash
python3 main.py
```
