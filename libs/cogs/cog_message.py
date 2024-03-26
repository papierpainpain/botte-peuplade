from nextcord.ext import commands


class CogMessage(commands.Cog):
    """
    Listener pour les messages

    C'est la partie inutile du bot, mais c'est pas mal <3
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        # Si jamais le text enregistré correspond à une commande alors on appelle la commande associée
        if message.content.startswith(str(self.bot.command_prefix)):
            await self.bot.process_commands(message)

        msg_lower = message.content.lower()

        if msg_lower.startswith("quoi"):
            await message.reply('feur')

        if msg_lower.startswith('coucou'):
            await message.reply('Au revoir !')

        if msg_lower.startswith('hein'):
            await message.reply('deux')

        if msg_lower.endswith("non"):
            await message.reply('bril !')

        if msg_lower.endswith("oui"):
            await message.reply('stiti !')

        if msg_lower.find("g u e u l e") != -1 or msg_lower.find("gueule") != -1:
            await message.reply('FERME TA GUEULE TOI !!!!')

        if msg_lower == "cheh":
            await message.reply('CHEH toa même !')


def setup(bot: commands.Bot):
    bot.add_cog(CogMessage(bot))
