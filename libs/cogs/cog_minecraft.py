import nextcord
from nextcord.ext import commands
from libs.utils.logger import create_logger
from libs.utils.messages import MessageType

from libs.utils.screen import Screen
from libs.utils.constants import Guild, Minecraft

ICON = "👾"


class CogMinecraft(commands.Cog, description="Minecraft commands"):

    def __init__(self, bot):
        self.bot = bot

        self._logger = create_logger(self.__class__.__name__)
        self._logger.info(f"{self.__class__.__name__} chargé")

    @nextcord.slash_command(name="mc-status", description="Retournes le status du serveur Minecraft", guild_ids=[Guild.id])
    async def minecraft_status(self, interaction: nextcord.Interaction, mc_name: str):
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

        screen = Screen("mc-" + mc_name, False, Minecraft.host,
                        Minecraft.username, Minecraft.password, Minecraft.port)

        if screen.exists:
            self._logger.info(f"{mc_name} est en ligne !")
            await MessageType.info(interaction, f"{mc_name} est en ligne !", ICON)
        else:
            self._logger.error(f"{mc_name} est hors ligne !")
            await MessageType.error(interaction, f"{mc_name} est hors ligne !", ICON)

    @nextcord.slash_command(name="mc-start", description="Démarrer le serveur Minecraft", guild_ids=[Guild.id])
    async def minecraft_start(self, interaction: nextcord.Interaction, mc_name: str):
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

        # Check if screen with mc-* name exists
        screen_list = Screen.list(
            Minecraft.host, Minecraft.username, Minecraft.password, Minecraft.port)
        if screen_list and any([screen.name.startswith("mc-") for screen in screen_list]):
            self._logger.error("Un serveur Minecraft est déjà en ligne !")
            await MessageType.error(interaction, f"Un serveur Minecraft est déjà en ligne !", ICON)
            return

        else:
            screen = Screen("mc-" + mc_name, True, Minecraft.host,
                            Minecraft.username, Minecraft.password, Minecraft.port)
            screen.send_commands(f"/home/minecraft/{mc_name}/start.sh")

            self._logger.info(f"{mc_name} est bientôt en ligne !")
            await MessageType.info(interaction, f"{mc_name} est bientôt en ligne !", ICON)

    @nextcord.slash_command(name="mc-stop", description="Arrêter le serveur Minecraft", guild_ids=[Guild.id])
    async def minecraft_stop(self, interaction: nextcord.Interaction, mc_name: str):
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

        screen = Screen("mc-" + mc_name, False, Minecraft.host,
                        Minecraft.username, Minecraft.password, Minecraft.port)

        screen.send_commands(f"stop")
        screen.kill()

        self._logger.info(f"{mc_name} est hors ligne !")
        await MessageType.info(interaction, f"{mc_name} est hors ligne !", ICON)

    @nextcord.slash_command(name="mc-restart", description="Redémarrer le serveur Minecraft", guild_ids=[Guild.id])
    async def minecraft_restart(self, interaction: nextcord.Interaction, mc_name: str):
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

        screen = Screen("mc-" + mc_name, False, Minecraft.host,
                        Minecraft.username, Minecraft.password, Minecraft.port)
        screen.send_commands(f"stop")
        screen.kill()
        screen.initialize()
        screen.send_commands(f"/home/minecraft/{mc_name}/start.sh")

        self._logger.info(f"{mc_name} est bientôt en ligne !")
        await MessageType.info(interaction, f"{mc_name} est en ligne !", ICON)


def setup(bot: commands.Bot):
    bot.add_cog(CogMinecraft(bot))
