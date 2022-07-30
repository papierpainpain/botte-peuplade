from os import environ as env

from nextcord.ext import commands


class Botte(commands.Bot):
    """
    Constructeur de Botte
    """

    def __init__(self, intents):
        super().__init__(command_prefix=env.get('BOTTE_PREFIX'),
                         intents=intents, help_command=None)
        self.add_commands()
        self.add_listeners()

    """
    Écouteurs
    """

    async def on_ready(self):
        print("Botte est en fonctionnement")

    """
    Commandes
    """

    def add_commands(self):

        self.load_extension("bot.commands.cog_music")
        self.load_extension("bot.commands.cog_reaction")

    def add_listeners(self):

        self.load_extension("bot.listeners.cog_message")
