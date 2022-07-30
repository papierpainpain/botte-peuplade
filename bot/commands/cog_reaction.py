import nextcord
from nextcord.ext import commands
from nextcord.ext.commands import Context

poopEdition = []
coeursMignons = []


class CogReaction(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="prout")
    async def prout(self, ctx):
        await ctx.send("@here 💨")

    @commands.command(name="poop-add")
    async def poop_add(self, ctx: Context, user: nextcord.User):
        if poopEdition.count(user) <= 0 and ctx.author.id == 242640786536005633:
            poopEdition.append(user)

    @commands.command(name="poop-rmv")
    async def poop_rmv(self, ctx: Context, user: nextcord.User):
        if poopEdition.count(user) > 0 and ctx.author.id == 242640786536005633:
            poopEdition.remove(user)

    # Comme les coeurs, c'est trop mignon
    @commands.command(name="coeur-add")
    async def coeur_add(self, ctx: Context, user: nextcord.User):
        if coeursMignons.count(user) <= 0 and ctx.author.id == 462191200938622986:
            coeursMignons.append(user)

    @commands.command(name="coeur-rmv")
    async def coeur_rmv(self, ctx: Context, user: nextcord.User):
        if coeursMignons.count(user) > 0 and ctx.author.id == 462191200938622986:
            coeursMignons.remove(user)

    @commands.Cog.listener()
    async def on_message(self, message):
        # Alexandre's poop edition
        for user in poopEdition:
            if message.author.id == user.id:
                await message.add_reaction('💩')

        # Les petits coeurs
        for user in coeursMignons:
            if message.author.id == user.id:
                await message.add_reaction('♥')


def setup(bot: commands.Bot):
    bot.add_cog(CogReaction(bot))
