from dotenv import load_dotenv
import logging

from libs.botte import Botte
from libs.utils.constants import Bot

print("Lancement du Botte")

"""
Chargement des variables d'environnement
"""
load_dotenv()

"""
Configuration du logger
"""
logger = logging.getLogger('BOTTE')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='nextcord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

"""
Lancement du Botte
"""
botte = Botte()
botte.run(Bot.token)
