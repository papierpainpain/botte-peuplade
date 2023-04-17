import nextcord
from nextcord import SlashOption
from nextcord import Interaction
from nextcord import User
from nextcord.ext import commands

from utils.constants import Guild

poopEdition = []
coeursMignons = []


class CogReaction(commands.Cog):
    """
    Listener pour les réactions
    """

    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        name="prout",
        description="Prout général !!!",
        guild_ids=[Guild.id]
    )
    async def prout(self, interaction: Interaction):

        await interaction.send("@here :dash:")

    # Poop edition
    @nextcord.slash_command(
        name="poop",
        description="Caca sur toi ♥",
        guild_ids=[Guild.id]
    )
    async def poop_edition(
        self,
        interaction: Interaction,
        status: str = SlashOption(
            name="status",
            choices=["add", "remove"]
        ),
        user: User = SlashOption(name="user"),
    ):

        if status == "add":
            if user not in poopEdition:
                poopEdition.append(user)
                await interaction.send("{} 💩 Tu as été poopé !".format(user.mention))
            else:
                # Il est déjà poopé ! Tu deviens un poopé !
                poopEdition.append(interaction.user)
                await interaction.send("{} est déjà poopé ! Tu deviens un poopé !".format(user.mention))
        elif status == "remove":
            if user in poopEdition:
                poopEdition.remove(user)
                await interaction.send("{} 💩 Tu n'es plus poopé !".format(user.mention))
            else:
                await interaction.send("{} est déjà propre !".format(user.mention))
        else:
            await interaction.send("Perdu ! 😢")

    # Coeur edition
    @nextcord.slash_command(
        name="heart",
        description="Coeur sur toi ♥",
        guild_ids=[Guild.id]
    )
    async def coeur_edition(
        self,
        interaction: Interaction,
        status: str = SlashOption(
            name="status",
            choices=["add", "remove"]
        ),
        user: User = SlashOption(name="user"),
    ):

        if status == "add":
            if user not in coeursMignons:
                coeursMignons.append(user)
                await interaction.send("{} ♥ Coeur sur toi !".format(user.mention))
            else:
                await interaction.send("Tu es trop gentil, mais {} est déjà un coeur !".format(user.mention))
        elif status == "remove":
            if user in coeursMignons:
                coeursMignons.remove(user)
                await interaction.send("{} Tu n'es plus coeur 😢".format(user.mention))
            else:
                await interaction.send("{} n'est pas un coeur !".format(user.mention))
        else:
            await interaction.send("Perdu ! 😢")

    @commands.Cog.listener()
    async def on_message(self, message):
        for user in poopEdition:
            if message.author.id == user.id:
                await message.add_reaction('💩')

        for user in coeursMignons:
            if message.author.id == user.id:
                await message.add_reaction('♥')


def setup(bot: commands.Bot):
    bot.add_cog(CogReaction(bot))
