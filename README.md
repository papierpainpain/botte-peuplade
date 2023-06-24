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
# LAVALINK
LAVALINK_HOST=<host>
LAVALINK_PORT=<port>
LAVALINK_PASSWORD=<password>
# MINECRAFT
MINECRAFT_HOST=<a-definir>
MINECRAFT_PORT=<a-definir>
MINECRAFT_USERNAME=<a-definir>
MINECRAFT_PASSWORD=<a-definir>
```

Lancer Lavalink :

```bash
cd lavalink
java -Djdk.tls.client.protocols=TLSv1.1,TLSv1.2 -Xmx4G -jar Lavalink.jar
```

Si vous souhaiter utiliser la dernière version de LavaLink, vous pouvez la télécharger [ici](https://github.com/lavalink-devs/Lavalink/releases).

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
