from os import environ as env

from nextcord.ext import commands


class Botte(commands.Bot):
    """
    Classe principale du Botte
    """

    def __init__(self, intents):
        super().__init__(command_prefix=env.get('BOTTE_PREFIX'),
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

        self.load_extension("bot.commands.cog_music")
        self.load_extension("bot.commands.cog_reaction")
        self.load_extension("bot.commands.cog_loup_garou")

    def add_listeners(self):
        """
        Ajoute les listeners
        """

        self.load_extension("bot.listeners.cog_message")
