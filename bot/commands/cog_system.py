import random
import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands

from utils.constants import Colors, Guild

ICON = "⚙️"


class CogSystem(commands.Cog, description="Commandes système"):

    def __init__(self, bot):
        self.bot = bot
        print("CogSystem chargé")

    @nextcord.slash_command(name="choose", description="Choix aléatoire", guild_ids=[Guild.id])
    async def choose(self, interaction: Interaction, choices: str = SlashOption(name="choix", description="Les choix à faire", required=True)):
        """
        Fait un choix aléatoire parmi une liste de choix.

        Args:
            interaction (nextcord.Interaction): Interaction.
            choices (str): Liste des choix séparés par des virgules.
        """

        choice = random.choice(choices.split(","))

        description = f"Les choix : \n"
        for item in choices.split(","):
            description += f"- {item}\n"

        embed = nextcord.Embed(
            title=f"Le choix choisi : {choice}", description=description, color=Colors.info)
        embed.set_author(name="Le déciseur de choix",
                         icon_url="https://mystickermania.com/cdn/stickers/memes/sticker_2110-512x512.png")
        await interaction.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(CogSystem(bot))
