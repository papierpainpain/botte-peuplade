import nextcord
from nextcord.ext import commands
from libs.utils.logger import create_logger
from libs.utils.messages import MessageType

from libs.utils.screen import Screen
from libs.utils.constants import Bot, Minecraft

ICON = "👾"


class CogMinecraft(commands.Cog, description="Minecraft commands"):
    """Minecraft commands

    Attributes
    ----------
    bot: commands.Bot
        Bot
    _logger: Logger
        Logger de la classe

    Methods
    -------
    minecraft_status: Return the status of the Minecraft server
    minecraft_start: Start the Minecraft server
    minecraft_stop: Stop the Minecraft server
    minecraft_restart: Restart the Minecraft server
    """

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

        self._logger = create_logger(self.__class__.__name__)
        self._logger.info(f"{self.__class__.__name__} chargé")

    @nextcord.slash_command(name="mc-status", description="Retournes le status du serveur Minecraft", guild_ids=Bot.GUILDS)
    async def minecraft_status(self, interaction: nextcord.Interaction, mc_name: str) -> None:
        """Retournes le status du serveur Minecraft depuis son nom.

        Parameters
        ----------
        interaction: nextcord.Interaction
            Interaction du slash command
        mc_name: str
            Nom du serveur Minecraft
        """

        self._logger.debug(
            f"Slash command {self.minecraft_status.name} called")

        try:
            screen = Screen("mc-" + mc_name, False, Minecraft.HOST,
                            Minecraft.USERNAME, Minecraft.PASSWORD, Minecraft.PORT)

            if screen.exists:
                self._logger.info(f"{mc_name} est en ligne !")
                await MessageType.info(interaction, f"{mc_name} est en ligne !", ICON)
            else:
                self._logger.error(f"{mc_name} est hors ligne !")
                await MessageType.error(interaction, f"{mc_name} est hors ligne !", ICON)
        except Exception as e:
            self._logger.error(
                f"Erreur lors de la récupération du status: {e}")
            await MessageType.error(interaction, f"Erreur lors de la récupération du status: \n{e}", ICON)

    @nextcord.slash_command(name="mc-start", description="Démarrer le serveur Minecraft", guild_ids=Bot.GUILDS)
    async def minecraft_start(self, interaction: nextcord.Interaction, mc_name: str) -> None:
        """Démarrer le serveur Minecraft depuis son nom.

        Parameters
        ----------
        interaction: nextcord.Interaction
            Interaction du slash command
        mc_name: str
            Nom du serveur Minecraft
        """

        self._logger.debug(
            f"Slash command {self.minecraft_start.name} called")

        try:
            # Check if screen with mc-* name exists
            screen_list = Screen.list(
                Minecraft.HOST, Minecraft.USERNAME, Minecraft.PASSWORD, Minecraft.PORT)
            if screen_list and any([screen.name.startswith("mc-") for screen in screen_list]):
                self._logger.error("Un serveur Minecraft est déjà en ligne !")
                await MessageType.error(interaction, f"Un serveur Minecraft est déjà en ligne !", ICON)
                return

            else:
                screen = Screen("mc-" + mc_name, True, Minecraft.HOST,
                                Minecraft.USERNAME, Minecraft.PASSWORD, Minecraft.PORT)
                screen.send_commands(f"/home/minecraft/{mc_name}/start.sh")

                self._logger.info(f"{mc_name} est bientôt en ligne !")
                await MessageType.info(interaction, f"{mc_name} est bientôt en ligne !", ICON)

        except Exception as e:
            self._logger.error(
                f"Erreur lors du démarrage du serveur: {e}")
            await MessageType.error(interaction, f"Erreur lors du démarrage du serveur: \n{e}", ICON)

    @nextcord.slash_command(name="mc-stop", description="Arrêter le serveur Minecraft", guild_ids=Bot.GUILDS)
    async def minecraft_stop(self, interaction: nextcord.Interaction, mc_name: str) -> None:
        """Arrêter le serveur Minecraft depuis son nom.

        Parameters
        ----------
        interaction: nextcord.Interaction
            Interaction du slash command
        mc_name: str
            Nom du serveur Minecraft
        """

        self._logger.debug(
            f"Slash command {self.minecraft_stop.name} called")

        try:
            screen = Screen("mc-" + mc_name, False, Minecraft.HOST,
                            Minecraft.USERNAME, Minecraft.PASSWORD, Minecraft.PORT)

            screen.send_commands(f"stop")
            screen.kill()

            self._logger.info(f"{mc_name} est hors ligne !")
            await MessageType.info(interaction, f"{mc_name} est hors ligne !", ICON)
        except Exception as e:
            self._logger.error(
                f"Erreur lors de l'arrêt du serveur: {e}")
            await MessageType.error(interaction, f"Erreur lors de l'arrêt du serveur: \n{e}", ICON)

    @nextcord.slash_command(name="mc-restart", description="Redémarrer le serveur Minecraft", guild_ids=Bot.GUILDS)
    async def minecraft_restart(self, interaction: nextcord.Interaction, mc_name: str) -> None:
        """Redémarrer le serveur Minecraft depuis son nom.

        Parameters
        ----------
        interaction: nextcord.Interaction
            Interaction du slash command
        mc_name: str
            Nom du serveur Minecraft
        """

        self._logger.debug(
            f"Slash command {self.minecraft_restart.name} called")

        try:
            screen = Screen("mc-" + mc_name, False, Minecraft.HOST,
                            Minecraft.USERNAME, Minecraft.PASSWORD, Minecraft.PORT)
            screen.send_commands(f"stop")
            screen.kill()
            screen.initialize()
            screen.send_commands(f"/home/minecraft/{mc_name}/start.sh")

            self._logger.info(f"{mc_name} est bientôt en ligne !")
            await MessageType.info(interaction, f"{mc_name} est en ligne !", ICON)
        except Exception as e:
            self._logger.error(
                f"Erreur lors du redémarrage du serveur: {e}")
            await MessageType.error(interaction, f"Erreur lors du redémarrage du serveur: \n{e}", ICON)


def setup(bot: commands.Bot):
    bot.add_cog(CogMinecraft(bot))
