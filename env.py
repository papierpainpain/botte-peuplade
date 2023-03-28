import configparser
from os import environ as env

"""
Chargement des variables d'environnement
"""

def env_var_from_config_file(config_file_name: str):
    # Get the config file
    config = configparser.ConfigParser()
    config.read(config_file_name)
    # Define env variables
    env.setdefault('BOTTE_VERSION', config['BOT']['VERSION'])
    env.setdefault('BOTTE_TOKEN', config['BOT']['TOKEN'])
    env.setdefault('BOTTE_PREFIX', config['BOT']['PREFIX'])
    env.setdefault('BOTTE_MUSIC_CHANNEL', config['BOT']['MUSIC_CHANNEL'])
    env.setdefault('BOTTE_GUILD_ID', config['BOT']['GUILD_ID'])

def check_env_var():
    if not env.get('BOTTE_VERSION'):
        raise Exception('BOTTE_VERSION non défini')
    if not env.get('BOTTE_TOKEN'):
        raise Exception('BOTTE_TOKEN non défini')
    if not env.get('BOTTE_PREFIX'):
        raise Exception('BOTTE_PREFIX non défini')
    if not env.get('BOTTE_MUSIC_CHANNEL'):
        raise Exception('BOTTE_MUSIC_CHANNEL non défini')
    if not env.get('BOTTE_GUILD_ID'):
        raise Exception('BOTTE_GUILD_ID non défini')
