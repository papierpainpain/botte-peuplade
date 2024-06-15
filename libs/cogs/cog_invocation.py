import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands

from libs.utils.constants import Bot, Colors, ZorblortAPI
from libs.utils.logger import create_logger
from libs.utils.messages import MessageType
from libs.utils.zorblort.zorblort import Zorblort

ICON = "👻"
ZORBLORT_ICON = "https://gitlab.papierpain.fr/uploads/-/system/project/avatar/153/zorblort.jpg?width=96"

CHARACTERS = {
    "Rick Sanchez": {
        "title": "Rick Sanchez",
        "model": "rick-sanchez"
    },
    "Par défaut": {
        "title": "Zorblort",
        "model": "llama3"
    }
}


class CogInvocation(commands.Cog, description="Invocation de Zorplort"):
    """Invocation de Zorplort

    """

    def __init__(self, bot: commands.Bot) -> None:
        """Initialisation du Cog

        Parameters
        ----------
        bot: commands.Bot
            Bot
        """

        self.bot: commands.Bot = bot
        self.zorblort = Zorblort(ZorblortAPI.HOST, True)

        self._logger = create_logger(self.__class__.__name__)
        self._logger.info(f"{self.__class__.__name__} chargé")

    async def _zorblort_message(self, interaction: Interaction, message: str, personnage: str, history: bool = False) -> None:
        """Message à envoyer à Zorblort

        Parameters
        ----------
        interaction: Interaction
            Interaction du slash command
        message: str
            Message à envoyer à Zorblort
        personnage: str
            Personnage à incarner
        history: bool
            Historique de la conversation

        Returns
        -------
        dict
            Réponse de Zorblort
        """

        self._logger.debug(f"Method called {self._zorblort_message.__name__}")

        await interaction.response.defer()

        try:
            model: str = CHARACTERS[personnage]["model"]
            zorblort_response = self.zorblort.message(
                message=message, model=model, history=history)

            self._logger.info(f"Zorblort API response: {zorblort_response}")

            full_message = f"> *{message}*\n\n{zorblort_response['message']}"

            embed = nextcord.Embed(
                description=full_message,
                color=Colors.INFO
            )
            embed.set_author(
                icon_url=ZORBLORT_ICON,
                name=CHARACTERS[personnage]["title"]
            )
            embed.set_footer(
                text=f"Temps : {round(zorblort_response["duration"], 2)} secondes")
            await interaction.send(embed=embed)
        except Exception as e:
            self._logger.error(f"Error while calling Zorblort API: {e}")
            await MessageType.error(interaction, "Erreur lors de l'invocation", ICON)

    @nextcord.slash_command(name="invocation", description="INVOCAAAAAAAAAAAAAAATIONNNNNN.... ᵖᵒᵘᶠ", guild_ids=Bot.GUILDS)
    async def invocation(
        self,
        interaction: Interaction,
        personnage: str = SlashOption(
            name="personnage",
            description="Personnage à incarner",
            choices=["Rick Sanchez", "Par défaut"],
            default="Par défaut"
        ),
        message: str = SlashOption(
            name="message",
            description="Message à envoyer à Zorblort",
            required=True
        )
    ) -> None:
        """Commande d'invocation

        Parameters
        ----------
        interaction: Interaction
            Interaction du slash command
        personnage: str
            Personnage à incarner
        message: str
            Message à envoyer à Zorblort
        """

        self._logger.debug(f"Slash command {self.invocation.name} called")

        await self._zorblort_message(interaction, message, personnage, history=True)

    @nextcord.slash_command(name="rick-sanchez", description="Invocation de Rick Sanchez", guild_ids=Bot.GUILDS)
    async def rick_sanchez(
        self,
        interaction: Interaction,
        message: str = SlashOption(
            name="message",
            description="Message à envoyer à Rick Sanchez",
            required=True
        )
    ) -> None:
        """Commande d'invocation

        Parameters
        ----------
        interaction: Interaction
            Interaction du slash command
        message: str
            Message à envoyer à Zorblort
        """

        self._logger.debug(f"Slash command {self.invocation.name} called")

        await self._zorblort_message(interaction, message, "Rick Sanchez", history=True)

    @nextcord.slash_command(name="nettoyage-historique", description="Nettoyage de l'historique de Zorblort", guild_ids=Bot.GUILDS)
    async def nettoyage_historique(
        self,
        interaction: Interaction,
        personnage: str = SlashOption(
            name="personnage",
            description="Personnage à nettoyer",
            choices=["Rick Sanchez", "Par défaut"],
            default="Par défaut"
        )
    ) -> None:
        """Nettoyage de l'historique de Zorblort

        Parameters
        ----------
        interaction: Interaction
            Interaction du slash command
        personnage: str
            Personnage à nettoyer
        """

        self._logger.debug(
            f"Slash command {self.nettoyage_historique.name} called")

        await interaction.response.defer()

        try:
            self.zorblort.clean_history(CHARACTERS[personnage]["model"])
            await MessageType.success(interaction, "Historique nettoyé", ICON)
        except Exception as e:
            self._logger.error(f"Error while cleaning Zorblort history: {e}")
            await MessageType.error(interaction, "Erreur lors du nettoyage de l'historique", ICON)


def setup(bot: commands.Bot):
    bot.add_cog(CogInvocation(bot))
