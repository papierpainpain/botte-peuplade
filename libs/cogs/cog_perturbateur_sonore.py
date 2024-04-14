import random
import nextcord
from nextcord import Interaction
from nextcord.ext import tasks, commands

from libs.utils.constants import Guild, Nuage
from libs.utils.logger import create_logger
from libs.utils.messages import MessageType
from libs.utils.nuage import NuageRepo

ICON = "🥳"
PATRICK_LE_PIGEON_REPO_ID = "a4f091fe-640d-46f7-8cc4-b13d30af99af"
PATRICK_LE_PIGEON_SOUND_DIR = "/Botte Peuplade/Sons qui font du bruit/"


class CogPerturbateurSonore(commands.Cog, description="Commandes système"):
    """Perturbateur sonore
    """

    def __init__(self, bot):
        self.bot = bot

        self._logger = create_logger(self.__class__.__name__)
        self._logger.info(f"{self.__class__.__name__} chargé")

        self.nuage_api = NuageRepo(PATRICK_LE_PIGEON_REPO_ID, Nuage.token)
        self.sound_bank = self.nuage_api.list_items_in_directory(
            PATRICK_LE_PIGEON_SOUND_DIR)
        self._logger.debug(f"Sound bank: {self.sound_bank}")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: nextcord.Member, before: nextcord.VoiceState, after: nextcord.VoiceState):
        """Listener pour la connexion/déconnexion du bot

        Parameters
        ----------
        member: nextcord.Member
            Membre
        before: nextcord.VoiceState
            Ancien état vocal
        after: nextcord.VoiceState
            Nouvel état vocal

        Returns
        -------
        None
        """

        self._logger.debug(
            f"Listener {self.on_voice_state_update.__name__} called")

        try:
            if not before.channel and after.channel and not after.channel.guild.voice_client:
                self._logger.debug(f"Connection en cours à '{after.channel.name}'")
                voice = await after.channel.connect()

                self._logger.info(f"Une menace a été détectée dans {after.channel.name}")
                voice.play(nextcord.FFmpegPCMAudio(f"libs/assets/avast.mp3"))

                self.perturbateur_sonore.start(voice)

            if before.channel and not after.channel and before.channel.guild.voice_client and len(before.channel.members) == 1:
                self.perturbateur_sonore.cancel()
                await before.channel.guild.voice_client.disconnect()

                self._logger.info(f"Bot déconnecté à {before.channel.name}")
        except Exception as e:
            self._logger.error(f"Erreur lors de la connexion/déconnexion: {e}")

    # Scheduled task
    @tasks.loop(minutes=4.5)
    async def perturbateur_sonore(self, voice: nextcord.VoiceClient = None):
        """Perturbation sonore

        Parameters
        ----------
        voice: nextcord.VoiceClient
            Client vocal

        Returns
        -------
        None
        """

        # Get random boolean with a chance of 1/60
        if not random.choice([True, False] + [False]*3):
            self._logger.debug("Pas de perturbation sonore")
            return

        self._logger.debug(f"Loop {self.perturbateur_sonore.name} called")

        try:
            song = random.choice(self.sound_bank)
            self._logger.debug(f"Playing {song["name"]}")
            song_download_link = self.nuage_api.get_download_link(
                f"{PATRICK_LE_PIGEON_SOUND_DIR}{song["name"]}")
            self._logger.debug(f"Download link: {song_download_link}")
            source = nextcord.FFmpegPCMAudio(song_download_link)

            if not voice.is_playing():
                voice.play(source)
            else:
                self._logger.warning("Le bot est déjà en train de jouer un son")
        except Exception as e:
            self._logger.error(f"Erreur lors de la perturbation sonore: {e}")
        finally:
            self._logger.debug("Perturbation sonore terminée")

    @nextcord.slash_command(name="reload-perturbateur", description="Re-chargement des sons", guild_ids=[Guild.id])
    async def reload_perturbateur(self, interaction: Interaction) -> None:
        """Re-chargement des sons

        Parameters
        ----------
        interaction: nextcord.Interaction
            Interaction du slash command

        Returns
        -------
        None
        """

        self._logger.debug(
            f"Slash command {self.reload_perturbateur.name} called")

        self.sound_bank = self.nuage_api.list_items_in_directory(
            PATRICK_LE_PIGEON_SOUND_DIR)

        self._logger.debug(f"Sound bank reloaded: {self.sound_bank}")
        await MessageType.info(interaction, f"Re-chargement des sons", ICON)


def setup(bot: commands.Bot):
    bot.add_cog(CogPerturbateurSonore(bot))
