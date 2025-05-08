import disnake
from disnake.ext import commands

from Buttons.AboutButtons import About_Buttons
from core.enums import *

class About():
    def __init__(self, bot: disnake.Client):
        self.bot = bot

    @commands.slash_command(
        name='about',
        description=f'View information about the framework',
        dm_permission=False
    )
    async def action_command(self, interaction: disnake.ApplicationCommandInteraction):
        # Creating an embed (message)
        emb = disnake.Embed(
            title='Midnight',
            description=f"This bot is based on the **[Midnight] framework(https://github.com/z0nyx )**\n\n> In general **Midnight** is a ready-made template for fast and convenient creation of bots based on the library [disnake.py ](https://github.com/z0nyx ).",
            colour=0x2f3136
        )
        # Getting buttons from AboutButtons
        view = About_Buttons()

        await interaction.response.send_message(
            embed=emb,
            view=view,
            ephemeral=True
        )

# Launching cog
def setup(bot):
    bot.add_cog(About(bot))
    print('Ког: "/about" загрузился!')
