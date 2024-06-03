import nextcord
from nextcord.ext import commands

from libs.utils.logger import create_logger


class CogMessage(commands.Cog):
    """Listener pour les messages

    C'est la partie inutile du bot, mais c'est pas mal <3

    Attributes
    ----------
    bot: commands.Bot
        Bot
    _logger: Logger
        Logger de la classe

    Methods
    -------
    on_message: Listener pour les messages
    """

    def __init__(self, bot: commands.Bot) -> None:
        """Initialisation du Cog

        Parameters
        ----------
        bot: commands.Bot
            Bot

        """

        self.bot = bot

        self._logger = create_logger(self.__class__.__name__)
        self._logger.info(f"{self.__class__.__name__} chargé")

    @commands.Cog.listener()
    async def on_message(self, message: nextcord.Message) -> None:
        """Listener pour les messages

        Parameters
        ----------
        message: nextcord.Message
            Message
        """

        self._logger.debug(f"Listener {self.on_message.__name__} called")

        if message.author == self.bot.user:
            return

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
