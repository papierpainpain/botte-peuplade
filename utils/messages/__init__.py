import nextcord

from utils.constants import Colors, Emojis


class DeleteMessage(nextcord.ui.View):
    """
    View pour supprimer un message
    """

    def __init__(self, interaction: nextcord.Interaction):
        super().__init__(timeout=None)
        self.interaction = interaction

    async def interaction_check(self, interaction: nextcord.Interaction):
        if interaction.user.id != self.interaction.user.id:
            await interaction.response.send_message("🤡 C'est pas pour toi ! Gnegnegne...", ephemeral=True)
            return False
        else:
            return True

    @nextcord.ui.button(style=nextcord.ButtonStyle.secondary, emoji=Emojis.trashcan)
    async def stop(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.message.delete()


class MessageType():
    """
    Types de messages
    """

    async def error(interaction: nextcord.Interaction, message: str, delete_after: int = 5):
        """
        Message d'erreur

        Args:
            interaction (nextcord.Interaction): Interaction
            message (str): Message
            delete_after (int, optional): Temps avant suppression (en secondes). Par défaut à 5.
        """

        embed = nextcord.Embed(
            title=f"💂 | {message}", color=Colors.error)
        message: nextcord.Message = await interaction.send(embed=embed)
        return message, await message.delete(delay=delete_after)

    async def info(interaction: nextcord.Interaction, message: str, delete_after: int = 5):
        """
        Message d'information

        Args:
            interaction (nextcord.Interaction): Interaction
            message (str): Message
            delete_after (int, optional): Temps avant suppression (en secondes). Par défaut à 5.
        """

        embed = nextcord.Embed(
            title=f"📢 | {message}", color=Colors.info)
        message: nextcord.Message = await interaction.send(embed=embed)
        return message, await message.delete(delay=delete_after)

    async def warning(interaction: nextcord.Interaction, message: str, delete_after: int = 5):
        """
        Message d'avertissement

        Args:
            interaction (nextcord.Interaction): Interaction
            message (str): Message
            delete_after (int, optional): Temps avant suppression (en secondes). Par défaut à 5.
        """

        embed = nextcord.Embed(
            title=f"⚠️ | {message}", color=Colors.warning)
        message: nextcord.Message = await interaction.send(embed=embed)
        return message, await message.delete(delay=delete_after)
