import sys
import traceback

import yaml
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from discord.ext import commands

from log import Logger
from strings import strings


# Load config
with open("config.yml") as configfile:
    config = yaml.safe_load(configfile)
    locals().update(config)
    prefix = config["prefix"]
    logs_channel_id = config["logs_channel_id"]
    subjects_channel_id = config["subjects_channel_id"]
    ping_role_id = config["ping_role_id"]
    token = config["token"]

bot = commands.Bot(prefix)

log = Logger(bot, logs_channel_id)


@bot.event
async def on_error(event, *args, **kwargs):
    await log.error(str(sys.exc_info()[1]), traceback.format_exc())


@bot.event
async def on_command_error(ctx, error):
    await log.command_error(
        ctx.message.content, str(error), title=strings["command_error"]
    )


@bot.command()
async def erreur(ctx):
    await ctx.send(3 / 0)


async def send_daily_subject():
    """This functions sends a message every day in the subjects channel"""
    # Get channel object
    channel = bot.get_channel(subjects_channel_id)
    # Read subjects
    with open("daily_subjects.txt", "r") as daily_subjects_list:
        subjects = daily_subjects_list.read().split("\n")
    try:
        # Send subject
        await channel.send(
            strings["subject_message"].format(
                f"<@&{ping_role_id}>", subjects[0]
            )
        )
    except IndexError:
        # Reply no subjects
        await channel.send(strings["no_subject_message"])
        return
    # Remove last subject
    subjects = subjects[1:]
    # Edit subjects list
    with open("daily_subjects.txt", "w") as daily_subjects_list:
        daily_subjects_list.write("\n".join(subjects))


@bot.event
async def on_ready():
    """Function executed when the bot is running"""

    # Load cogs
    bot.load_extension("cogs.manage")

    # Ready!
    await log.ready()

    # Schedule task to send subjects daily
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        send_daily_subject, CronTrigger.from_crontab("0 0 * * *")
    )
    scheduler.start()


bot.run(token, bot=True, reconnect=True)
