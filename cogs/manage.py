import yaml
from discord import Embed
from discord.ext import commands

from strings import strings


with open("config.yml", "r") as configfile:
    config = yaml.safe_load(configfile)
    staff_role_name = config["staff_role_name"]


class Manage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_role(staff_role_name)
    async def list_subjects(self, ctx):
        """List all daily subjects in daily_subjects.txt file"""
        # Read subjects
        with open("daily_subjects.txt", "r") as daily_subjects_list:
            subjects = daily_subjects_list.read()
        # Reply
        embed = Embed(
            title=strings["list_subjects_title"],
            description=subjects,
            color=0x000000,
        )
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_role(staff_role_name)
    async def add_subject(self, ctx, subject):
        """Add subject to the list"""
        # Append subjects
        with open("daily_subjects.txt", "a") as daily_subjects_list:
            daily_subjects_list.write("\n" + subject)
        # Reply
        await ctx.send(strings["subject_added"].format(subject))

    @commands.command()
    @commands.has_role(staff_role_name)
    async def remove_last_subject(self, ctx):
        """Remove last subject from list"""
        # Read subjects except the last one
        with open("daily_subjects.txt", "r") as daily_subjects_list:
            subjects = daily_subjects_list.read().split("\n")[:-1]
        # Write subjects
        with open("daily_subjects.txt", "w") as daily_subjects_list:
            daily_subjects_list.write("\n".join(subjects))
        # Reply
        await ctx.send(strings["last_subject_removed"])


def setup(bot):
    bot.add_cog(Manage(bot))
