import os
import random
import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import tasks, commands
import requests

from libs.utils.constants import Bot, Nuage
from libs.utils.logger import create_logger
from libs.utils.messages import MessageType
from libs.utils.nuage import NuageRepo

ICON = "🥳"
PATRICK_LE_PIGEON_REPO_ID = "a4f091fe-640d-46f7-8cc4-b13d30af99af"
PATRICK_LE_PIGEON_SOUND_DIR = "/Botte Peuplade/Sons qui font du bruit/"


class CogPerturbateurSonore(commands.Cog, description="Commandes système"):
    """Perturbateur sonore
    """

    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
        self.voice = None

        self._logger = create_logger(self.__class__.__name__)
        self._logger.info(f"{self.__class__.__name__} chargé")

        self.nuage_api = NuageRepo(PATRICK_LE_PIGEON_REPO_ID, Nuage.TOKEN)
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
                self._logger.debug(f"Connection en cours à '{
                                   after.channel.name}'")
                self.voice = await after.channel.connect()

                self._logger.info(f"Une menace a été détectée dans {
                                  after.channel.name}")
                self.voice.play(nextcord.FFmpegPCMAudio(
                    f"libs/assets/avast.mp3"))

                self.perturbateur_sonore.start(self.voice)
            elif not before.channel and after.channel and member.id != self.bot.user.id:
                self._logger.info(f"{member.display_name} a rejoint {
                                  after.channel.name}")
                if self.voice and self.voice.channel == after.channel and not self.voice.is_playing():
                    self.voice.play(nextcord.FFmpegPCMAudio(
                        f"libs/assets/avast.mp3"))

            if before.channel and not after.channel and before.channel.guild.voice_client and len(before.channel.members) == 1:
                self.perturbateur_sonore.cancel()
                await before.channel.guild.voice_client.disconnect()
                self.voice = None

                self._logger.info(f"Bot déconnecté à {before.channel.name}")
        except Exception as e:
            self._logger.error(f"Erreur lors de la connexion/déconnexion: {e}")

    # Scheduled task
    @tasks.loop(minutes=7.0)
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

        self._logger.debug(f"Loop perturbateur_sonore called")

        if not random.choice([True, False]):
            self._logger.debug("Pas de perturbation sonore")
            return

        if voice.is_playing():
            self._logger.warning(
                "Le bot est déjà en train de jouer un son")
            return

        song = random.choice(self.sound_bank)
        self._logger.debug(f"Playing {song["name"]}")

        # Try and catch to avoid any errors and retry 3 times before giving up
        retries = 3
        while retries > 0:
            try:
                song_download_link = self.nuage_api.get_download_link(
                    f"{PATRICK_LE_PIGEON_SOUND_DIR}{song["name"]}")
                self._logger.debug(f"Download link: {song_download_link}")

                song_local_path = self._download_file(song_download_link)
                self._logger.debug(f"Local path: {song_local_path}")

                source = nextcord.FFmpegPCMAudio(song_local_path)

                voice.play(source)
                self._logger.debug("Perturbation sonore terminée")

                break
            except Exception as e:
                self._logger.error(
                    f"{4 - retries}/3 Erreur lors de la perturbation sonore: {e}")
                retries -= 1
        else:
            self._logger.error(f"Impossible de jouer le son: {song["name"]}")

    def _download_file(self, url: str) -> str:
        """Télécharge un fichier

        Parameters
        ----------
        url: str
            URL du fichier

        Returns
        -------
        str
            Chemin du fichier téléchargé
        """

        local_filename = url.split("/")[-1]
        download_base_path = "tmp"
        if not os.path.exists(download_base_path):
            os.makedirs(download_base_path)

        local_path = f"{download_base_path}/{local_filename}"

        if os.path.exists(local_path):
            self._logger.debug(f"File already exists: {local_path}")
        else:
            self._logger.debug(f"Downloading {url} to {local_path}")

            with requests.get(url, stream=True) as r:
                r.raise_for_status()
                with open(local_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)

        return local_path

    @nextcord.slash_command(name="reload-perturbateur", description="Re-chargement des sons", guild_ids=Bot.GUILDS)
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

        # Remove files in tmp folder
        if os.path.exists("tmp"):
            for file in os.listdir("tmp"):
                os.remove(f"tmp/{file}")

        self._logger.debug(f"Sound bank reloaded: {self.sound_bank}")
        await MessageType.info(interaction, f"Re-chargement des sons", ICON)

    @commands.is_owner()
    @nextcord.slash_command(name="connect-perturbateur", description="Connexion du perturbateur sonore", guild_ids=Bot.GUILDS)
    async def connect_perturbateur(self, interaction: Interaction, voice_channel: nextcord.VoiceChannel = SlashOption(name="channel", description="Channel vocal", required=True), force: bool = SlashOption(name="force", description="Forcer la connexion", required=False, default=False)):
        """Connexion du perturbateur sonore

        Parameters
        ----------
        interaction: nextcord.Interaction
            Interaction du slash command
        voice_channel: nextcord.VoiceChannel
            Channel vocal
        force: bool
            Forcer la connexion

        Returns
        -------
        None
        """

        if not self.voice or (self.voice and force):
            if self.voice:
                self.perturbateur_sonore.cancel()
                await self.voice.disconnect()

            self.voice = await voice_channel.connect()
            self.perturbateur_sonore.start(self.voice)

            self._logger.debug(f"Bot connecté à {voice_channel.name}")
            await MessageType.info(interaction, f"Connexion à {voice_channel.name}", ICON)
        else:
            self._logger.warning(
                "Le botte est déjà connecté à un channel vocal")
            await MessageType.error(interaction, f"Le botte est déjà connecté (faire force pour le déconnecter)", ICON)

    @commands.is_owner()
    @nextcord.slash_command(name="débrancher-mamie", description="Déconnexion du perturbateur sonore", guild_ids=Bot.GUILDS)
    async def debrancher_mamie(self, interaction: Interaction):
        """Déconnexion du perturbateur sonore

        Parameters
        ----------
        interaction: nextcord.Interaction
            Interaction du slash command

        Returns
        -------
        None
        """

        if self.voice:
            self.perturbateur_sonore.cancel()
            await self.voice.disconnect()

            self._logger.debug("Botte déconnecté")
            await MessageType.info(interaction, f"Déconnexion", ICON)
        else:
            self._logger.warning("Le botte n'est pas connecté")
            await MessageType.error(interaction, f"Le bot n'est pas connecté", ICON)


def setup(bot: commands.Bot):
    bot.add_cog(CogPerturbateurSonore(bot))
