from nextcord.ext import commands
from nextcord.ext.commands import Context
import nextcord


class CogMain(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help", aliases=['h'])
    async def help(self, ctx: Context):
        embed_announcement = nextcord.Embed(title="Commandes Bot Botte", colour=nextcord.Colour.from_rgb(0, 148, 133))
        embed_announcement.add_field(name="!help", value="Aide", inline=False)
        embed_announcement.add_field(name="!prout", value="Prouter Here", inline=True)
        embed_announcement.add_field(name="!poop-add @Someone", value="Poopage de quelqu'un", inline=False)
        embed_announcement.add_field(name="!poop-rmv @Someone", value="Dépoopage de quelqu'un", inline=True)
        embed_announcement.add_field(name="!coeur-add @Someone", value="Coeur sur quelqu'un", inline=False)
        embed_announcement.add_field(name="!coeur-rmv @Someone", value="Plus coeur sur quelqu'un", inline=True)
        embed_announcement.add_field(name="!play <url>", value="Exécuter une musique", inline=False)
        embed_announcement.add_field(name="!leave", value="Stopper la musique", inline=True)
        embed_announcement.add_field(name="!resume", value="Mise en lecture de la musique", inline=False)
        embed_announcement.add_field(name="!pause", value="Mise en pause de la musique", inline=True)
        embed_announcement.add_field(name="!skip", value="(ou !next) Musique suivante", inline=False)
        await ctx.send(embed=embed_announcement)

def setup(bot: commands.Bot):
    bot.add_cog(CogMain(bot))
