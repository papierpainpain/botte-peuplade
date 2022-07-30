import configparser
from os import environ as env
import logging

import nextcord

from bot.botte import Botte

CONFIG_FILE_NAME = 'config.ini' # Seulement en mode development

"""
Configuration du logger
"""
logger = logging.getLogger('nextcord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='nextcord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

"""
Chargement des variables d'environnement
"""
if env.get('BOTTE_ENV') is None or env.get('BOTTE_ENV') == 'development':
    env.setdefault('BOTTE_ENV', 'development')

    config = configparser.ConfigParser()
    config.read(CONFIG_FILE_NAME)

    if config['BOT']['VERSION'] is None or config['BOT']['TOKEN'] is None or config['BOT']['PREFIX'] is None or config['BOT']['MUSIC_CHANNEL'] is None or config['BOT']['GUILD_ID'] is None:
        raise Exception(
            'BOTTE_VERSION, BOTTE_TOKEN, BOTTE_PREFIX, BOTTE_MUSIC_CHANNEL ou BOTTE_GUILD_ID non défini dans le fichier {}'.format(CONFIG_FILE_NAME))

    env.setdefault('BOTTE_VERSION', config['BOT']['VERSION'])
    env.setdefault('BOTTE_TOKEN', config['BOT']['TOKEN'])
    env.setdefault('BOTTE_PREFIX', config['BOT']['PREFIX'])
    env.setdefault('BOTTE_MUSIC_CHANNEL', config['BOT']['MUSIC_CHANNEL'])
    env.setdefault('BOTTE_GUILD_ID', config['BOT']['GUILD_ID'])
elif env.get('BOTTE_ENV') == 'production':
    if env.get('BOTTE_VERSION') is None:
        raise Exception('BOTTE_VERSION non défini')
    if env.get('BOTTE_TOKEN') is None:
        raise Exception('BOTTE_TOKEN non défini')
    if env.get('BOTTE_PREFIX') is None:
        raise Exception('BOTTE_PREFIX non défini')
    if env.get('BOTTE_MUSIC_CHANNEL') is None:
        raise Exception('BOTTE_MUSIC_CHANNEL non défini')
    if env.get("BOTTE_GUILD_ID") is None:
        raise Exception("BOTTE_GUILD_ID non défini")
else:
    raise Exception('BOTTE_ENV n\'est pas défini correctement')

"""
Chargement des Intents Discord
On active les fonctionnalités qui seront nécessaires au bot pour fonctionner (désactivées par défaut)
"""
intents = nextcord.Intents.default()
intents.message_content = True
intents.members = True

botte = Botte(intents=intents)
botte.run(env.get('BOTTE_TOKEN'))
