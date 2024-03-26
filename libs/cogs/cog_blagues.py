import nextcord
from nextcord.ext import commands
from libs.utils.constants import Blagues, Colors, Guild
from blagues_api import BlaguesAPI

ICON = "🤡"


class CogBlagues(commands.Cog, description="Balance ta blague"):

    def __init__(self, bot):
        self.bot = bot
        self.blagues_api = BlaguesAPI(Blagues.token)
        print("CogBlagues chargé")

    @nextcord.slash_command(name="blague", description="Balance ta blague", guild_ids=[Guild.id])
    async def blague(self, interaction: nextcord.Interaction):
        """
        Envoie une blague aléatoire.

        Args:
            interaction (nextcord.Interaction): Interaction.
        """

        blague = await self.blagues_api.random()

        embed = nextcord.Embed(
            title=blague.joke, description=blague.answer, color=Colors.info)
        embed.set_author(name="Le Poti-Blagueur",
                         icon_url="https://i.ytimg.com/vi/xxoVynoUAn4/hqdefault.jpg")
        await interaction.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(CogBlagues(bot))
