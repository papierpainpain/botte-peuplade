from typing import Union
import nextwave
from nextwave.ext import spotify

import nextcord
from nextcord.ext import commands

from utils.messages import DeleteMessage as MessageType
from utils.constants import Guild, Lavalink, Spotify
from utils.messages.music import MusicMessageType


class CogMusic(commands.Cog, description="Listen and Control that music which you want."):

    def __init__(self, bot):
        self.bot = bot
        bot.loop.create_task(self.node_connect())

    async def node_connect(self):
        """
        Connecte le bot au node de Lavalink.
        """

        await self.bot.wait_until_ready()
        await nextwave.NodePool.create_node(bot=self.bot, host=Lavalink.host, port=Lavalink.port, password=Lavalink.password, https=Lavalink.https, spotify_client=spotify.SpotifyClient(client_id=Spotify.client_id, client_secret=Spotify.client_secret))

    async def cog_check(self, interaction: nextcord.Interaction):
        """
        Vérifie si l'utilisateur est connecté au salon vocal.

        Args:
            interaction (nextcord.Interaction): Interaction
        """

        if not interaction.guild.voice_client:
            await MessageType.error(interaction, "Jeanne d'arc... Tu entends du son ?", 5)
            return False

        elif not interaction.user.voice:
            await MessageType.error(interaction, "Il faut que tu te connectes si tu veux que je te fasse vibrer 💃🏻", 5)
            return False

        else:
            return True

    async def add_track(self, interaction: nextcord.Interaction, track: Union[nextwave.PartialTrack, nextwave.YouTubeTrack]):
        """
        Ajoute une musique à la liste.

        Args:
            interaction (nextcord.Interaction): Interaction
            track (Union[nextwave.PartialTrack, nextwave.YouTubeTrack]): Track
        """

        if not track:
            return await MessageType.error(interaction, "Je n'ai pas trouvé la musique que tu cherches 😢", 20)

        print(f"> Track: {track.author} - {track.title} - {track.uri}")

        vc: nextwave.Player = interaction.guild.voice_client
        await vc.queue.put_wait(track)

        await MusicMessageType.info(interaction, f"Le Tube de l'année a été ajouté.", 20)

        if not vc.is_playing() and not vc.queue.is_empty:
            await vc.play(await vc.queue.get_wait())

    @commands.Cog.listener()
    async def on_nextwave_node_ready(self, node: nextwave.Node):
        """
        Quand le node est prêt, on affiche un message dans la console.

        Args:
            node (nextwave.Node): Node
        """

        print(f"Node <{node.identifier}> is ready!")

    @commands.Cog.listener()
    async def on_nextwave_track_end(self, player: nextwave.Player, track: nextwave.Track, reason):
        """
        Quand la musique est finie, on joue la prochaine musique de la queue.

        Args:
            player (nextwave.Player): Player
            track (nextwave.Track): Track
            reason (str): Raison
        """

        if not player.queue.is_empty:
            new_track = player.queue.get()
            print(f"> Musique actuelle : {new_track.author} - {new_track.title} - {new_track.uri}")
            await player.play(new_track)
            track_list = player.queue.copy()
            print(f"> Liste des musiques : {[track.title for track in track_list]}")

    @nextcord.slash_command(name="play", description="Balance le son", guild_ids=[Guild.id])
    async def play(self, interaction: nextcord.Interaction, search_music: str):
        """
        Joue de la musique.

        Args:
            interaction (nextcord.Interaction): Interaction
            search_music (str): Musique à rechercher
        """

        if not interaction.user.voice:
            return await MessageType.error(interaction, "Il faut que tu te connectes si tu veux que je te fasse vibrer 💃🏻", 5)

        elif not interaction.guild.voice_client:
            vc: nextwave.Player = await interaction.user.voice.channel.connect(cls=nextwave.Player)

        if not interaction.user.voice.channel == interaction.guild.voice_client.channel:
            msg = await MusicMessageType.info(interaction, "Je vais bientôt te rejoindre...", 7)
            vc: nextwave.Player = interaction.guild.voice_client
            await vc.move_to(interaction.user.voice.channel)
            return msg

        else:
            vc: nextwave.Player = interaction.guild.voice_client

        track = await nextwave.YouTubeTrack.search(query=search_music, return_first=True)

        await self.add_track(interaction, track)

    @nextcord.slash_command(name="playlist", description="Joue une playlist Youtube", guild_ids=[Guild.id])
    async def playlist(self, interaction: nextcord.Interaction, playlist_url: str, number_of_songs: int = 10):
        """
        Joue une playlist Youtube.

        Args:
            interaction (nextcord.Interaction): Interaction
            playlist_url (str): URL de la playlist
        """

        if not interaction.user.voice:
            return await MessageType.error(interaction, "Il faut que tu te connectes si tu veux que je te fasse vibrer 💃🏻", 5)

        elif not interaction.guild.voice_client:
            vc: nextwave.Player = await interaction.user.voice.channel.connect(cls=nextwave.Player)

        if not interaction.user.voice.channel == interaction.guild.voice_client.channel:
            msg = await MusicMessageType.info(interaction, "Je vais bientôt te rejoindre...", 7)
            vc: nextwave.Player = interaction.guild.voice_client
            await vc.move_to(interaction.user.voice.channel)
            return msg

        else:
            vc: nextwave.Player = interaction.guild.voice_client

        playlist = await vc.node.get_playlist(nextwave.YouTubePlaylist, playlist_url)

        if number_of_songs > len(playlist.tracks):
            number_of_songs = len(playlist.tracks)

        for track in playlist.tracks[:number_of_songs]:
            await self.add_track(interaction, track)
            # await asyncio.sleep(0.5)

    @nextcord.slash_command(name="next", description="Passe à la musique suivante", guild_ids=[Guild.id])
    async def next(self, interaction: nextcord.Interaction):
        """
        Passe à la musique suivante.

        Args:
            interaction (nextcord.Interaction): Interaction
        """

        if await self.cog_check(interaction):
            vc: nextwave.Player = interaction.guild.voice_client
            await vc.stop()
            await MusicMessageType.info(interaction, "On passe à la musique suivante, c'est reeeeepartiiiii !!!", 10)

    @nextcord.slash_command(name="pause", description="C'est l'heure de la sieste", guild_ids=[Guild.id])
    async def pause(self, interaction: nextcord.Interaction):
        """
        Met la musique en pause.

        Args:
            interaction (nextcord.Interaction): Interaction
        """

        if await self.cog_check(interaction):
            vc: nextwave.Player = interaction.guild.voice_client
            await vc.pause()
            await MusicMessageType.info(interaction, "⏸️ Rayon de soleil est en pause", 5)

        # if interaction.user is self._global_interaction.user:

        # else:
        #     await MessageType.warning(interaction, "🤡 Cette musique n'est pas la tienne, tu ne peux pas la mettre en pause.", 5)

    @nextcord.slash_command(name="resume", description="Il est temps de reprendre du service", guild_ids=[Guild.id])
    async def resume(self, interaction: nextcord.Interaction):
        """
        Reprend la musique.

        Args:
            interaction (nextcord.Interaction): Interaction
        """

        if await self.cog_check(interaction):
            vc: nextwave.Player = interaction.guild.voice_client
            await vc.resume()
            await MusicMessageType.info(interaction, "⏯️ Et c'est reparti !", 5)

        # if interaction.user is self._global_interaction.user:
        # else:
        #     await MessageType.warning(interaction, "🤡 Cette musique n'est pas la tienne, tu ne peux pas la mettre en pause.", 5)

    @nextcord.slash_command(name="queue", description="Affiche la liste des musiques en attente", guild_ids=[Guild.id])
    async def queue(self, interaction: nextcord.Interaction):
        """
        Affiche la liste des musiques en attente.

        Args:
            interaction (nextcord.Interaction): Interaction
        """

        if await self.cog_check(interaction):
            vc: nextwave.Player = interaction.guild.voice_client

        if vc.queue.is_empty:
            await MessageType.warning(interaction, "Ma queue est vide... :smirk:", 7)

        else:
            await MusicMessageType.track_list(interaction, vc.queue.copy())
    
    @nextcord.slash_command(name="shuffle", description="Ratoutouille de musiiique !", guild_ids=[Guild.id])
    async def shuffle(self, interaction: nextcord.Interaction):
        """
        Mélange toutes les musiques de la file d'attente.

        Args:
            interaction (nextcord.Interaction): Interaction
        """

        if await self.cog_check(interaction):
            vc: nextwave.Player = interaction.guild.voice_client
            vc.queue.shuffle()
            await MusicMessageType.info(interaction, "Ratoutouille de musiiique !", 5)

    @nextcord.slash_command(name="stop", description="🔌 Déconnecte le bot du channel vocal.", guild_ids=[Guild.id])
    async def vcdisconnect(self, interaction: nextcord.Interaction):
        """
        Déconnecte le bot du channel vocal.

        Args:
            interaction (nextcord.Interaction): Interaction
        """

        if await self.cog_check(interaction):
            vc: nextwave.Player = interaction.guild.voice_client
            await vc.stop()
            vc.queue.clear()
            await vc.disconnect()
            await MusicMessageType.info(interaction, "🔌 Mamie a été débranchée !", 5)

    @nextcord.slash_command(name="volume", description="Change le volume du bot.", guild_ids=[Guild.id])
    async def setvolume(self, interaction: nextcord.Interaction, volume: int):
        """
        Change le volume du bot.

        Args:
            interaction (nextcord.Interaction): Interaction
            volume (int): Volume
        """

        if await self.cog_check(interaction):
            vc: nextwave.Player = interaction.guild.voice_client

        # if interaction.user is self._global_interaction.user:

            if volume > 100:
                await MessageType.warning(interaction, "🤡 C'est beaucoup trop (tu vas exploser...).", 5)

            elif volume < 0:
                await MessageType.warning(interaction, "🤡 Gnegnegne...", 5)

            else:
                return await vc.set_volume(volume), await MusicMessageType.info(interaction, f"Le 🔊 volume a été défini à `{volume}%`", 3)

        else:
            await MessageType.warning(interaction, "🤡 Cette musique n'est pas la tienne, tu ne peux pas la mettre en pause.", 5)

    @nextcord.slash_command(name="nowplaying", description="Affiche les informations de la musique en cours.", guild_ids=[Guild.id])
    async def nowplaying(self, interaction: nextcord.Interaction):
        """
        Affiche les informations de la musique en cours.

        Args:
            interaction (nextcord.Interaction): Interaction
        """

        if await self.cog_check(interaction):
            vc: nextwave.Player = interaction.guild.voice_client

        if not vc.is_playing():
            return await MessageType.error(interaction, "Je ne joue pas de musique...", 5)

        embed = MusicMessageType.track_embed("Musique en cours", vc.track)
        message: nextcord.Message = await interaction.send(embed=embed)
        await message.delete(delay=5)


def setup(bot: commands.Bot):
    bot.add_cog(CogMusic(bot))
