import os
import nextcord
from nextcord.ext import commands

from libs.utils.constants import Bot


class Botte(commands.Bot):
    """
    Classe principale du Botte
    """

    def __init__(self):
        # Configuration des Intents Discord
        intents = nextcord.Intents.default()
        intents.message_content = True
        intents.members = True

        super().__init__(command_prefix=Bot.prefix,
                         intents=intents, help_command=None)
        
        for filename in os.listdir("libs/cogs"):
            if filename.endswith(".py"):
                self.load_extension(f"libs.cogs.{filename[:-3]}")

    async def on_ready(self):
        """
        Quand le bot est prêt
        """

        print("Botte est en fonctionnement")
