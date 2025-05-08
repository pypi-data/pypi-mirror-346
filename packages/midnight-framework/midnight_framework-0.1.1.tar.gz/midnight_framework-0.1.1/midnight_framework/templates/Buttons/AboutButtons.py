import disnake
from disnake.ui import View, Button

class About_Buttons(View):
    def __init__(self):
        super().__init__(timeout=None)

        self.add_item(
            Button(
                label="Документация",
                url="https://discord.gg",
                style=disnake.ButtonStyle.url
            )
        )

        self.add_item(
            Button(
                label="Поддержка",
                url="https://discord.gg",
                style=disnake.ButtonStyle.url
            )
        )
