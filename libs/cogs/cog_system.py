import random
import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands

from libs.utils.constants import Colors, Guild
from libs.utils.logger import create_logger

ICON = "⚙️"
ICON_LE_DECIDEUR_DE_CHOIX = "https://mystickermania.com/cdn/stickers/memes/sticker_2110-512x512.png"


class CogSystem(commands.Cog, description="Commandes système"):

    def __init__(self, bot):
        self.bot = bot

        self._logger = create_logger(self.__class__.__name__)
        self._logger.info(f"{self.__class__.__name__} chargé")

    async def _random_choose(self, interaction: Interaction, choices: list) -> str:
        """
        Fait un choix aléatoire parmi une liste de choix.

        Args:
            interaction (nextcord.Interaction): Interaction.
            choices (list): Liste des choix séparés par des virgules.
        """
        choice = random.choice(choices)
        description = f"Les choix : \n"
        for item in choices:
            description += f"- {item}\n"

        self._logger.debug(f"Les choix : {choices}")
        self._logger.info(f"Le choix choisi : {choice}")
        embed = nextcord.Embed(
            title=f"Le choix choisi : {choice}", description=description, color=Colors.info)
        embed.set_author(name="Le déciseur de choix", icon_url=ICON_LE_DECIDEUR_DE_CHOIX)
        await interaction.send(embed=embed)

    @nextcord.slash_command(name="choose", description="Choix aléatoire", guild_ids=[Guild.id])
    async def choose(self, interaction: Interaction, choices: str = SlashOption(name="choix", description="Les choix à faire", required=True)):
        """
        Fait un choix aléatoire parmi une liste de choix.

        Args:
            interaction (nextcord.Interaction): Interaction.
            choices (str): Liste des choix séparés par des virgules.
        """

        self._logger.debug(f"Slash command {self.choose.name} called")
        await self._random_choose(interaction, choices.split(","))

    @nextcord.slash_command(name="père-de-chaussure", description="Choix aléatoire", guild_ids=[Guild.id])
    async def pere_de_chaussure(self, interaction: Interaction, choices: str = SlashOption(name="choix", description="Les choix à faire", required=True)):
        """
        Fait un choix aléatoire parmi une liste de choix.

        Args:
            interaction (nextcord.Interaction): Interaction.
            choices (str): Liste des choix séparés par des virgules.
        """

        self._logger.debug(f"Slash command {self.pere_de_chaussure.name} called")
        await self._random_choose(interaction, choices.split(","))

    @nextcord.slash_command(name="saussure", description="Choix aléatoire", guild_ids=[Guild.id])
    async def saussure(self, interaction: Interaction, choices: str = SlashOption(name="choix", description="Les choix à faire", required=True)):
        """
        Fait un choix aléatoire parmi une liste de choix.

        Args:
            interaction (nextcord.Interaction): Interaction.
            choices (str): Liste des choix séparés par des virgules.
        """

        self._logger.debug(f"Slash command {self.saussure.name} called")
        await self._random_choose(interaction, choices.split(","))


def setup(bot: commands.Bot):
    bot.add_cog(CogSystem(bot))
