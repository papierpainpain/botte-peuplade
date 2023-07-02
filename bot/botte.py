import nextcord
from nextcord.ext import commands

from utils.constants import Bot


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
        self.add_commands()
        self.add_listeners()

    async def on_ready(self):
        """
        Quand le bot est prêt
        """

        print("Botte est en fonctionnement")

    def add_commands(self):
        """
        Ajoute les commandes
        """

        self.load_extension("bot.commands.cog_blagues")
        self.load_extension("bot.commands.cog_minecraft")
        self.load_extension("bot.commands.cog_music")
        self.load_extension("bot.commands.cog_reaction")
        self.load_extension("bot.commands.cog_system")

    def add_listeners(self):
        """
        Ajoute les listeners
        """

        self.load_extension("bot.listeners.cog_message")
