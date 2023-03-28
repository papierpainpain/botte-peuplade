import asyncio
import re
from os import environ as env

import aiohttp
import nextcord
from nextcord import Interaction
from nextcord.ext import commands

from bot.addons.music import Music

YT_BASE = "https://youtube.com/results"
YT_LINK_REGEX = "http(?:s?):\/\/(?:www\.)?youtu(?:be\.com\/watch\?v=|\.be\/)([\w\-\_]*)(&(amp;)?[\w\?=]*)?"
EMBED_COLOR = nextcord.Colour.from_rgb(0, 141, 125)


async def youtube_search(search):
    """
    Recherche sur Youtube

    Returns:
        str: Lien de la vidéo YouTube
    """

    p = {"search_query": search}
    h = {"User-Agent": "Mozilla/5.0"}
    async with aiohttp.ClientSession() as client:
        async with client.get(YT_BASE, params=p, headers=h) as resp:
            dom = await resp.text()
    found = re.findall(r'watch\?v=([a-zA-Z0-9_-]{11})', dom)
    # print("found : {}".format(found))
    return f"https://youtu.be/watch?v={found[0]}"


class CogMusic(commands.Cog):
    """
    Commandes de musique
    """

    def __init__(self, bot):
        self.bot = bot
        self.is_playing = False
        self.is_paused = False
        self.voice_client = None
        self.music_queue = list()

    async def play_song(self, interaction: Interaction):
        """
        Joue une musique
        """

        if len(self.music_queue) > 0:
            self.is_playing = True

            song = self.music_queue[0][0]

            if self.voice_client is None or not self.voice_client.is_connected():
                self.voice_client = await self.music_queue[0][1].connect()

                if self.voice_client is None:
                    await interaction.send("Le bot ne peut pas se connecter au salon")
                    return
            else:
                await self.voice_client.move_to(self.music_queue[0][1])

            self.music_queue.pop(0)

            source = nextcord.PCMVolumeTransformer(nextcord.FFmpegPCMAudio(
                song.stream_url, before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"))
            self.voice_client.play(source, after=lambda e: self.play_next())
        else:
            self.is_playing = False

    def play_next(self):
        """
        Joue la musique suivante
        """

        if len(self.music_queue) > 0:
            self.is_playing = True
            new_song = self.music_queue[0][0]
            self.music_queue.pop(0)
            embed_message = nextcord.Embed(title="La musique elle a changé", colour=EMBED_COLOR,
                                           description="[{0}]({1})".format(new_song.title, new_song.url))
            embed_message.set_author(name=f"Il reste {len(self.music_queue)} musiques dans la file" if len(
                self.music_queue) > 1 else f"Il reste {len(self.music_queue)} musique dans la file")
            asyncio.run_coroutine_threadsafe(self.bot.get_channel(
                int(env.get("BOTTE_MUSIC_CHANNEL"))).send(embed=embed_message), self.bot.loop)
            source = nextcord.PCMVolumeTransformer(nextcord.FFmpegPCMAudio(
                new_song.stream_url, before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"))
            self.voice_client.play(source, after=lambda e: self.play_next())

        else:
            self.is_playing = False
            asyncio.run_coroutine_threadsafe(
                self.voice_client.disconnect(), self.bot.loop)

    @nextcord.slash_command(name="play", description="Balance le son", guild_ids=[int(env.get("BOTTE_GUILD_ID"))])
    async def play(self, interaction: Interaction, url_ou_titre: str):
        """
        Commande /play : Balance le son
        """

        voice_status = interaction.user.voice
        if voice_status is None:
            await interaction.send("Tu dois être connecté à un salon pour pouvoir jouer de la musique")

        elif self.is_paused:
            self.voice_client.resume()

        else:
            voice_channel = voice_status.channel
            pattern = re.compile(YT_LINK_REGEX)
            music = None
            if not (pattern.match(url_ou_titre)):
                yt_search_task = asyncio.create_task(
                    youtube_search(url_ou_titre))
                await yt_search_task
                url = yt_search_task.result()
                if len(url) > 0:
                    music = Music(url)
                else:
                    await interaction.send("Aucune musique trouvée, faites une meilleure recherche...")
                    return
            else:
                music = Music(url_ou_titre)

            self.music_queue.append([music, voice_channel])

            embed_message = nextcord.Embed(
                title="En cours de lecture", colour=EMBED_COLOR, description="[{0}]({1})".format(music.title, music.url))
            embed_message.set_author(
                name="File d'attente (1/{})".format(len(self.music_queue)))
            embed_message.set_footer(text="Ajouté par {}".format(
                interaction.user.name), icon_url=interaction.user.avatar.url)
            asyncio.run_coroutine_threadsafe(self.bot.get_channel(
                int(env.get("BOTTE_MUSIC_CHANNEL"))).send(embed=embed_message), self.bot.loop)

            if not self.is_playing:
                await self.play_song(interaction)

            await interaction.send("Votre musique a été ajoutée à la file d'attente")

    @nextcord.slash_command(name="leave", description="Allez ouste !", guild_ids=[int(env.get("BOTTE_GUILD_ID"))])
    async def leave(self, interaction: Interaction):
        """
        Commande /leave : Allez ouste !
        """

        self.is_playing = False
        self.is_paused = False
        if self.voice_client is not None and not self.is_playing:
            self.voice_client.stop()
        self.music_queue.clear()
        await self.voice_client.disconnect()
        embed_message = nextcord.Embed(
            title="Rayon de soleil s'en va", colour=EMBED_COLOR)
        embed_message.set_footer(text="Arrêté par {}".format(
            interaction.user.name), icon_url=interaction.user.avatar.url)
        await interaction.send(embed=embed_message)

    @nextcord.slash_command(name="resume", description="Il est temps de reprendre du service", guild_ids=[int(env.get("BOTTE_GUILD_ID"))])
    async def resume(self, interaction: Interaction):
        """
        Commande /resume : Il est temps de reprendre du service
        """

        if self.is_paused:
            self.is_playing = True
            self.is_paused = False
            self.voice_client.resume()
            embed_message = nextcord.Embed(
                title="Rayon de soleil reprend du service", colour=EMBED_COLOR)
            embed_message.set_footer(text="Mis en route par {}".format(
                interaction.user.name), icon_url=interaction.user.avatar.url)
            await interaction.send(embed=embed_message)
        else:
            await interaction.send("Rayon de soleil n'est pas en pause")

    @nextcord.slash_command(name="pause", description="C'est l'heure de la sieste", guild_ids=[int(env.get("BOTTE_GUILD_ID"))])
    async def pause(self, interaction: Interaction):
        """
        Commande /pause : C'est l'heure de la sieste
        """

        if self.is_playing:
            self.is_playing = False
            self.is_paused = True
            self.voice_client.pause()
            embed_message = nextcord.Embed(
                title="Rayon de soleil est en pause", colour=EMBED_COLOR)
            embed_message.set_footer(text="Mis en pause par {}".format(
                interaction.user.name), icon_url=interaction.user.avatar.url)
            await interaction.send(embed=embed_message)

    @nextcord.slash_command(name="next", description="Faut savoir changer de disque", guild_ids=[int(env.get("BOTTE_GUILD_ID"))])
    async def skip(self, interaction: Interaction):
        """
        Commande /next : Faut savoir changer de disque
        """

        if self.voice_client is not None and self.voice_client:
            self.voice_client.stop()
        else:
            await interaction.send("Il n'y a pas de musique en cours de lecture")

    @nextcord.slash_command(name="clear", description="Petit coup de karcher", guild_ids=[int(env.get("BOTTE_GUILD_ID"))])
    async def clear(self, interaction: Interaction):
        """
        Commande /clear : Petit coup de karcher
        """

        if self.voice_client is not None and not self.is_playing:
            self.voice_client.stop()
        self.music_queue.clear()
        embed_message = nextcord.Embed(
            title="Rayon de soleil utilise swiffer", colour=EMBED_COLOR)
        embed_message.set_footer(text="L'acheteur du swiffer est {}".format(
            interaction.user.name), icon_url=interaction.user.avatar.url)
        await interaction.send(embed=embed_message)

    @nextcord.slash_command(name="queue", description="Fait moi voir ce que t'as", guild_ids=[int(env.get("BOTTE_GUILD_ID"))])
    async def queue(self, interaction: Interaction):
        """
        Commande /queue : Fait moi voir ce que t'as
        """

        # Faire une boucle pour afficher toutes les musiques de la file d'attente avec un embed
        if len(self.music_queue) > 0:
            embed_message = nextcord.Embed(
                title="File d'attente", colour=EMBED_COLOR)
            for i in range(0, len(self.music_queue)):
                embed_message.add_field(
                    name="{}/{}".format(i+1, len(self.music_queue)), value="[{0}]({1})".format(self.music_queue[i][0].title, self.music_queue[i][0].url), inline=False)
            embed_message.set_footer(text="Affiché par {}".format(
                interaction.user.name), icon_url=interaction.user.avatar.url)
            await interaction.send(embed=embed_message)
        else:
            await interaction.send("Il n'y a pas de musique dans la queue :'(")


def setup(bot: commands.Bot):
    bot.add_cog(CogMusic(bot))
