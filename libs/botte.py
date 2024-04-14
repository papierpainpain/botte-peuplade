import os
import nextcord
from nextcord.ext import commands

from libs.utils.constants import Bot
from libs.utils.logger import create_logger


class Botte(commands.Bot):
    """
    Classe principale du Botte
    """

    def __init__(self):
        self._logger = create_logger(self.__class__.__name__)
        self._logger.info(f"{self.__class__.__name__} chargé")

        # Configuration des Intents Discord
        self._logger.debug("Configuration des Intents Discord")
        intents = nextcord.Intents.default()
        intents.message_content = True
        intents.members = True

        super().__init__(command_prefix=Bot.prefix,
                         intents=intents, help_command=None)

        self._logger.debug("Chargement des cogs")
        for filename in os.listdir("libs/cogs"):
            if filename.endswith(".py"):
                self.load_extension(f"libs.cogs.{filename[:-3]}")

    async def on_ready(self):
        """
        Quand le bot est prêt
        """

        self._logger.info("Bot prêt")
