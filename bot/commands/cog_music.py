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

"""
def find_yt_video_by_query(query):
    query = query.replace()
    yt_search_url = "https://www.youtube.com/results?search_query="
    r = requests.get(yt_search_url).text
"""


async def youtube_search(search):
    p = {"search_query": search}
    h = {"User-Agent": "Mozilla/5.0"}
    async with aiohttp.ClientSession() as client:
        async with client.get(YT_BASE, params=p, headers=h) as resp:
            dom = await resp.text()
    found = re.findall(r'watch\?v=([a-zA-Z0-9_-]{11})', dom)
    print("found : {}".format(found))
    return f"https://youtu.be/watch?v={found[0]}"


class CogMusic(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.is_playing = False
        self.is_paused = False
        self.voice_client = None
        self.music_queue = list()

    async def play_song(self, interaction: Interaction):
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

            source = nextcord.PCMVolumeTransformer(nextcord.FFmpegPCMAudio(song.stream_url,
                                                                           before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"))
            self.voice_client.play(source, after=lambda e: self.play_next())
        else:
            self.is_playing = False

    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True
            new_song = self.music_queue[0][0]
            self.music_queue.pop(0)
            embed_message = nextcord.Embed(title="La musique elle a changé",
                                           colour=nextcord.Colour.from_rgb(37, 150, 190),
                                           description="[{0}]({1})".format(new_song.title, new_song.url))
            embed_message.set_author(name=f"Il reste {len(self.music_queue)} musiques dans la file" if len(
                self.music_queue) > 1 else f"Il reste {len(self.music_queue)} musique dans la file")
            asyncio.run_coroutine_threadsafe(self.bot.get_channel(int(env.get("BOTTE_MUSIC_CHANNEL"))).send(embed=embed_message),
                                             self.bot.loop)
            source = nextcord.PCMVolumeTransformer(nextcord.FFmpegPCMAudio(new_song.stream_url,
                                                                           before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"))
            self.voice_client.play(source, after=lambda e: self.play_next())

        else:
            self.is_playing = False
            asyncio.run_coroutine_threadsafe(self.voice_client.disconnect(), self.bot.loop)

    @nextcord.slash_command(name="play", description="Balance le son", guild_ids=[int(env.get("BOTTE_GUILD_ID"))])
    async def play(self, interaction: Interaction, url_ou_titre: str):
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
                yt_search_task = asyncio.create_task(youtube_search(url_ou_titre))
                await yt_search_task
                url = yt_search_task.result()
                if len(url) > 0:
                    music = Music(url)
            else:
                music = Music(url_ou_titre)

            self.music_queue.append([music, voice_channel])

            embed_message = nextcord.Embed(title="En cours de lecture", colour=nextcord.Colour.from_rgb(37, 150, 190),
                                           description="[{0}]({1})".format(music.title, music.url))
            embed_message.set_author(
                name="File d'attente (1/{})".format(len(self.music_queue)))
            embed_message.set_footer(text="Ajouté par {}".format(interaction.user.name), icon_url=interaction.user.avatar.url)
            asyncio.run_coroutine_threadsafe(self.bot.get_channel(int(env.get("BOTTE_MUSIC_CHANNEL"))).send(embed=embed_message),
                                             self.bot.loop)

            if not self.is_playing:
                await self.play_song(interaction)

            await interaction.send("Votre musique a été ajoutée à la file d'attente")

    @nextcord.slash_command(name="leave", description="Allez ouste !", guild_ids=[int(env.get("BOTTE_GUILD_ID"))])
    async def leave(self, interaction: Interaction):
        self.is_playing = False
        self.is_paused = False
        await self.voice_client.disconnect()

    @nextcord.slash_command(name="resume", description="Il est temps de reprendre du service", guild_ids=[int(env.get("BOTTE_GUILD_ID"))])
    async def resume(self, interaction: Interaction):
        if self.is_paused:
            self.is_playing = True
            self.is_paused = False
            self.voice_client.resume()
            embed_message = nextcord.Embed(title="Rayon de soleil reprend du service",
                                           colour=nextcord.Colour.from_rgb(37, 150, 190))
            embed_message.set_footer(text="Mis en route par {}".format(interaction.user.name),
                                     icon_url=interaction.user.avatar.url)
            await interaction.send(embed=embed_message)

    @nextcord.slash_command(name="pause", description="C'est l'heure de la sieste", guild_ids=[int(env.get("BOTTE_GUILD_ID"))])
    async def pause(self, interaction: Interaction):
        if self.is_playing:
            self.is_playing = False
            self.is_paused = True
            self.voice_client.pause()
            embed_message = nextcord.Embed(title="Rayon de soleil est en pause",
                                           colour=nextcord.Colour.from_rgb(37, 150, 190))
            embed_message.set_footer(text="Mis en pause par {}".format(interaction.user.name),
                                     icon_url=interaction.user.avatar.url)
            await interaction.send(embed=embed_message)

    @nextcord.slash_command(name="skip", description="Faut savoir changer de disque", guild_ids=[int(env.get("BOTTE_GUILD_ID"))])
    async def skip(self, interaction: Interaction):
        if self.voice_client is not None and self.voice_client:
            self.voice_client.stop()
            await self.play_song(interaction)

    @nextcord.slash_command(name="clear", description="L'odeur de la queue", guild_ids=[int(env.get("BOTTE_GUILD_ID"))])
    async def clear(self, interaction: Interaction):
        if self.voice_client is not None and not self.is_playing:
            self.voice_client.stop()
        self.music_queue.clear()
        embed_message = nextcord.Embed(title="Rayon de soleil utilise swiffer",
                                       colour=nextcord.Colour.from_rgb(37, 150, 190))
        embed_message.set_footer(text="L'acheteur du swiffer est {}".format(interaction.user.name),
                                 icon_url=interaction.user.avatar.url)
        await interaction.send(embed=embed_message)

    @nextcord.slash_command(name="queue", description="Fait moi voir ce que t'as", guild_ids=[int(env.get("BOTTE_GUILD_ID"))])
    async def queue(self, interaction: Interaction):
        retval = ""
        for i in range(0, len(self.music_queue)):
            if (i > 4): break
            retval += self.music_queue[i][0].title + "\n"

        if retval != "":
            await interaction.send(retval)
        else:
            await interaction.send("Il n'y a pas de musique dans la queue :'(")


def setup(bot: commands.Bot):
    bot.add_cog(CogMusic(bot))
