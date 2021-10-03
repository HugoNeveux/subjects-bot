import yaml
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from discord import Embed
from discord.ext import commands, tasks
from discord.utils import get


# Load bot config
with open("config.yml") as configfile:
    config = yaml.safe_load(configfile)
    TOKEN = config["token"]
    PREFIX = config["prefix"]
    SUBJECTS_CHANNEL = config["channel"]
    PING_ROLE = config["ping_role_id"]
    STAFF_ROLE_NAME = config["staff_role_name"]

bot = commands.Bot(PREFIX)


async def send_daily_subject():
    """This functions sends a message every day in SUBJECTS_CHANNEL"""
    # Get channel object
    channel = bot.get_channel(SUBJECTS_CHANNEL)
    # Read subjects
    with open("daily_subjects.txt", "r") as daily_subjects_list:
        subjects = daily_subjects_list.read().split("\n")
    try:
        # Send subject
        await channel.send(
            f"<@&{PING_ROLE}> Bonjour ! Le sujet est **{subjects[0]}**."
        )
    except IndexError:
        # Reply no subjects
        await channel.send("Il n'y a pas de sujet prévu pour aujourd'hui.")
        return
    # Remove last subject
    subjects = subjects[1:]
    # Edit subjects list
    with open("daily_subjects.txt", "w") as daily_subjects_list:
        daily_subjects_list.write("\n".join(subjects))


@bot.command(pass_context=True)
async def ping(ctx):
    """Usual ping command"""
    await ctx.send("Pong !")


@bot.command(pass_context=True)
@commands.has_role(STAFF_ROLE_NAME)
async def list_subjects(ctx):
    """List all daily subjects in daily_subjects.txt file"""
    # Read subjects
    with open("daily_subjects.txt", "r") as daily_subjects_list:
        subjects = daily_subjects_list.read()
    # Reply
    embed = Embed(title="Prochains sujets", description=subjects, color=0x000000)
    await ctx.send(embed=embed)


@bot.command(pass_context=True)
@commands.has_role(STAFF_ROLE_NAME)
async def add_subject(ctx, subject):
    """Add subject to the list"""
    # Append subjects
    with open("daily_subjects.txt", "a") as daily_subjects_list:
        daily_subjects_list.write("\n" + subject)
    # Reply
    await ctx.send(f"Sujet {subject} ajouté à la fin de la liste !")


@bot.command(pass_context=True)
@commands.has_role(STAFF_ROLE_NAME)
async def remove_last_subject(ctx):
    """Remove last subject from list"""
    # Read subjects except the last one
    with open("daily_subjects.txt", "r") as daily_subjects_list:
        subjects = daily_subjects_list.read().split("\n")[:-1]
    # Write subjects
    with open("daily_subjects.txt", "w") as daily_subjects_list:
        daily_subjects_list.write("\n".join(subjects))
    # Reply
    await ctx.send("Le dernier sujet de la liste a été supprimé.")


@bot.event
async def on_ready():
    """Function executed when the bot is running"""

    print("Bot ready, configuration loaded.")
    print(f"Subjects channel : {SUBJECTS_CHANNEL}")
    print(f"Ping role : {PING_ROLE}")

    # Schedule task to send subjects daily
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_daily_subject, CronTrigger.from_crontab("0 0 * * *"))
    scheduler.start()


bot.run(TOKEN, bot=True, reconnect=True)
