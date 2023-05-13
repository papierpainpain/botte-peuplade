import nextcord
from nextcord.ext import commands
from utils.messages import MessageType

from utils.modules.screen import Screen
from utils.constants import Guild, Minecraft


class CogMinecraft(commands.Cog, description="Minecraft commands"):

    def __init__(self, bot):
        self.bot = bot

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

        screen = Screen("mc-" + mc_name, False, Minecraft.host,
                        Minecraft.username, Minecraft.password, Minecraft.port)

        if screen.exists:
            await MessageType.info(interaction, f"{mc_name} est en ligne !")
        else:
            await MessageType.error(interaction, f"{mc_name} est hors ligne !")

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

        # Check if screen with mc-* name exists
        screen_list = Screen.list(
            Minecraft.host, Minecraft.username, Minecraft.password, Minecraft.port)
        if screen_list and any([screen.name.startswith("mc-") for screen in screen_list]):
            await MessageType.error(interaction, f"Un serveur Minecraft est déjà en ligne !")
            return

        else:
            screen = Screen("mc-" + mc_name, True, Minecraft.host,
                            Minecraft.username, Minecraft.password, Minecraft.port)
            screen.send_commands(f"/home/minecraft/{mc_name}/start.sh")

            await MessageType.info(interaction, f"{mc_name} est bientôt en ligne !")

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

        screen = Screen("mc-" + mc_name, False, Minecraft.host,
                        Minecraft.username, Minecraft.password, Minecraft.port)

        screen.send_commands(f"stop")
        screen.kill()

        await MessageType.info(interaction, f"{mc_name} est hors ligne !")

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

        screen = Screen("mc-" + mc_name, False, Minecraft.host,
                        Minecraft.username, Minecraft.password, Minecraft.port)
        screen.send_commands(f"stop")
        screen.kill()
        screen.initialize()
        screen.send_commands(f"/home/minecraft/{mc_name}/start.sh")

        await MessageType.info(interaction, f"{mc_name} est en ligne !")


def setup(bot: commands.Bot):
    bot.add_cog(CogMinecraft(bot))
