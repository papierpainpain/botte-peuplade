import configparser
from os import environ as env
import logging
import nextcord
from bot.botte import Botte
from env import env_var_from_config_file
from env import check_env_var

CONFIG_FILE_NAME = 'config.ini'  # Seulement en mode development

"""
Configuration du logger
"""
logger = logging.getLogger('nextcord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(
    filename='nextcord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

"""
Chargement des variables d'environnement
"""
env.setdefault('BOTTE_ENV', 'development')
if env.get('BOTTE_ENV') == 'development':
    env_var_from_config_file(CONFIG_FILE_NAME)
    check_env_var()
elif env.get('BOTTE_ENV') == 'production':
    check_env_var()
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
