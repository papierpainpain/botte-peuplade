import humanfriendly
import nextcord
import nextwave

from utils.constants import Colors


class MusicMessageType():
    """
    Types de messages
    """

    def track_embed(title: str, track: nextwave.YouTubeTrack):
        """
        Génère un embed pour une musique

        Args:
            title (str): Titre
            description (str): Description
        """

        embed = nextcord.Embed(
            title=f"🎶 {title}", description=f"On joue `{track.title}` par {track.author} \n **LIEN:** {track.uri}", color=Colors.info)
        embed.add_field(
            name="Durée", value=humanfriendly.format_timespan(track.duration))
        embed.set_image(url=track.thumbnail)
        return embed

    async def track_list(interaction: nextcord.Interaction, tracks):
        """
        Affiche la liste des musiques

        Args:
            interaction (nextcord.Interaction): Interaction
            tracks (Queue): Liste de musiques
        """

        embed = nextcord.Embed(
            title=f"🎶 Liste des musiques", color=Colors.info)

        for i, track in enumerate(tracks):
            embed.add_field(
                name="‏‏‎ ", value=f"**{i})** {track.title}", inline=False)

        embed.set_footer(text=f"Total: {len(tracks)}")

        message: nextcord.Message = await interaction.send(embed=embed)
        return message, await message.delete(delay=10)

    async def info(interaction: nextcord.Interaction, message: str, delete_after: float = 5):
        """
        Message d'information

        Args:
            interaction (nextcord.Interaction): Interaction
            message (str): Message
            delete_after (float, optional): Temps avant suppression (en secondes). Par défaut à 5.
        """

        embed = nextcord.Embed(
            title=f"🎶 | {message}", color=Colors.info)
        message: nextcord.Message = await interaction.send(embed=embed)
        return message, await message.delete(delay=delete_after)
