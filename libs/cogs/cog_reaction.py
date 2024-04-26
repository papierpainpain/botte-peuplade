from time import sleep
import nextcord
from nextcord import SlashOption
from nextcord import Interaction
from nextcord import User
from nextcord.ext import commands
import random

from libs.utils.constants import Bot
from libs.utils.logger import create_logger
from libs.utils.messages import MessageType

ICON = "🥳"

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

        self._logger = create_logger(self.__class__.__name__)
        self._logger.info(f"{self.__class__.__name__} chargé")

    @nextcord.slash_command(name="prout", description="Prout général !!!", guild_ids=Bot.GUILDS)
    async def prout(self, interaction: Interaction):
        """Fait un prout à tout le monde.
        """

        self._logger.debug(f"Slash command {self.prout.name} called")

        await interaction.send("@here :dash:")

    @nextcord.slash_command(name="poop", description="Caca sur toi ♥", guild_ids=Bot.GUILDS)
    async def poop_edition(self, interaction: Interaction, user: User = SlashOption(name="user"), status: str = SlashOption(name="status", choices=["add", "remove"])):
        """Fait caca sur les messages de quelqu'un.
        """

        self._logger.debug(
            f"Slash command {self.poop_edition.name} called")

        if status == "add":
            if user not in poopEdition:
                poopEdition.append(user)
                self._logger.info(f"{user.name} est poopé !")
                await interaction.send("{} 💩 Tu as été poopé !".format(user.mention))
            else:
                poopEdition.append(interaction.user)
                self._logger.info(
                    f"{user.name} est déjà poopé ! Tu deviens un poopé !")
                await interaction.send("{} est déjà poopé ! Tu deviens un poopé !".format(user.mention))
        elif status == "remove":
            if user in poopEdition:
                poopEdition.remove(user)
                self._logger.info(f"{user.name} n'est plus poopé !")
                await interaction.send("{} 💩 Tu n'es plus poopé !".format(user.mention))
            else:
                self._logger.info(f"{user.name} est déjà propre !")
                await interaction.send("{} est déjà propre !".format(user.mention))
        else:
            self._logger.error("Perdu ! 😢")
            await interaction.send("Perdu ! 😢")

    @nextcord.slash_command(name="heart", description="Coeur sur toi ♥", guild_ids=Bot.GUILDS)
    async def coeur_edition(self, interaction: Interaction, status: str = SlashOption(name="status", choices=["add", "remove"]), user: User = SlashOption(name="user")):
        """Fait des coeurs sur les messages de quelqu'un.
        """

        self._logger.debug(
            f"Slash command {self.coeur_edition.name} called")

        if status == "add":
            if user not in coeursMignons:
                coeursMignons.append(user)
                self._logger.info(f"{user.name} est un coeur !")
                await interaction.send("{} ♥ Coeur sur toi !".format(user.mention))
            else:
                self._logger.info(f"{user.name} est déjà un coeur !")
                await interaction.send("Tu es trop gentil, mais {} est déjà un coeur !".format(user.mention))
        elif status == "remove":
            if user in coeursMignons:
                coeursMignons.remove(user)
                self._logger.info(f"{user.name} n'est plus un coeur !")
                await interaction.send("{} Tu n'es plus coeur 😢".format(user.mention))
            else:
                self._logger.info(f"{user.name} n'est pas un coeur !")
                await interaction.send("{} n'est pas un coeur !".format(user.mention))
        else:
            self._logger.error("Perdu ! 😢")
            await interaction.send("Perdu ! 😢")

    @nextcord.slash_command(name="taper", description="Je vais te taper !", guild_ids=Bot.GUILDS)
    async def taper(self, interaction: Interaction, user: User = SlashOption(name="user")):
        """Je vais te taper !

        Parameters
        ----------
        interaction: nextcord.Interaction
            Interaction du slash command
        user: User
            Utilisateur à taper
        """

        self._logger.debug(f"Slash command {self.taper.name} called")

        await MessageType.info(interaction, f"Destruction de {user.name} en cours...", ICON)

        # Ajout de l'utilisateur dans la liste des victimes si il n'y est pas
        # Sinon on incrémente son compteur de 4
        if user in victimes:
            for victime in victimes:
                if victime["user"] == user:
                    victime["compteur"] += 4
        else:
            victimes.append({"user": user, "compteur": 4})

    @nextcord.slash_command(name="debout", description="Debout la d'dans !!", guild_ids=Bot.GUILDS)
    async def debout(self, interaction: Interaction, user: User = SlashOption(name="user"), motDoux: str = SlashOption(name="petit_message", default="Bouge toi !", description="Petit mot doux <3", required=False)):
        """Debout la d'dans !!

        Parameters
        ----------
        interaction: nextcord.Interaction
            Interaction du slash command
        user: User
            Utilisateur à réveiller
        motDoux: str
            Mot doux à envoyer
        """

        self._logger.debug(f"Slash command {self.debout.name} called")

        await MessageType.info(interaction, f"Opération réveil de {user.name} en cours...", ICON)

        # Envoi de 20 messages à l'utilisateur
        for _ in range(20):
            sleep(.5)
            self._logger.debug(f"Réveil de {user.name} en cours...")
            await MessageType.error(user, f"{motDoux}", ICON, delete_after=120)

    @commands.Cog.listener()
    async def on_message(self, message):

        self._logger.debug(f"Listener {self.on_message.__name__} called")

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
