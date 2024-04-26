import nextcord
from nextcord.ext import commands
from libs.utils.constants import Blagues, Bot, Colors
from blagues_api import BlaguesAPI

from libs.utils.logger import create_logger

ICON = "🤡"


class CogBlagues(commands.Cog, description="Balance ta blague"):

    def __init__(self, bot):
        self.bot = bot
        self.blagues_api = BlaguesAPI(Blagues.TOKEN)

        self._logger = create_logger(self.__class__.__name__)
        self._logger.info(f"{self.__class__.__name__} chargé")

    @nextcord.slash_command(name="blague", description="Balance ta blague", guild_ids=Bot.GUILDS)
    async def blague(self, interaction: nextcord.Interaction):
        """
        Envoie une blague aléatoire.

        Args:
            interaction (nextcord.Interaction): Interaction.
        """

        self._logger.debug(f"Slash command {self.blague.name} called")

        blague = await self.blagues_api.random()

        embed = nextcord.Embed(
            title=blague.joke, description=blague.answer, color=Colors.INFO)
        embed.set_author(name="Le Poti-Blagueur",
                         icon_url="https://i.ytimg.com/vi/xxoVynoUAn4/hqdefault.jpg")
        await interaction.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(CogBlagues(bot))
