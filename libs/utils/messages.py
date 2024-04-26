import nextcord

from libs.utils.constants import Colors

DEFAULT_TIMEOUT = 30


class MessageType():
    """
    Types de messages
    """

    async def error(interaction: nextcord.Interaction, message: str, default_icon: str = "💂", delete_after: int = DEFAULT_TIMEOUT):
        """
        Message d'erreur

        Args:
            interaction (nextcord.Interaction): Interaction.
            message (str): Message.
            default_icon (str, optional): Icône par défaut. Par défaut à "💂".
            delete_after (int, optional): Temps avant suppression (en secondes). Par défaut à DEFAULT_TIMEOUT.
        """

        embed = nextcord.Embed(
            title=f"{default_icon} | {message}", color=Colors.ERROR)
        message: nextcord.Message = await interaction.send(embed=embed)
        return message, await message.delete(delay=delete_after)

    async def info(interaction: nextcord.Interaction, message: str, default_icon: str = "📢", delete_after: int = DEFAULT_TIMEOUT):
        """
        Message d'information

        Args:
            interaction (nextcord.Interaction): Interaction.
            message (str): Message.
            default_icon (str, optional): Icône par défaut. Par défaut à "📢".
            delete_after (int, optional): Temps avant suppression (en secondes). Par défaut à DEFAULT_TIMEOUT.
        """

        embed = nextcord.Embed(
            title=f"{default_icon} | {message}", color=Colors.INFO)
        message: nextcord.Message = await interaction.send(embed=embed)
        return message, await message.delete(delay=delete_after)

    async def warning(interaction: nextcord.Interaction, message: str, default_icon: str = "⚠️", delete_after: int = DEFAULT_TIMEOUT):
        """
        Message d'avertissement

        Args:
            interaction (nextcord.Interaction): Interaction.
            message (str): Message.
            default_icon (str, optional): Icône par défaut. Par défaut à "⚠️".
            delete_after (int, optional): Temps avant suppression (en secondes). Par défaut à DEFAULT_TIMEOUT.
        """

        embed = nextcord.Embed(
            title=f"{default_icon} | {message}", color=Colors.WARNING)
        message: nextcord.Message = await interaction.send(embed=embed)
        return message, await message.delete(delay=delete_after)
