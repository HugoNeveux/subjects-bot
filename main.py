from discord.ext import commands, tasks
from discord.utils import get
from discord import Embed
import yaml
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

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
    """
    This functions sends a message every day in SUBJECTS_CHANNEL
    """
    channel = bot.get_channel(SUBJECTS_CHANNEL) # Get channel object
    with open("daily_subjects.txt", "r") as daily_subjects_list:
        subjects = daily_subjects_list.read().split("\n")
    try:
        await channel.send(f"<@&{PING_ROLE}> Bonjour ! Le sujet est **{subjects[0]}**.")   # Send subject
    except IndexError:
        await channel.send("Il n'y a pas de sujet prévu pour aujourd'hui.")
        return
    subjects = subjects[1:]
    with open("daily_subjects.txt", "w") as daily_subjects_list:
        daily_subjects_list.write("\n".join(subjects))  # Edit subjects list

@bot.command(pass_context = True)
async def ping(ctx):
    """
    Usual ping command
    """
    await ctx.send("Pong !")

@bot.command(pass_context = True)
@commands.has_role(STAFF_ROLE_NAME)
async def list_subjects(ctx):
    """
    List all daily subjects in daily_subjects.txt file
    """
    with open("daily_subjects.txt", "r") as daily_subjects_list:
        subjects = daily_subjects_list.read()
    embed = Embed(title = "Prochains sujets", description = subjects, color=0x000000)
    await ctx.send(embed = embed)

@bot.command(pass_context = True)
@commands.has_role(STAFF_ROLE_NAME)
async def add_subject(ctx, subject):
    """
    Add subject to the list
    """
    with open("daily_subjects.txt", "a") as daily_subjects_list:
        daily_subjects_list.write(subject)
    await ctx.send(f"Sujet {subject} ajouté à la fin de la liste !")

@bot.command(pass_context = True)
@commands.has_role(STAFF_ROLE_NAME)
async def remove_last_subject(ctx):
    """
    Remove last subject from list
    """
    with open("daily_subjects.txt", "r") as daily_subjects_list:
        subjects = daily_subjects_list.read().split("\n")[:-1]
    with open("daily_subjects.txt", "w") as daily_subjects_list:
        daily_subjects_list.write("\n".join(subjects))
    await ctx.send("Le dernier sujet de la liste a été supprimé.")

@bot.event
async def on_ready():
    """
    Function executed when the bot is running
    """
    print("Bot ready, configuration loaded.")
    print(f"Subjects channel : {SUBJECTS_CHANNEL}")
    print(f"Ping role : {PING_ROLE}")

    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_daily_subject, CronTrigger.from_crontab("0 0 * * *"))
    scheduler.start()

bot.run(TOKEN, bot=True, reconnect=True)
