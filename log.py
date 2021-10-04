from discord import Embed
from termcolor import cprint

from strings import strings


colors_hex = {"green": 0x00FF00, "yellow": 0xFF9500, "red": 0xFF0000}


class Logger:
    def __init__(self, bot, channel_id):
        self.bot = bot
        self.channel_id = channel_id
        print()

    async def log(self, title, description, color):
        # Log in stdout
        out = title + "\n"
        if description:
            for line in description.split("\n"):
                out += "  | " + line + "\n"
        cprint(out, color)
        # Log on Discord
        channel = self.bot.get_channel(self.channel_id)
        embed = Embed(
            title=title, description=description, color=colors_hex[color]
        )
        await channel.send(embed=embed)
        return

    async def ready(self, title=strings["ready"]):
        await self.log(title, "", "green")
        return

    async def error(self, summary, error, title=strings["error"]):
        await self.log(title, f"{summary}\n```\n{error}\n```", "red")
        return

    async def warning(self, description, title=strings["warning"]):
        await self.log(title, description, "yellow")

    async def command_error(
        self, command, error, title=strings["command_error"]
    ):
        await self.warning(f"`{command}`\n```\n{error}\n```", title=title)
