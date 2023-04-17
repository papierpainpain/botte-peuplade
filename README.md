# Botte LaPeuplade

Bot Botte pour le serveur discord **LaPeuplade**.

## Developpement

Installer les requirements :

```bash
pip3 install -r requirements.txt
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
# SPOTIFY
SPOTIFY_CLIENT_ID=<id-du-client-spotify>
SPOTIFY_CLIENT_SECRET=<secret-du-client-spotify>
```

Lancer le bot :

```bash
python3 main.py
```

## Commandes

### Musique

* **/play**: Balance le son ;
* **/leave**: Allez ouste ! ;
* **/resume**: Il est temps de reprendre du service ;
* **/pause**: C'est l'heure de la sieste ;
* **/skip**: Faut savoir changer de disque ;
* **/clear**: Petit coup de karcher ;
* **/queue**: Fait moi voir ce que t'as.

### Reaction

* **/prout**: Prout ;
* **/poop-add**: Pooper quelqu'un ;
* **/poop-remove**: Dé-pooper quelqu'un ;
* **/coeur-add**: Coeur sur toi ;
* **/coeur-remove**: Je te quitte !
