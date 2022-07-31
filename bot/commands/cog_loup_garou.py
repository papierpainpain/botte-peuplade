from discord import SlashOption
import nextcord
from nextcord import Interaction
from nextcord.ext import commands
from gitlab import Gitlab

from os import environ as env


class CogLoupGarou(commands.Cog):
    """
    Gestion du serveur Minecraft loup garou
    """

    def __init__(self, bot):
        self.bot = bot
        self.running = False
        self.pipeline_process = False
        self.gitlab = Gitlab(url=env.get("GITLAB_URL"), private_token=env.get("GITLAB_TOKEN"))
        self.project = self.gitlab.projects.get(env.get("GITLAB_PROJECT_ID"))
    
    def run_loup_garou(self):
        _ = self.project.pipelines.create({
            'ref': 'master', 
            'variables': [
                {'key': 'PLAYBOOK_NAME', 'value': 'install_loup_garou.yml'},
                {'key': 'ENVIROMENT', 'value': 'inventory'},
                {'key': 'VARIABLES', 'value': 'lg_container_version=' + env.get("GITLAB_LG_VERSION")}
            ]
        })
        self.running = True
    
    def stop_loup_garou(self):
        _ = self.project.pipelines.create({
            'ref': 'master', 
            'variables': [
                {'key': 'PLAYBOOK_NAME', 'value': 'uninstall_loup_garou.yml'},
                {'key': 'ENVIROMENT', 'value': 'inventory'},
                {'key': 'VARIABLES', 'value': ''}
            ]
        })
        self.running = False

    @nextcord.slash_command(
        name="lg-server",
        description="Réveiller/Endormir le Loup Garou",
        guild_ids=[int(env.get("BOTTE_GUILD_ID"))]
    )
    async def lg_server(
        self, 
        interaction: Interaction, 
        status: str = SlashOption(
            name="statut",
            description="Le statut du Loup Garou",
            choices=["reveiller", "endormir"]
        )
    ):
        if status == "reveiller":
            if self.running:
                await interaction.send("Le Loup Garou est déjà réveillé ou il est en train de se réveiller")
            else:
                await interaction.send("Je vais essayer de le réveiller... (il se réveille en 5 à 10 minutes en général)")
                self.run_loup_garou()
        elif status == "endormir":
            if self.running:
                await interaction.send("Je vais essayer de l'endormir...")
                self.stop_loup_garou()
            else:
                await interaction.send("Le Loup Garou est déjà endormi")
        else:
            await interaction.send("Je ne comprends pas ce que tu veux faire...")


def setup(bot: commands.Bot):
    bot.add_cog(CogLoupGarou(bot))
