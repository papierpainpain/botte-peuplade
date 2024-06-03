import os
import nextcord
from nextcord.ext import commands

from libs.utils.constants import Bot
from libs.utils.logger import create_logger


class Botte(commands.Bot):
    """Classe principale du Botte

    Attributes
    ----------
        _logger (Logger): Logger de la classe

    Methods
    -------
        on_ready: Action à effectuer quand le bot est prêt
    """

    def __init__(self) -> None:
        """Initialisation du Botte

        Les actions effectuées sont :
            - Configuration des Intents Discord
            - Chargement des cogs
        """

        self._logger = create_logger(self.__class__.__name__)
        self._logger.info(f"{self.__class__.__name__} chargé")

        # Configuration des Intents Discord
        self._logger.debug("Configuration des Intents Discord")
        intents = nextcord.Intents.default()
        intents.message_content = True
        intents.members = True

        super().__init__(command_prefix=Bot.PREFIX,
                         intents=intents, help_command=None)

        self._logger.debug("Chargement des cogs")
        for filename in os.listdir("libs/cogs"):
            if filename.endswith(".py"):
                self.load_extension(f"libs.cogs.{filename[:-3]}")

    async def on_ready(self) -> None:
        """Action à effectuer quand le bot est prêt
        """

        self._logger.info("Bot prêt")
