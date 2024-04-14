from dotenv import load_dotenv

from libs.botte import Botte
from libs.utils.constants import Bot
from libs.utils.logger import create_logger

"""
Configuration du logger
"""
logger = create_logger('main')

"""
Chargement des variables d'environnement
"""
logger.debug("Chargement des variables d'environnement")
load_dotenv()

"""
Lancement du Botte
"""
try:
    logger.info("Lancement du Botte")
    botte = Botte()
    botte.run(Bot.token)
except Exception as e:
    logger.error(f"Erreur lors du lancement du Botte : {e}")
    exit(1)
