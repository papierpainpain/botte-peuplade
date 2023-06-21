import nextcord
from nextcord import SlashOption
from nextcord import Interaction
from nextcord import User
from nextcord.ext import commands
import random

from utils.constants import Guild

poopEdition = []
coeursMignons = []
victimes = []
gifTaper = [
    "https://tenor.com/view/mister-v-oh-jai-envie-de-te-goumer-goumer-je-vais-te-taper-menacer-gif-15403508",
    "https://tenor.com/view/claque-chat-claque-chat-chat-drole-de-quel-cote-tu-veux-ta-claque-gif-17697044",
    "https://tenor.com/view/spank-tom-and-jerry-tom-puppy-hit-gif-16778355",
    "https://tenor.com/view/cringe-eeee-gif-24636179",
    "https://tenor.com/view/slap-bear-slap-me-you-gif-17942299",
    "https://tenor.com/view/penguins-hit-gif-5498544",
    "https://tenor.com/view/hahahahah-gahahahaha-haha-ha-fun-gif-19042485"
]


class CogReaction(commands.Cog, description="Reaction commands"):
    """
    Listener pour les réactions
    """

    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="prout", description="Prout général !!!", guild_ids=[Guild.id])
    async def prout(self, interaction: Interaction):
        """Fait un prout à tout le monde.
        """

        await interaction.send("@here :dash:")

    @nextcord.slash_command(name="poop", description="Caca sur toi ♥", guild_ids=[Guild.id])
    async def poop_edition(self, interaction: Interaction, user: User = SlashOption(name="user"), status: str = SlashOption(name="status", choices=["add", "remove"])):
        """Fait caca sur les messages de quelqu'un.
        """

        if status == "add":
            if user not in poopEdition:
                poopEdition.append(user)
                await interaction.send("{} 💩 Tu as été poopé !".format(user.mention))
            else:
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

    @nextcord.slash_command(name="heart", description="Coeur sur toi ♥", guild_ids=[Guild.id])
    async def coeur_edition(self, interaction: Interaction, status: str = SlashOption(name="status", choices=["add", "remove"]), user: User = SlashOption(name="user")):
        """Fait des coeurs sur les messages de quelqu'un.
        """

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

    @nextcord.slash_command(name="taper", description="Je vais te taper !", guild_ids=[Guild.id])
    async def coeur_edition(self, interaction: Interaction, user: User = SlashOption(name="user")):
        """Je vais te taper !

        Parameters
        ----------
        interaction: nextcord.Interaction
            Interaction du slash command
        user: User
            Utilisateur à taper
        """

        # Ajout de l'utilisateur dans la liste des victimes si il n'y est pas
        # Sinon on incrémente son compteur de 4
        if user in victimes:
            for victime in victimes:
                if victime["user"] == user:
                    victime["compteur"] += 4
        else:
            victimes.append({"user": user, "compteur": 4})
        await interaction.send("Destruction de {} en cours...".format(user.name))

    @commands.Cog.listener()
    async def on_message(self, message):
        for user in poopEdition:
            if message.author.id == user.id:
                await message.add_reaction('💩')

        for user in coeursMignons:
            if message.author.id == user.id:
                await message.add_reaction('♥')

        for victime in victimes:
            if message.author.id == victime["user"].id and victime["compteur"] > 0:
                await message.reply(random.choice(gifTaper))
                victime["compteur"] -= 1


def setup(bot: commands.Bot):
    bot.add_cog(CogReaction(bot))
